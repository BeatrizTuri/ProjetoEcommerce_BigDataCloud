from azure.cosmos import CosmosClient, exceptions
import os
from pytest import Session
from app.core.cosmos_db import get_cosmos_container
from app.services.cosmos_pedido import create_pedido
from app.services.cosmos_product import obter_produto_por_id

COSMOS_DB_URI = os.getenv("AZURE_COSMOS_URI")
COSMOS_DB_KEY = os.getenv("AZURE_COSMOS_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOS_DATABASE")
AZURE_COSMOS_CONTAINER_CARRINHO = os.getenv("AZURE_COSMOS_CONTAINER_CARRINHO")

_cart_container = None

def get_cart_container():
    global _cart_container
    if _cart_container is None:
        client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
        database = client.create_database_if_not_exists(DATABASE_NAME)
        _cart_container = get_cosmos_container(database, AZURE_COSMOS_CONTAINER_CARRINHO, partition_path="/id_usuario")
    return _cart_container


def get_cart(id_usuario: str) -> dict:
    container = get_cart_container()
    try:
        cart = container.read_item(item=id_usuario, partition_key=id_usuario)
    except exceptions.CosmosResourceNotFoundError:
        cart = {"id_usuario": id_usuario, "produtos": []}

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
    container = get_cart_container()
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
    cart = {"id_usuario": id_usuario, "produtos": []}
    save_cart(cart)
    return cart


def finalize_cart(id_usuario: str, db: Session):
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
