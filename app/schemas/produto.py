from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: Decimal
    estoque: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: str 

    class Config:
        from_attributes = True
