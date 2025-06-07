from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext,
    DialogTurnResult, TextPrompt, PromptOptions
)
from botbuilder.core import MessageFactory
from services.pedido_api import PedidoAPI
from datetime import datetime

class ConsultarPedidoPorIdDialog(ComponentDialog):
    def __init__(self, pedido_api: PedidoAPI):
        super().__init__("ConsultarPedidoPorIdDialog")
        self.pedido_api = pedido_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "ConsultarPedidoPorIdWaterfallDialog",
                [
                    self.get_pedido_id_step,
                    self.show_pedido_step,
                ],
            )
        )

        self.initial_dialog_id = "ConsultarPedidoPorIdWaterfallDialog"

    async def get_pedido_id_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Digite o ID do pedido que deseja consultar:"))
        )

    async def show_pedido_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        pedido_id = step_context.result
        pedido = self.pedido_api.consultar_pedido_por_id(pedido_id)

        if not pedido:
            await step_context.context.send_activity("❌ Pedido não encontrado. Verifique o ID.")
            return await step_context.replace_dialog(self.id)

        valor = float(pedido.get("valor_total", 0))
        data_str = pedido['produtos'][0].get('data')
        try:
            data_formatada = datetime.fromisoformat(data_str).strftime("%Y-%m-%d %H:%M")
        except:
            data_formatada = "Data inválida"

        mensagem = (
            f"🔍 *Pedido*: {pedido.get('id')}\n\n"
            f" *Nome*: {pedido['produtos'][0].get('nome')}\n\n"
            f" *Quantidade*: {pedido['produtos'][0].get('quantidade')}\n\n"
            f" *Valor*: R$ {valor:.2f}\n\n"
            f" *Data*: {data_formatada}\n\n"
        )
        await step_context.context.send_activity(MessageFactory.text(mensagem))

        return await step_context.end_dialog("retornar_ao_menu")
