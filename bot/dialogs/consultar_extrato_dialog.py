from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext,
    DialogTurnResult, TextPrompt, PromptOptions
)
from botbuilder.core import MessageFactory
from services.product_api import ProductAPI

class ConsultarExtratoDialog(ComponentDialog):
    def __init__(self, product_api: ProductAPI):
        super().__init__("ConsultarExtratoDialog")
        self.product_api = product_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "ConsultarExtratoWaterfallDialog",
                [
                    self.get_user_id_step,
                    self.show_extrato_step
                ],
            )
        )

        self.initial_dialog_id = "ConsultarExtratoWaterfallDialog"

    async def get_user_id_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Digite o ID do usuário para ver o extrato de compras:"))
        )

    async def show_extrato_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        usuario_id = step_context.result
        extrato = self.product_api.consultar_extrato_compras(usuario_id)

        if not extrato:
            await step_context.context.send_activity("❌ Nenhum extrato encontrado. Verifique o ID digitado.")
        else:
            mensagens = []
            for pedido in extrato:
                mensagens.append(
                    f"🛒 Pedido: {pedido.get('id')} | 💰 Total: R$ {pedido.get('valor_total')} | 📅 Data: {pedido.get('data')}"
                )
            await step_context.context.send_activity("\n".join(mensagens))

        return await step_context.end_dialog("retornar_ao_menu")
