from pydantic import BaseModel
from typing import List
from decimal import Decimal

class ItemPedidoBase(BaseModel):
    id_produto: str  # ID do produto no CosmosDB
    quantidade: int

class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoRead(ItemPedidoBase):
    preco_unitario: Decimal

class PedidoCreate(BaseModel):
    id_usuario: str
    itens: List[ItemPedidoCreate]

class PedidoRead(PedidoCreate):
    id: str
    valor_total: Decimal
    status: str
    itens: List[ItemPedidoRead]

    class Config:
        orm_mode = True
