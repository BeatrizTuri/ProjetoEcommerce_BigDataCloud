from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    ChoicePrompt,
    PromptOptions
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory

from services.product_api import ProductAPI
from services.cart_api import CartAPI
from services.user_api import UserAPI
from services.card_api import CardAPI
from services.order_api import OrderAPI



class PurchaseDialog(ComponentDialog):
    def __init__(self):
        super().__init__("PurchaseDialog")

        # Prompts
        self.add_dialog(TextPrompt("ProdutoNomePrompt"))
        self.add_dialog(TextPrompt("EscolhaProdutoPrompt"))
        self.add_dialog(TextPrompt("QuantidadePrompt"))
        self.add_dialog(TextPrompt("ContinuarPrompt"))
        self.add_dialog(TextPrompt("CpfPrompt"))
        self.add_dialog(ChoicePrompt("EscolhaCartaoPrompt"))

        self.add_dialog(WaterfallDialog("MainFlow", [
            self.perguntar_nome_produto,
            self.buscar_produto_e_exibir_opcoes,
            self.perguntar_quantidade,
            self.adicionar_ao_carrinho,
            self.perguntar_se_deseja_continuar,
            self.perguntar_cpf,
            self.validar_usuario_e_listar_cartoes,
            self.confirmar_finalizacao
        ]))

        self.initial_dialog_id = "MainFlow"

    async def perguntar_nome_produto(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            "ProdutoNomePrompt",
            PromptOptions(prompt=MessageFactory.text("Qual produto você deseja comprar?"))
        )

    async def buscar_produto_e_exibir_opcoes(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        termo_busca = step_context.result
        step_context.values["termo_produto"] = termo_busca
        produtos = ProductAPI().consultar_produtos(termo_busca)

        if not produtos:
            await step_context.context.send_activity("Nenhum produto encontrado com esse nome. Tente novamente.")
            return await step_context.replace_dialog("PurchaseDialog")

        step_context.values["produtos_encontrados"] = produtos

        if len(produtos) == 1:
            step_context.values["produto_escolhido"] = produtos[0]
            return await step_context.next(None)

        opcoes_texto = "\n".join([f"{i + 1}. {p['nome']} (R${p['preco']:.2f})" for i, p in enumerate(produtos)])
        prompt_text = f"Encontrei vários produtos. Qual você deseja?\n{opcoes_texto}\n\nDigite o número correspondente."
        return await step_context.prompt("EscolhaProdutoPrompt", PromptOptions(prompt=MessageFactory.text(prompt_text)))

    async def perguntar_quantidade(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if "produto_escolhido" not in step_context.values:
            produtos = step_context.values["produtos_encontrados"]
            try:
                indice = int(step_context.result) - 1
                step_context.values["produto_escolhido"] = produtos[indice]
            except:
                await step_context.context.send_activity("Escolha inválida. Recomeçando...")
                return await step_context.replace_dialog("PurchaseDialog")

        return await step_context.prompt(
            "QuantidadePrompt",
            PromptOptions(prompt=MessageFactory.text("Quantos desse produto você quer?"))
        )

    async def adicionar_ao_carrinho(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        produto = step_context.values["produto_escolhido"]
        quantidade = step_context.result

        # Usa o id_usuario se já tiver sido coletado, senão "tmp-user"
        id_usuario = step_context.values.get("id_usuario", "tmp-user")

        try:
            CartAPI().adicionar_ao_carrinho(id_usuario, produto["id"], int(quantidade))
            await step_context.context.send_activity(
                MessageFactory.text(f"✅ {quantidade}x '{produto['nome']}' foram adicionados ao seu carrinho!")
            )
        except Exception as e:
            await step_context.context.send_activity(f"❌ Erro ao adicionar ao carrinho: {str(e)}")

        return await step_context.next(None)

    async def perguntar_se_deseja_continuar(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            "ContinuarPrompt",
            PromptOptions(prompt=MessageFactory.text("Deseja adicionar mais algum produto? (sim/não)"))
        )

    async def perguntar_cpf(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            "CpfPrompt",
            PromptOptions(prompt=MessageFactory.text("Por favor, informe seu CPF para finalizar a compra:"))
        )

    async def validar_usuario_e_listar_cartoes(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        cpf = step_context.result
        usuario = UserAPI().buscar_usuario_por_cpf(cpf)

        if not usuario:
            await step_context.context.send_activity("❌ CPF não encontrado. Você precisa estar cadastrado.")
            return await step_context.end_dialog()

        step_context.values["id_usuario"] = usuario["id"]

        cartoes = CardAPI().listar_cartoes_por_usuario(usuario["id"])
        if not cartoes:
            await step_context.context.send_activity("⚠️ Nenhum cartão encontrado. Cadastre um cartão na sua conta.")
            return await step_context.end_dialog()

        opcoes = [
            Choice(f"Cartão final {c['numero'][-4:]}", value=c["id"])
            for c in cartoes
        ]
        step_context.values["cartoes_disponiveis"] = {c["id"]: c for c in cartoes}

        return await step_context.prompt(
            "EscolhaCartaoPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Qual cartão deseja usar para finalizar a compra?"),
                choices=opcoes
            )
        )

    async def confirmar_finalizacao(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        id_cartao = step_context.result.value
        id_usuario = step_context.values["id_usuario"]

        try:
            pedido = OrderAPI().finalizar_pedido(id_usuario=id_usuario, id_cartao=id_cartao)
            await step_context.context.send_activity(f"✅ Pedido finalizado com sucesso! Número do pedido: {pedido['id']}")
        except Exception as e:
            await step_context.context.send_activity(f"❌ Erro ao finalizar o pedido: {str(e)}")

        return await step_context.end_dialog()
