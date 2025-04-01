from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    dtNascimento: Optional[date] = None
    telefone: Optional[str] = None
    
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

    class Config:
        from_attributes = True
