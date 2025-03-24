from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.cartao_credito import CartaoCreditoCreate
# from app.schemas.endereco import EnderecoCreate

class UsuarioBase(BaseModel):
    nome: str
    email: str
    dtNascimento: Optional[datetime] = None
    cpf: str
    telefone: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    cartao_credito: Optional[CartaoCreditoCreate] = None
    # enderecos: Optional[List[EnderecoCreate]] = Field(default_factory=list)

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
