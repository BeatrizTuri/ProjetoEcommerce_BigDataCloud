from pydantic import BaseModel, validator
from datetime import datetime
from decimal import Decimal

class CartaoCreditoBase(BaseModel):
    numero: str
    dtExpiracao: datetime
    cvv: str
    saldo: Decimal

    @validator("cvv")
    def cvv_must_be_valid(cls, value: str) -> str:
        if len(value) != 3:
            raise ValueError("CVV deve ter exatamente 3 dígitos.")
        if not value.isdigit():
            raise ValueError("CVV deve conter apenas dígitos.")
        return value

class CartaoCreditoCreate(CartaoCreditoBase):
    pass

class CartaoCreditoResponse(CartaoCreditoBase):
    id: int
    id_usuario_cartao: int

    class Config:
        from_attibutes = True
