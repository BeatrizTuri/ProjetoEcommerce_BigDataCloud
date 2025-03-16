from fastapi import FastAPI
from app.api.routes import cartao, usuario 

app = FastAPI()

app.include_router(usuario.router)
app.include_router(cartao.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
