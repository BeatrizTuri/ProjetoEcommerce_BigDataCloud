from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from app.schemas.cartao_credito import CartaoCreditoCreate

class UsuarioBase(BaseModel):
    nome: str
    email: str
    dtNascimento: Optional[datetime] = None
    cpf: str
    telefone: Optional[str] = None
    
    @validator("cpf")
    def validar_cpf(cls, value: str) -> str:  # Debugging print
        if len(value) != 11:
            print("CPF pode ter somente 11 números")
            raise ValueError("CPF pode ter somente 11 números")
        if not value.isdigit():
            print("CPF deve conter apenas dígitos")
            raise ValueError("CPF deve conter apenas dígitos")
        return value

class UsuarioCreate(UsuarioBase):
    cartao_credito: Optional[CartaoCreditoCreate] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
