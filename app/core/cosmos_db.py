import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Configurações do Cosmos DB
COSMOS_URI = os.getenv("AZURE_COSMOS_URI", "https://localhost:8081")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY", "C2y6yDjf5/R+ob0N8A7Cgv30VR==")
COSMOS_DATABASE = os.getenv("AZURE_COSMOS_DATABASE", "ecommerce")
# Container para produtos (padrão)
COSMOS_CONTAINER_PRODUTOS = os.getenv("AZURE_COSMOS_CONTAINER", "produtos")
# Novo container para pedidos
COSMOS_CONTAINER_PEDIDOS = os.getenv("AZURE_COSMOS_CONTAINER_PEDIDOS", "pedidos")
COSMOS_QUERY_METRICS_ENABLED = os.getenv("AZURE_COSMOS_QUERY_METRICS_ENABLED", "false").lower() == "true"
COSMOS_RESPONSE_DIAGNOSTICS_ENABLED = os.getenv("AZURE_COSMOS_RESPONSE_DIAGNOSTICS_ENABLED", "false").lower() == "true"

def get_cosmos_client():

    client = CosmosClient(COSMOS_URI, COSMOS_KEY)
    return client

def get_cosmos_database(client: CosmosClient):
    
    database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
    return database

def get_cosmos_container(database, container_name: str, partition_path="/id"):
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_path),
        offer_throughput=400
    )
    return container
