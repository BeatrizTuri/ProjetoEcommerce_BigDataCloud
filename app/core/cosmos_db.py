import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Equivalente à CosmosProperties (usando prefixo "AZURE_COSMOS")
COSMOS_URI = os.getenv("AZURE_COSMOS_URI", "https://localhost:8081")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY", "C2y6yDjf5/R+ob0N8A7Cgv30VR==")
COSMOS_DATABASE = os.getenv("AZURE_COSMOS_DATABASE", "ecommerce")
COSMOS_CONTAINER = os.getenv("AZURE_COSMOS_CONTAINER", "produtos")
COSMOS_QUERY_METRICS_ENABLED = os.getenv("AZURE_COSMOS_QUERY_METRICS_ENABLED", "false").lower() == "true"
COSMOS_RESPONSE_DIAGNOSTICS_ENABLED = os.getenv("AZURE_COSMOS_RESPONSE_DIAGNOSTICS_ENABLED", "false").lower() == "true"

def get_cosmos_client():
    """Cria e retorna um cliente do Cosmos DB configurado."""
    client = CosmosClient(COSMOS_URI, COSMOS_KEY)
    return client

def get_cosmos_database(client: CosmosClient):
    """Cria ou obtém o banco de dados configurado."""
    database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
    return database

def get_cosmos_container(database):
    """Cria ou obtém o container (coleção) configurado."""
    container = database.create_container_if_not_exists(
        id=COSMOS_CONTAINER,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    return container
