from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext,
    DialogTurnResult, TextPrompt, ChoicePrompt, PromptOptions
)
from botbuilder.dialogs.choices import Choice, ListStyle
from botbuilder.core import MessageFactory
from datetime import datetime, timedelta

from services.extrato_api import ExtratoAPI

class ConsultarExtratoDialog(ComponentDialog):
    def __init__(self, extrato_api: ExtratoAPI):
        super().__init__("ConsultarExtratoDialog")
        self.extrato_api = extrato_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "ConsultarExtratoWaterfallDialog",
                [
                    self.get_cpf_step,
                    self.get_periodo_step,
                    self.show_extrato_step,
                ],
            )
        )
        self.initial_dialog_id = "ConsultarExtratoWaterfallDialog"

    async def get_cpf_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Digite o CPF do usuário para consultar o extrato:"))
        )

    async def get_periodo_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["cpf"] = step_context.result
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Selecione o período para o extrato:"),
                choices=[
                    Choice("Última semana"),
                    Choice("Último mês"),
                    Choice("Últimos 6 meses"),
                    Choice("Todos")
                ],
                style=ListStyle.hero_card
            )
        )

    async def show_extrato_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        cpf = step_context.values["cpf"]
        periodo = step_context.result.value

        # Calcula a data inicial conforme o período escolhido
        data_inicio = None
        if periodo == "Última semana":
            data_inicio = datetime.now() - timedelta(weeks=1)
        elif periodo == "Último mês":
            data_inicio = datetime.now() - timedelta(days=30)
        elif periodo == "Últimos 6 meses":
            data_inicio = datetime.now() - timedelta(days=180)

        extrato = self.extrato_api.consultar_extrato_cartoes_por_cpf(cpf)

        if not extrato:
            await step_context.context.send_activity("❌ Nenhum extrato encontrado para este CPF.")
            return await step_context.end_dialog("retornar_ao_menu")

        mensagens = []
        total_geral = 0

        for cartao in extrato:
            pedidos = cartao["pedidos"]
            if data_inicio:
                pedidos = [
                    p for p in pedidos
                    if "data_pedido" in p and datetime.fromisoformat(p["data_pedido"]) >= data_inicio
                ]
            if not pedidos:
                continue

            subtotal = sum(float(p.get("valor_total", 0)) for p in pedidos)
            total_geral += subtotal

            mensagens.append(
                f"💳 Cartão final: {cartao['numero_final']}\n\n"
                f"(Validade: {cartao['validade']})\n\n"
                f"Pedidos: {len(pedidos)}\n\n"
                f"Total: R$ {subtotal:.2f}\n"
                f"{'-'*30}"
            )

        mensagens.append(f"\n**Total geral do extrato:** R$ {total_geral:.2f}")
        await step_context.context.send_activity(MessageFactory.text("\n".join(mensagens)))
        return await step_context.end_dialog("retornar_ao_menu")