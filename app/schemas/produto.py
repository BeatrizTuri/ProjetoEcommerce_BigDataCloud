from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

class ProdutoBase(BaseModel):
    productCategory: str
    productName: str
    price: float
    imageUrl: List[str]
    productDescription: str

    def to_dict(self):
        return {**self.model_dump(), "id": str(uuid4())}

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: str = Field(default_factory=lambda: str(uuid4()))

    class Config:
        from_attributes = True
