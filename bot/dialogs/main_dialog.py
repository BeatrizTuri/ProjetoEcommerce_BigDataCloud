from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory
from services.product_api import ProductAPI
from dialogs.consultar_produtos_dialog import ConsultarProdutoDialog
from dialogs.consultar_extrato_dialog import ConsultarExtratoDialog

class MainDialog(ComponentDialog):
    def __init__(self):
        super().__init__("MainDialog")
        self.product_api = ProductAPI()  # Instancia a API uma vez

        self.add_dialog(ChoicePrompt("ChoicePrompt"))

        self.add_dialog(TextPrompt("TextPrompt"))
        # Passa a instância ao criar o diálogo
        self.add_dialog(ConsultarProdutoDialog(self.product_api))
        self.add_dialog(ConsultarExtratoDialog(self.product_api))

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
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[Choice("Consultar Produtos"),
                    Choice("Ver Extrato de Compra")],
            ),
        )

    async def process_option_step(self, step_context: WaterfallStepContext):
        choice = step_context.result.value
        if choice == "Consultar Produtos":
            return await step_context.begin_dialog("ConsultarProdutoDialog")
        if choice == "Ver Extrato de Compra":
            return await step_context.begin_dialog("ConsultarExtratoDialog")
        
    async def final_step(self, step_context: WaterfallStepContext):
        if step_context.result == "retornar_ao_menu":
            # Reinicia o diálogo principal para mostrar o menu novamente
            return await step_context.replace_dialog(self.initial_dialog_id)
        
        # Caso nenhum retorno especial, apenas encerra o diálogo
        return await step_context.end_dialog()



