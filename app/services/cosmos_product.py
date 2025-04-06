from azure.cosmos import CosmosClient, PartitionKey, exceptions
from app.core.cosmos_db import COSMOS_URI, COSMOS_KEY, COSMOS_DATABASE, COSMOS_CONTAINER_PRODUTOS

client = CosmosClient(COSMOS_URI, COSMOS_KEY)
database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER_PRODUTOS,
    partition_key=PartitionKey(path="/id")
)

def criar_produto(produto: dict) -> dict:
    return container.create_item(body=produto)

def listar_produtos() -> list:
    consulta = "SELECT * FROM produtos"
    itens = list(container.query_items(
        query=consulta,
        enable_cross_partition_query=True
    ))
    return itens

def obter_produto_por_id(produto_id: str) -> dict:
    try:
        return container.read_item(item=produto_id, partition_key=produto_id)
    except exceptions.CosmosResourceNotFoundError:
        return None

def deletar_produto_por_id(produto_id: str) -> None:
    container.delete_item(item=produto_id, partition_key=produto_id)
    
def atualizar_produto(produto_id: str, produto_dict: dict) -> dict:
    try:
        
        produto_dict['id'] = produto_id 
        container.upsert_item(body=produto_dict) 
        return produto_dict
    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Erro ao atualizar o produto no Cosmos DB: {str(e)}")
