from pydantic import BaseModel
from typing import List
from decimal import Decimal

class ProdutoPedidoBase(BaseModel):
    id_produto: str  
    quantidade: int

class ProdutoPedidoCreate(ProdutoPedidoBase):
    pass

class ProdutoPedidoRead(ProdutoPedidoBase):
    preco_unitario: Decimal

class PedidoCreate(BaseModel):
    id_usuario: str
    produtos: List[ProdutoPedidoCreate]

class PedidoRead(PedidoCreate):
    id: str
    valor_total: Decimal
    status: str
    produtos: List[ProdutoPedidoRead]

    class Config:
        from_attributes = True
