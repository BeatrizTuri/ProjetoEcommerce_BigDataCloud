from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice,ListStyle
from botbuilder.core import MessageFactory
from services.extrato_api import ExtratoAPI
from services.product_api import ProductAPI
from services.pedido_api import PedidoAPI
from services.compra_api import CompraAPI
from dialogs.consultar_produtos_dialog import ConsultarProdutoDialog
from dialogs.consultar_pedido_dialog import ConsultarPedidoDialog
from dialogs.consultar_extrato_compras import ConsultarExtratoDialog
from dialogs.consultar_pedido_por_id_dialog import ConsultarPedidoPorIdDialog
from dialogs.comprar_produtos_dialog import CompraDialog
from dialogs.consultar_todos_produtos import ConsultarTodosProdutosDialog

class MainDialog(ComponentDialog):
    def __init__(self):
        super().__init__("MainDialog")
        self.product_api = ProductAPI()  # Instancia a API uma vez
        self.pedido_api = PedidoAPI()
        self.extrato_api = ExtratoAPI()
        self.compra_api = CompraAPI()

        self.add_dialog(ChoicePrompt("ChoicePrompt"))

        self.add_dialog(TextPrompt("TextPrompt"))
        # Passa a instância ao criar o diálogo
        self.add_dialog(ConsultarProdutoDialog(self.product_api))
        self.add_dialog(ConsultarPedidoDialog(self.pedido_api))
        self.add_dialog(ConsultarExtratoDialog(self.extrato_api))
        self.add_dialog(ConsultarPedidoPorIdDialog(self.pedido_api))
        self.add_dialog(CompraDialog(self.product_api, self.extrato_api, self.compra_api))
        self.add_dialog(ConsultarTodosProdutosDialog(self.product_api))
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
                    Choice("Ver Consulta de Pedidos"),
                    Choice("Extrato de Compras"),
                    Choice("Consultar Pedido por ID"),
                    Choice("Comprar Produtos"),
                    Choice("Consultar Todos Produtos"),
                ],
                style=ListStyle.hero_card
        ),
    )


    async def process_option_step(self, step_context: WaterfallStepContext):
        choice = step_context.result.value
        if choice == "Consultar Produtos":
            return await step_context.begin_dialog("ConsultarProdutoDialog")
        if choice == "Ver Consulta de Pedidos":
            return await step_context.begin_dialog("ConsultarPedidoDialog")
        if choice == "Extrato de Compras":
            return await step_context.begin_dialog("ConsultarExtratoDialog")
        if choice == "Consultar Pedido por ID":
            return await step_context.begin_dialog("ConsultarPedidoPorIdDialog")
        if choice == "Comprar Produtos":
            return await step_context.begin_dialog("CompraDialog")
        if choice == "Consultar Todos Produtos":
            return await step_context.begin_dialog("ConsultarTodosProdutosDialog")
        
    async def final_step(self, step_context: WaterfallStepContext):
        if step_context.result == "retornar_ao_menu":
            # Reinicia o diálogo principal para mostrar o menu novamente
            return await step_context.replace_dialog(self.initial_dialog_id)
        
        # Caso nenhum retorno especial, apenas encerra o diálogo
        return await step_context.end_dialog()



