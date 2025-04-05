from pydantic import BaseModel, Field, validator
from datetime import date
from typing import List, Optional
from app.schemas.cartao_credito import CartaoCreditoCreate

class UsuarioBase(BaseModel):
    nome: str
    email: str
    dtNascimento: Optional[date] = None
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
    
    @validator("email")
    def validar_email(cls, value: str) -> str:
        if value and "@" not in value:
            raise ValueError("E-mail inválido")
        return value

    @validator("telefone")
    def validar_telefone(cls, value: Optional[str]) -> Optional[str]:
        if value and not value.isdigit():
            raise ValueError("O telefone deve conter apenas números")
        return value
 

class UsuarioCreate(UsuarioBase):
    cartao_credito: Optional[CartaoCreditoCreate] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
