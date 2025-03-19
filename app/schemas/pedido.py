from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

class PedidoBase(BaseModel):
    id_usuario: int
    valor_total: Decimal
    status: Optional[str] = "pendente"

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id: int

    class Config:
        orm_mode = True
