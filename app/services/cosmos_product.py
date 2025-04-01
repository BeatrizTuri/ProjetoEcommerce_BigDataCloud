from azure.cosmos import CosmosClient, PartitionKey, exceptions
from app.core.cosmos_db import COSMOS_URI, COSMOS_KEY, COSMOS_DATABASE, COSMOS_CONTAINER_PRODUTOS

client = CosmosClient(COSMOS_URI, COSMOS_KEY)
database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
container = database.create_container_if_not_exists(
    id=COSMOS_CONTAINER_PRODUTOS,
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

def create_product(product: dict) -> dict:
    return container.create_item(body=product)

def list_products() -> list:
    query = "SELECT * FROM produtos"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    return items

def get_product_by_id(product_id: str) -> dict:
    try:
        return container.read_item(item=product_id, partition_key=product_id)
    except exceptions.CosmosResourceNotFoundError:
        return None

def delete_product_by_id(product_id: str) -> None:
    container.delete_item(item=product_id, partition_key=product_id)
    
def update_product(product_id: str, product_dict: dict) -> dict:
    try:
        # Assuming 'product_dict' contains the updated data and 'id' is the partition key
        product_dict['id'] = product_id  # Ensure 'id' is in the document to maintain consistency
        container.upsert_item(body=product_dict)  # Using 'upsert_item' to insert or update the product
        return product_dict
    except exceptions.CosmosHttpResponseError as e:
        raise Exception(f"Error updating product in Cosmos DB: {str(e)}")
