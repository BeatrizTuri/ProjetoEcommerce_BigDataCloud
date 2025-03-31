from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ItemCarrinho(BaseModel):
    id_produto: str
    quantidade: int = Field(..., gt=0, description="A quantidade deve ser maior que zero.")
    categoria: Optional[str] = None  # Preenchida automaticamente no backend

    @validator("id_produto")
    def id_produto_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("O ID do produto não pode estar vazio.")
        return v

class CarrinhoResponse(BaseModel):
    id_usuario: str
    produtos: List[ItemCarrinho]

    @validator("id_usuario")
    def id_usuario_nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("O ID do usuário não pode estar vazio.")
        return v
