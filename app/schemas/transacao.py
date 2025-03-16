from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import Optional

class TransacaoRequest(BaseModel):
    numero: str
    dtExpiracao: datetime 
    cvv: str
    valor: Decimal

class TransacaoResponse(BaseModel):
    status: str
    codigoAutorizacao: Optional[UUID] = None
    dtTransacao: datetime
    message: str

    class Config:
        orm_mode = True
