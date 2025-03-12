from pydantic import BaseModel
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    dtNascimento: datetime
    CPF: str
    telefone: str
