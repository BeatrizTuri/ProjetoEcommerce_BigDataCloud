from pydantic import BaseModel, Field
from typing import List, Optional

class ProdutoUpdate(BaseModel):
    productCategory: Optional[str] = None
    productName: Optional[str] = None
    price: Optional[float] = None
    imageUrl: Optional[List[str]] = None
    productDescription: Optional[str] = None

    class Config:
        from_attributes = True
