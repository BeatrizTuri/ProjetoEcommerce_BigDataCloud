from azure.cosmos import CosmosClient, exceptions
import os
import uuid
from app.services.cosmos_product import get_product_by_id  

# Configurações do Cosmos DB
COSMOS_DB_URI = os.getenv("AZURE_COSMOS_URI")
COSMOS_DB_KEY = os.getenv("AZURE_COSMOS_KEY")
DATABASE_NAME = os.getenv("AZURE_COSMOS_DATABASE")
CONTAINER_NAME = os.getenv("AZURE_COSMOS_CONTAINER_PEDIDOS")

client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_KEY)
database = client.create_database_if_not_exists(DATABASE_NAME)
container = database.create_container_if_not_exists(id=CONTAINER_NAME, partition_key="/id")

def create_pedido(pedido: dict):
    pedido_id = pedido.get("id", str(uuid.uuid4()))
    
    produtos_final = []
    valor_total = 0

    for item in pedido["produtos"]:
        produto_info = get_product_by_id(item["id_produto"])

        if not produto_info:
            raise Exception(f"Produto {item['id_produto']} não encontrado.")

        preco_unitario = produto_info["price"]
        subtotal = preco_unitario * item["quantidade"]

        produtos_final.append({
            "id_produto": item["id_produto"],
            "quantidade": item["quantidade"],
            "categoria": produto_info["productCategory"],
            "preco_unitario": preco_unitario
        })

        valor_total += subtotal

    pedido_completo = {
        "id": pedido_id,
        "id_usuario": pedido["id_usuario"],
        "produtos": produtos_final,
        "valor_total": valor_total,
        "status": "pendente"
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
