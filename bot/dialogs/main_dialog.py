from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory
from services.product_api import ProductAPI
from dialogs.consultar_produtos_dialog import ConsultarProdutoDialog
from dialogs.purchase_dialog import PurchaseDialog  # ✅ NOVO

class MainDialog(ComponentDialog):
    def __init__(self):
        super().__init__("MainDialog")
        self.product_api = ProductAPI()  

        self.add_dialog(ChoicePrompt("ChoicePrompt"))
        self.add_dialog(TextPrompt("TextPrompt"))

        self.add_dialog(ConsultarProdutoDialog(self.product_api))
        self.add_dialog(PurchaseDialog())  

        self.add_dialog(
            WaterfallDialog(
                "MainWaterfallDialog",
                [
                    self.prompt_option_step,
                    self.process_option_step,
                    self.final_step,
                ],
            )
        )
        self.initial_dialog_id = "MainWaterfallDialog"

    async def prompt_option_step(self, step_context: WaterfallStepContext):
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Escolha a opção desejada:"),
                choices=[
                    Choice("Consultar Produtos"),
                    Choice("Comprar Produtos")  
                ],
            ),
        )

    async def process_option_step(self, step_context: WaterfallStepContext):
        choice = step_context.result.value
        if choice == "Consultar Produtos":
            return await step_context.begin_dialog("ConsultarProdutoDialog")
        elif choice == "Comprar Produtos":  
            return await step_context.begin_dialog("PurchaseDialog")

    async def final_step(self, step_context: WaterfallStepContext):
        if step_context.result == "retornar_ao_menu":
            return await step_context.replace_dialog(self.initial_dialog_id)
        return await step_context.end_dialog()

