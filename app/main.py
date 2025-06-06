from fastapi import FastAPI
from app.api.routes import carrinho, produto, usuario, cartao, endereco, pedido, tipo_endereco
from app.core.sql_db import Base, engine
from app.core.cosmos_db import (
    get_cosmos_client, 
    get_cosmos_database, 
    get_cosmos_container,
    COSMOS_CONTAINER_PRODUTOS,
    COSMOS_CONTAINER_CARRINHO,
    COSMOS_CONTAINER_PEDIDOS
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    client = get_cosmos_client()
    database = get_cosmos_database(client)
    
    carrinho_container = get_cosmos_container(database, COSMOS_CONTAINER_CARRINHO)
    print(f"Container de carrinho criado ou obtido: {carrinho_container.id}")
    
    produtos_container = get_cosmos_container(database, COSMOS_CONTAINER_PRODUTOS)
    print(f"Container de produtos criado ou obtido: {produtos_container.id}")
    
    pedidos_container = get_cosmos_container(database, COSMOS_CONTAINER_PEDIDOS)
    print(f"Container de pedidos criado ou obtido: {pedidos_container.id}")

app.include_router(usuario.router)
app.include_router(cartao.router)
app.include_router(endereco.router)
app.include_router(tipo_endereco.router)
app.include_router(produto.router)
app.include_router(pedido.router)  
app.include_router(carrinho.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
