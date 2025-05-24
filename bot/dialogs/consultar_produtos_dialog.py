import requests
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from services.product_api import ProductAPI

class ConsultarProdutoDialog(ComponentDialog):
    def __init__(self, product_api: ProductAPI):
        super().__init__("ConsultarProdutoDialog")
        self.product_api = product_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "consultarProdutoWaterfallDialog",
                [
                    self.product_name_step,
                    self.show_product_info_step,
                ],
            )
        )
        self.initial_dialog_id = "consultarProdutoWaterfallDialog"

    async def product_name_step(self, step_context: WaterfallStepContext):
        prompt_message = MessageFactory.text("Por favor, digite o nome do produto que você deseja consultar.")
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def show_product_info_step(self, step_context: WaterfallStepContext):
        product_name = step_context.result
        produtos = self.product_api.consultar_produtos(product_name)

        if not produtos:
            await step_context.context.send_activity("❌ Nenhum produto encontrado com esse nome.")
            return await step_context.end_dialog()

        mensagens = []
        for produto in produtos[:3]:  # Mostra no máximo 3 resultados
            mensagens.append(
                f"🔍 Produto:\n"
                f"🆔 ID: {produto.get('id')}\n"
                f"📦 Nome: {produto.get('productName')}\n"
                f"💰 Preço: R$ {produto.get('price')}\n"
                f"📄 Descrição: {produto.get('productDescription')}\n"
                f"----------------------"
            )
        await step_context.context.send_activity(MessageFactory.text("\n\n".join(mensagens)))

        return await step_context.end_dialog()

