import requests
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions

class ConsultarProdutoDialog(ComponentDialog):
    def __init__(self):
        super(ConsultarProdutoDialog, self).__init__("ConsultarProdutoDialog")

        self.add_dialog(TextPrompt(TextPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "consultarProdutoWaterfallDialog",
                [
                    self.product_id_step,
                    self.process_product_id_step,
                ],
            )
        )

        self.initial_dialog_id = "consultarProdutoWaterfallDialog"

    async def product_id_step(self, step_context: WaterfallStepContext):
        prompt_message = MessageFactory.text("Digite o ID do produto que deseja consultar:")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=prompt_message)
        )

    async def process_product_id_step(self, step_context: WaterfallStepContext):
        produto_id = step_context.result

        # URL da API
        base_url = "http://localhost:8000/produtos"  # substitua pelo endereço real da sua API se necessário
        endpoint = f"{base_url}/{produto_id}"

        try:
            response = requests.get(endpoint)

            if response.status_code == 200:
                produto = response.json()
                resposta = (
                    f"🔍 Produto encontrado:\n\n"
                    f"🆔 ID: {produto.get('id')}\n"
                    f"📦 Nome: {produto.get('productName')}\n"
                    f"💰 Preço: R$ {produto.get('price')}\n"
                    f"📄 Descrição: {produto.get('productDescription')}\n"
                )
            elif response.status_code == 404:
                resposta = "❌ Produto não encontrado. Verifique o ID e tente novamente."
            else:
                resposta = f"⚠️ Erro ao consultar produto: {response.status_code}"

        except Exception as e:
            resposta = f"❌ Erro ao conectar com o serviço: {str(e)}"

        await step_context.context.send_activity(MessageFactory.text(resposta))
        return await step_context.end_dialog()
