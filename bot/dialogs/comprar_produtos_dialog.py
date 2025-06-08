from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext,
    DialogTurnResult, TextPrompt, ConfirmPrompt, PromptOptions, ChoicePrompt, DialogTurnStatus
)
from botbuilder.schema import HeroCard, CardAction, ActionTypes, Attachment
from botbuilder.core import MessageFactory
from botbuilder.dialogs.choices import Choice
from services.product_api import ProductAPI
from services.extrato_api import ExtratoAPI
from services.compra_api import CompraAPI

class CompraDialog(ComponentDialog):
    def __init__(self, product_api: ProductAPI, extrato_api: ExtratoAPI, compra_api: CompraAPI):
        super().__init__("CompraDialog")
        self.product_api = product_api
        self.extrato_api = extrato_api
        self.compra_api = compra_api

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "CompraWaterfallDialog",
                [
                    self.get_cpf_step,
                    self.get_produto_step,
                    self.escolher_produto_step,  # Novo passo para escolher produto
                    self.get_quantidade_step,
                    self.add_to_cart_step,
                    self.ask_add_more_step,
                    self.loop_or_cvv_step,
                    self.get_cvv_step,
                    self.finalizar_compra_step,
                ],
            )
        )
        self.initial_dialog_id = "CompraWaterfallDialog"

    async def get_cpf_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        cpf = None
        if step_context.options and "cpf" in step_context.options:
            cpf = step_context.options["cpf"]
        if cpf:
            step_context.values["cpf"] = cpf
            # Avança para o próximo passo do Waterfall (get_produto_step)
            return await step_context.next(None)
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Digite o CPF do usuário para iniciar a compra:"))
        )

    async def get_produto_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if "cpf" not in step_context.values and step_context.result:
            step_context.values["cpf"] = step_context.result
            # Só pede o produto após salvar o CPF
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Qual produto deseja comprar? (Digite parte do nome)"))
            )
        # Se já tem CPF, sempre pede o produto
        if "cpf" in step_context.values:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Qual produto deseja comprar? (Digite parte do nome)"))
            )
    
    async def escolher_produto_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        nome_produto = step_context.result
        produtos = self.product_api.consultar_produtos(nome_produto)
        if not produtos:
            await step_context.context.send_activity("Nenhum produto encontrado com esse nome.")
            return await step_context.end_dialog()

        # Monta os Hero Cards
        attachments = []
        for p in produtos[:5]:
            card = HeroCard(
                title=p.get("productName", "Sem nome"),
                subtitle=f"R$ {p.get('price', '0.00')}",
                text=p.get("productDescription", "Sem descrição"),
                buttons=[
                    CardAction(
                        type=ActionTypes.im_back,
                        title="Selecionar",
                        value=p["id"]
                    )
                ]
            )
            attachments.append(Attachment(content_type="application/vnd.microsoft.card.hero", content=card))

        await step_context.context.send_activity(
            MessageFactory.carousel(attachments, "Produtos encontrados:")
        )

        step_context.values["produtos_encontrados"] = produtos
        # Agora, aguarda o usuário clicar em um botão (que envia o id do produto)
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Clique em 'Selecionar' no produto desejado ou digite o ID do produto:"))
        )
    async def get_quantidade_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        produto_id = step_context.result.strip()
        produtos = step_context.values["produtos_encontrados"]
        produto = next((p for p in produtos if p["id"] == produto_id), None)
        if not produto:
            await step_context.context.send_activity("Produto não encontrado na lista.")
            return await step_context.end_dialog()
        step_context.values["produto"] = produto

        mensagem = (
            f"Produto selecionado:\n"
            f"Nome: {produto['productName']}\n"
            f"Preço: R$ {produto['price']}\n"
            f"Descrição: {produto.get('productDescription', 'Sem descrição')}"
        )
        await step_context.context.send_activity(mensagem)

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Qual a quantidade?"))
        )
    async def add_to_cart_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["quantidade"] = int(step_context.result)
        # Busca usuário pelo CPF para obter id_usuario
        cpf = step_context.values["cpf"]
        usuario = self.extrato_api.buscar_usuario_por_cpf(cpf)
        if not usuario:
            await step_context.context.send_activity("Usuário não encontrado.")
            return await step_context.end_dialog()
        id_usuario = usuario["id_usuario"]
        step_context.values["id_usuario"] = id_usuario

        # Busca produto
        produto = step_context.values["produto"]

        # Adiciona ao carrinho
        item = {
            "id_produto": produto["id"],
            "quantidade": step_context.values["quantidade"]
        }
        self.compra_api.adicionar_ao_carrinho(id_usuario, item)
        await step_context.context.send_activity(f"Produto '{produto['productName']}' adicionado ao carrinho.")

        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Deseja adicionar mais produtos?"))
        )

    async def ask_add_more_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            # Reinicia o diálogo, mas mantém o CPF já preenchido
            cpf = step_context.values["cpf"]
            return await step_context.replace_dialog(self.id, {"cpf": cpf})
        return await step_context.next(None)

    async def loop_or_cvv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Digite o CVV do cartão para finalizar (ou deixe em branco para usar o cartão padrão):"))
        )

    async def get_cvv_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["cvv"] = step_context.result.strip() if step_context.result else None
        return await step_context.next(None)

    async def finalizar_compra_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        id_usuario = step_context.values["id_usuario"]
        cvv = step_context.values["cvv"]
        pedido = self.compra_api.finalizar_carrinho(id_usuario, cvv)
        if not pedido:
            await step_context.context.send_activity("Erro ao finalizar a compra.")
            return await step_context.end_dialog()
        resumo = f"Compra finalizada!\n\nValor total: R$ {pedido['valor_total']:.2f}\n\nStatus: {pedido['status']}"
        await step_context.context.send_activity(resumo)
        return await step_context.end_dialog("retornar_ao_menu")