from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice,ListStyle
from botbuilder.core import MessageFactory
from services.product_api import ProductAPI
from services.pedido_api import PedidoAPI
from dialogs.consultar_produtos_dialog import ConsultarProdutoDialog
from dialogs.consultar_pedido_dialog import ConsultarPedidoDialog

class MainDialog(ComponentDialog):
    def __init__(self):
        super().__init__("MainDialog")
        self.product_api = ProductAPI()  # Instancia a API uma vez
        self.pedido_api = PedidoAPI()

        self.add_dialog(ChoicePrompt("ChoicePrompt"))

        self.add_dialog(TextPrompt("TextPrompt"))
        # Passa a instância ao criar o diálogo
        self.add_dialog(ConsultarProdutoDialog(self.product_api))
        self.add_dialog(ConsultarPedidoDialog(self.pedido_api))

        self.add_dialog(
            WaterfallDialog(
                "MainWaterfallDialog",
                [
                    self.prompt_option_step,
                    self.process_option_step,
                    self.final_step,  # novo passo
                ],
            )
        )
        self.initial_dialog_id = "MainWaterfallDialog"

    async def prompt_option_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            "ChoicePrompt",
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Consultar Produtos"),
                    Choice("Ver Consulta de Pedidos")
                ],
                style=ListStyle.hero_card  # agora sim, botão tipo HeroCard
        ),
    )


    async def process_option_step(self, step_context: WaterfallStepContext):
        choice = step_context.result.value
        if choice == "Consultar Produtos":
            return await step_context.begin_dialog("ConsultarProdutoDialog")
        if choice == "Ver Consulta de Pedidos":
            return await step_context.begin_dialog("ConsultarPedidoDialog")
        
    async def final_step(self, step_context: WaterfallStepContext):
        if step_context.result == "retornar_ao_menu":
            # Reinicia o diálogo principal para mostrar o menu novamente
            return await step_context.replace_dialog(self.initial_dialog_id)
        
        # Caso nenhum retorno especial, apenas encerra o diálogo
        return await step_context.end_dialog()



