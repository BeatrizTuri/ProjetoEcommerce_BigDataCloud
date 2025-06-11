from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ConfirmPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory
from botbuilder.schema import HeroCard, CardImage, Attachment
from services.product_api import ProductAPI

class ConsultarTodosProdutosDialog(ComponentDialog):
    def __init__(self, product_api: ProductAPI):
        super().__init__("ConsultarTodosProdutosDialog")
        self.product_api = product_api

        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "consultarTodosProdutosWaterfallDialog",
                [
                    self.show_all_products_step,
                    self.ask_repeat_step,
                    self.loop_or_end_step,
                ],
            )
        )
        self.initial_dialog_id = "consultarTodosProdutosWaterfallDialog"

    async def show_all_products_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        produtos = self.product_api.consultar_todos_produtos()

        if not produtos:
            await step_context.context.send_activity("❌ Nenhum produto cadastrado no momento.")
            return await step_context.next(None)

        attachments = []
        for produto in produtos:
            images = []
            if produto.get("imageUrl"):
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
            MessageFactory.carousel(attachments, "Todos os produtos cadastrados:")
        )
        return await step_context.next(None)

    async def ask_repeat_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_message = "Deseja visualizar novamente todos os produtos?"
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(prompt_message))
        )

    async def loop_or_end_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            return await step_context.replace_dialog(self.id)
        await step_context.context.send_activity("✅ Consulta finalizada.")
        return await step_context.end_dialog("retornar_ao_menu")
