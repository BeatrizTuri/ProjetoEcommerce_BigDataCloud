# from fastapi import APIRouter, HTTPException, status
# from uuid import uuid4
# from typing import List
# from app.schemas.produto import ProdutoCreate, ProdutoResponse
# from app.services.cosmos_product import create_product, list_products, get_product_by_id, delete_product_by_id

# router = APIRouter(prefix="/products", tags=["products"])

# @router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
# def create_product_endpoint(produto: ProdutoCreate):
#     product_data = produto.dict()
#     # Gerar identificador único (UUID)
#     product_data["id"] = str(uuid4())
#     created_item = create_product(product_data)
#     return created_item

# @router.get("/{id}", response_model=ProdutoResponse)
# def get_product(id: str):
#     product = get_product_by_id(id)
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
#     return product

# @router.get("/", response_model=List[ProdutoResponse])
# def get_all_products():
#     return list_products()

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_product(id: str):
#     product = get_product_by_id(id)
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
#     delete_product_by_id(id)
#     return None
