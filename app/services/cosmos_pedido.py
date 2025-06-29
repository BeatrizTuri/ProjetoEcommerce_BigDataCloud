from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import uuid
from decimal import Decimal
from app.services.cosmos_product import obter_produto_por_id
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario
from app.utils.cartao_utils import autorizar_cartao_compra
from app.core.cosmos_db import (
    COSMOS_URI,
    COSMOS_KEY,
    COSMOS_DATABASE,
    COSMOS_CONTAINER_PEDIDOS
)

client = CosmosClient(COSMOS_URI, COSMOS_KEY)
database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER_PEDIDOS,
    partition_key=PartitionKey(path="/id")
)

def create_pedido(pedido: dict, db):
    pedido_id = pedido.get("id", str(uuid.uuid4()))
    produtos_final = []
    valor_total = Decimal("0.0")
    data_pedido = datetime.now()


    usuario = db.query(Usuario).filter(Usuario.id == pedido["id_usuario"]).first()
    if not usuario:
        raise Exception("Usuário não encontrado.")
    
    cvv = pedido.get("cvv")
    if cvv:
        cartao = db.query(CartaoCredito).filter(
            CartaoCredito.id_usuario_cartao == pedido["id_usuario"],
            CartaoCredito.cvv == cvv
        ).first()

        if not cartao:
            raise Exception("Cartão de crédito com o CVV informado não encontrado.")
    else:
        cartao = db.query(CartaoCredito).filter(
            CartaoCredito.id_usuario_cartao == pedido["id_usuario"]
        ).order_by(CartaoCredito.saldo.desc()).first()

        if not cartao:
            raise Exception("Nenhum cartão de crédito encontrado para o usuário.")
        

    for item in pedido["produtos"]:
        produto_info = obter_produto_por_id(item["id_produto"])
        if not produto_info:
            raise Exception(f"Produto {item['id_produto']} não encontrado.")

        preco_unitario = Decimal(str(produto_info["price"]))
        subtotal = preco_unitario * item["quantidade"]

        produtos_final.append({
            "id_produto": item["id_produto"],
            "nome": produto_info["productName"],
            "quantidade": item["quantidade"],
            "categoria": produto_info["productCategory"],
            "preco_unitario": float(preco_unitario),
            "data": data_pedido.isoformat()
        })

        valor_total += subtotal

    autorizado, mensagem = autorizar_cartao_compra(cartao, valor_total)
    if not autorizado:
        raise Exception(mensagem)

    cartao.saldo -= valor_total
    db.commit()

    pedido_completo = {
        "id": pedido_id,
        "id_usuario": pedido["id_usuario"],
        "id_cartao_utilizado": cartao.id, 
        "cartao_utilizado": {
            "numero_final": cartao.numero[-4:],
            "validade": cartao.dtExpiracao.strftime("%m/%Y")
        },
        "produtos": produtos_final,
        "valor_total": float(valor_total),
        "status": "confirmado",
        "data_pedido": data_pedido.isoformat()
    }

    container.create_item(body=pedido_completo)
    return pedido_completo

def get_pedido_by_id(id: str):
    try:
        return container.read_item(item=id, partition_key=id)
    except exceptions.CosmosResourceNotFoundError:
        return None

def list_pedidos():
    pedidos = list(container.read_all_items())
    for pedido in pedidos:
        pedido.pop("cvv", None)
    return pedidos

def delete_pedido_by_id(id: str):
    container.delete_item(item=id, partition_key=id)
    
def list_pedidos_por_usuario(usuario_id: str):
    query = f"SELECT * FROM c WHERE c.id_usuario = '{usuario_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return items

