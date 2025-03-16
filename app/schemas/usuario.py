from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: str
    dtNascimento: Optional[datetime] = None
    cpf: str
    telefone: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
