from pydantic import BaseModel
from datetime import date
from uuid import UUID
from decimal import Decimal
from typing import Optional

class TransacaoRequest(BaseModel):
    numero: str
    dtExpiracao: date 
    cvv: str
    valor: Decimal

class TransacaoResponse(BaseModel):
    status: str
    codigoAutorizacao: Optional[UUID] = None
    dtTransacao: date
    message: str

    class Config:
        from_attributes = True
