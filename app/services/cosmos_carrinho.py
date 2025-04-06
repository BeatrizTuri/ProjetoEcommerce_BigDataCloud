from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
from decimal import Decimal
from datetime import datetime
import uuid
from app.services.cosmos_product import obter_produto_por_id
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario

from app.core.cosmos_db import (
    COSMOS_URI,
    COSMOS_KEY,
    COSMOS_DATABASE,
    COSMOS_CONTAINER_CARRINHO
)

client = CosmosClient(COSMOS_URI, COSMOS_KEY)
database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER_CARRINHO,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

def get_cart(id_usuario: str) -> dict:
    try:
        cart = container.read_item(item=id_usuario, partition_key=id_usuario)
    except exceptions.CosmosResourceNotFoundError:
        cart = {"id": id_usuario, "id_usuario": id_usuario, "produtos": []}

    total = 0.0
    produtos_atualizados = []

    for item in cart.get("produtos", []):
        produto_info = obter_produto_por_id(item["id_produto"])
        if not produto_info:
            continue

        preco = produto_info.get("price", 0)
        subtotal = preco * item["quantidade"]

        produtos_atualizados.append({
            "id_produto": item["id_produto"],
            "quantidade": item["quantidade"],
            "categoria": item.get("categoria", produto_info.get("productCategory")),
            "preco_unitario": preco,
            "subtotal": subtotal
        })

        total += subtotal

    return {
        "id_usuario": id_usuario,
        "produtos": produtos_atualizados,
        "total": round(total, 2)
    }

def save_cart(cart):
    if "id" not in cart:
        cart["id"] = cart["id_usuario"]
    container.upsert_item(cart)

def add_to_cart(id_usuario: str, item: dict):
    cart = get_cart(id_usuario)
    produtos = cart.get("produtos", [])
    for prod in produtos:
        if prod["id_produto"] == item["id_produto"]:
            prod["quantidade"] += item["quantidade"]
            break
    else:
        produto_info = obter_produto_por_id(item["id_produto"])
        if not produto_info:
            raise Exception(f"Produto {item['id_produto']} não encontrado.")
        item["categoria"] = produto_info["productCategory"]
        produtos.append(item)

    cart["produtos"] = produtos
    save_cart(cart)
    return cart

def remove_from_cart(id_usuario: str, id_produto: str):
    cart = get_cart(id_usuario)
    cart["produtos"] = [p for p in cart["produtos"] if p["id_produto"] != id_produto]
    save_cart(cart)
    return cart

def clear_cart(id_usuario: str):
    cart = {"id": id_usuario, "id_usuario": id_usuario, "produtos": []}
    save_cart(cart)
    return cart

def finalize_cart(id_usuario: str, db):
    from app.services.cosmos_pedido import create_pedido
    cart = get_cart(id_usuario)

    if not cart["produtos"]:
        raise Exception("Carrinho está vazio.")

    pedido = {
        "id_usuario": id_usuario,
        "produtos": cart["produtos"]
    }

    pedido_finalizado = create_pedido(pedido, db=db)

    clear_cart(id_usuario)

    return pedido_finalizado
