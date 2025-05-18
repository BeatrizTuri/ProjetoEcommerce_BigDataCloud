from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from services.api_client import APIClient
from .consultar_produtos_dialog import ConsultarProdutoDialog  # ajuste o caminho conforme seu projeto

class MainDialog(ComponentDialog):
    def __init__(self):
        super(MainDialog, self).__init__("MainDialog")

        self.api_client = APIClient(base_url="http://localhost:8000")  # <== instância criada aqui

        self.add_dialog(TextPrompt("TextPrompt"))
        self.add_dialog(ConsultarProdutoDialog())

        self.add_dialog(
            WaterfallDialog(
                "MainWaterfallDialog",
                [
                    self.process_message_step,
                    self.after_consultar_produto_step,
                ],
            )
        )

        self.initial_dialog_id = "MainWaterfallDialog"

    async def process_message_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        texto = step_context.context.activity.text.lower()

        if "ver produtos" in texto:
            try:
                produtos = self.api_client.get_produtos()  # usa a instância
            except Exception as e:
                await step_context.context.send_activity(f"Erro ao buscar produtos: {str(e)}")
                return await step_context.end_dialog()

            if not produtos:
                await step_context.context.send_activity("Nenhum produto encontrado.")
            else:
                lista = "\n".join([f"- {p['productName']} (R$ {p['price']})" for p in produtos])
                await step_context.context.send_activity(f"🛒 Produtos disponíveis:\n{lista}")
            return await step_context.end_dialog()

        elif "consultar produto" in texto:
            # chama o diálogo ConsultarProdutoDialog
            return await step_context.begin_dialog("ConsultarProdutoDialog")

        elif "ajuda" in texto or "menu" in texto:
            ajuda = (
                "📋 Menu de opções:\n"
                "- ver produtos\n"
                "- consultar produto\n"
                "- status do pedido\n"
                "- checar carrinho\n"
                "- cadastrar produto\n"
                "- ajuda / menu"
            )
            await step_context.context.send_activity(ajuda)
            return await step_context.end_dialog()

        elif "status do pedido" in texto:
            await step_context.context.send_activity("🔄 Funcionalidade de status de pedido em construção.")
            return await step_context.end_dialog()

        else:
            await step_context.context.send_activity("❓ Não entendi. Digite 'menu' para ver as opções.")
            return await step_context.end_dialog()

    async def after_consultar_produto_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Pode adicionar lógica pós diálogo de produto, se desejar
        return await step_context.end_dialog()
