from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
import uuid




class CartaoResumo(BaseModel):
    numero_final: str
    validade: str

class ItemPedidoBase(BaseModel):
    id_produto: str
    nome: Optional[str] = None
    quantidade: int
    categoria: str
    data: datetime = Field(default_factory=datetime.now)
    
class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoResponse(ItemPedidoBase):
    preco_unitario: Decimal

class PedidoBase(BaseModel):
    id_usuario: str
    produtos: List[ItemPedidoCreate]
    cvv: Optional[str] = None

    def to_dict(self):
        return {**self.model_dump(), "id": str(uuid.uuid4())}

class PedidoCreate(PedidoBase):
    pass

class PedidoResponse(PedidoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    valor_total: Decimal
    status: str = "pendente"
    produtos: List[ItemPedidoResponse]
    id_cartao_utilizado: int
    cvv: Optional[str] = None
    cartao_utilizado: CartaoResumo

    class Config:
        from_attributes = True
