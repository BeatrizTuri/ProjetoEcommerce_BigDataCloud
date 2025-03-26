from fastapi import FastAPI
from app.api.routes import usuario, cartao, endereco

app = FastAPI()

app.include_router(usuario.router)
app.include_router(cartao.router)
app.include_router(endereco.router)
# app.include_router(produto.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
