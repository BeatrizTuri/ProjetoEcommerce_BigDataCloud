from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    TextPrompt,
    ConfirmPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory
from botbuilder.schema import HeroCard, CardImage, Attachment
from services.product_api import ProductAPI

class ConsultarProdutoDialog(ComponentDialog):
    def __init__(self, product_api: ProductAPI):
        super().__init__("ConsultarProdutoDialog")
        self.product_api = product_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))  # <- novo prompt
        self.add_dialog(
            WaterfallDialog(
                "consultarProdutoWaterfallDialog",
                [
                    self.product_name_step,
                    self.show_product_info_step,
                    self.ask_repeat_step,         # <- novo passo
                    self.loop_or_end_step,        # <- novo passo
                ],
            )
        )
        self.initial_dialog_id = "consultarProdutoWaterfallDialog"

    async def product_name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_message = MessageFactory.text("Por favor, digite o nome do produto que você deseja consultar.")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def show_product_info_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        product_name = step_context.result
        produtos = self.product_api.consultar_produtos(product_name)

        if not produtos:
            await step_context.context.send_activity("❌ Nenhum produto encontrado com esse nome.")
            return await step_context.next(None)

        attachments = []
        for produto in produtos[:3]:
            images = []
            # Se houver imagem, adiciona ao HeroCard
            if produto.get("imageUrl"):
                # imageUrl pode ser lista, pega a primeira imagem
                url = produto["imageUrl"][0] if isinstance(produto["imageUrl"], list) else produto["imageUrl"]
                images = [CardImage(url=url)]
            card = HeroCard(
                title=produto.get("productName", "Sem nome"),
                subtitle=f"R$ {produto.get('price', '0.00')}",
                text=produto.get("productDescription", "Sem descrição"),
                images=images
            )
            attachments.append(Attachment(content_type="application/vnd.microsoft.card.hero", content=card))

        await step_context.context.send_activity(
            MessageFactory.carousel(attachments, "Produtos encontrados:")
        )
        return await step_context.next(None)

    async def ask_repeat_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_message = "Deseja consultar outro produto?"
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(prompt_message))
        )

    async def loop_or_end_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            return await step_context.replace_dialog(self.id)  # Reinicia o diálogo
        await step_context.context.send_activity("✅ Consulta finalizada. Se precisar de algo mais, estou à disposição.")
        return await step_context.end_dialog("retornar_ao_menu")
