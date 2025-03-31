from azure.cosmos import CosmosClient, exceptions
import os
from pytest import Session
from app.core.cosmos_db import get_cosmos_container
from app.services.cosmos_pedido import create_pedido
from app.services.cosmos_product import get_product_by_id

COSMOS_DB_URI = os.getenv("AZURE_COSMOS_URI")
COSMOS_DB_KEY = os.getenv("AZURE_COSMOS_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOS_DATABASE")
CART_CONTAINER_NAME = os.getenv("AZURE_COSMOS_CONTAINER_CARRINHO", "carrinhos")

client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
database = client.create_database_if_not_exists(DATABASE_NAME)
cart_container = get_cosmos_container(database, CART_CONTAINER_NAME, partition_path="/id_usuario")

def get_cart(id_usuario):
    try:
        return cart_container.read_item(item=id_usuario, partition_key=id_usuario)
    except exceptions.CosmosResourceNotFoundError:
        return {"id_usuario": id_usuario, "produtos": []}

def save_cart(cart):
    if "id" not in cart:
        cart["id"] = cart["id_usuario"]
    cart_container.upsert_item(cart)


def add_to_cart(id_usuario: str, item: dict):
    cart = get_cart(id_usuario)
    produtos = cart.get("produtos", [])
    for prod in produtos:
        if prod["id_produto"] == item["id_produto"]:
            prod["quantidade"] += item["quantidade"]
            break
    else:
        produto_info = get_product_by_id(item["id_produto"])
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
