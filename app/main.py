from fastapi import FastAPI
from app.api.routes import usuario

app = FastAPI()

app.include_router(usuario.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
