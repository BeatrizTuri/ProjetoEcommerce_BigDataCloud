from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext,
    DialogTurnResult, TextPrompt, PromptOptions
)
from botbuilder.core import MessageFactory
from services.product_api import ProductAPI
from datetime import datetime
class ConsultarPedidoDialog(ComponentDialog):
    def __init__(self, product_api: ProductAPI):
        super().__init__("ConsultarPedidoDialog")
        self.product_api = product_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "ConsultarPedidoWaterfallDialog",
                [
                    self.get_user_id_step,
                    self.show_extrato_step,
                ],
            )
        )

        self.initial_dialog_id = "ConsultarPedidoWaterfallDialog"

    async def get_user_id_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Digite o CPF do usuário para ver a consulta de pedidos:"))
        )

    async def show_extrato_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        cpf = step_context.result
        extrato = self.product_api.consultar_pedido_por_cpf(cpf)

        if not extrato:
            await step_context.context.send_activity("❌ Nenhum pedido encontrado. Verifique o ID digitado.")
            return await step_context.replace_dialog(self.id)
        
        else:
            mensagens = []
            total_geral = 0
            for pedido in extrato:
                valor = float(pedido.get("valor_total", 0))
                total_geral += valor

                data_str = pedido['produtos'][0].get('data')
                try:
                    data_formatada = datetime.fromisoformat(data_str).strftime("%Y-%m-%d %H:%M")
                except:
                    data_formatada = "Data inválida"
                
                mensagens.append(
                    f"🔍 *Pedido*: {pedido.get('id')}\n\n"
                    f"*Valor*: R$ {valor:.2f}\n\n"
                    f"*Data do Pedido*: {data_formatada}\n\n\n"
                )
            
        mensagens.append(f"\n **Total**: R$ {total_geral:.2f}")
        await step_context.context.send_activity(MessageFactory.text("\n".join(mensagens)))

        return await step_context.end_dialog("retornar_ao_menu")
