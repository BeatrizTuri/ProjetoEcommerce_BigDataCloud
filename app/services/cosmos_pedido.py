from datetime import datetime
from azure.cosmos import exceptions
import uuid
from decimal import Decimal

from app.services.cosmos_product import obter_produto_por_id
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario

from app.core.cosmos_db import (
    get_cosmos_client,
    get_cosmos_database,
    get_cosmos_container,
    COSMOS_CONTAINER_PEDIDOS
)

client = get_cosmos_client()
database = get_cosmos_database(client)
container = get_cosmos_container(database, COSMOS_CONTAINER_PEDIDOS)

def create_pedido(pedido: dict, db):
    pedido_id = pedido.get("id", str(uuid.uuid4()))
    produtos_final = []
    valor_total = Decimal("0.0")
    data_pedido = datetime.now()

    usuario = db.query(Usuario).filter(Usuario.id == pedido["id_usuario"]).first()
    if not usuario:
        raise Exception("Usuário não encontrado.")

    cartao = db.query(CartaoCredito).filter(CartaoCredito.id_usuario_cartao == pedido["id_usuario"]).first()
    if not cartao:
        raise Exception("Cartão de crédito do usuário não encontrado.")

    for item in pedido["produtos"]:
        produto_info = obter_produto_por_id(item["id_produto"])
        if not produto_info:
            raise Exception(f"Produto {item['id_produto']} não encontrado.")

        preco_unitario = Decimal(str(produto_info["price"]))
        subtotal = preco_unitario * item["quantidade"]

        produtos_final.append({
            "id_produto": item["id_produto"],
            "quantidade": item["quantidade"],
            "categoria": produto_info["productCategory"],
            "preco_unitario": float(preco_unitario),
            "data": data_pedido.isoformat()
        })

        valor_total += subtotal

    if cartao.saldo < valor_total:
        raise Exception("Saldo insuficiente no cartão de crédito.")

    cartao.saldo -= valor_total
    db.commit()

    pedido_completo = {
        "id": pedido_id,
        "id_usuario": pedido["id_usuario"],
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
    return list(container.read_all_items())

def delete_pedido_by_id(id: str):
    container.delete_item(item=id, partition_key=id)
