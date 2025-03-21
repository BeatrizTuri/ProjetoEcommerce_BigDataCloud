from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.cartao_credito import CartaoCreditoCreate

class UsuarioBase(BaseModel):
    nome: str
    email: str
    dtNascimento: Optional[datetime] = None
    cpf: str
    telefone: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    cartao_credito: Optional[CartaoCreditoCreate] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
