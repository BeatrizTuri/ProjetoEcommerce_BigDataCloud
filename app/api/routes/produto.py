from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.services.cosmos_product import create_product, get_product_by_id, list_products, delete_product_by_id

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/batch", response_model=List[ProdutoResponse], status_code=status.HTTP_201_CREATED)
def create_produtos(produtos: List[ProdutoCreate]):
    created_items = []
    errors = []
    
    for produto in produtos:
        try:
            produto_dict = produto.to_dict()
            created_item = create_product(produto_dict)
            created_items.append(created_item)
        except Exception as e:
            errors.append({"produto": produto.productName, "erro": str(e)})

    if errors:
        raise HTTPException(status_code=207, detail={"sucesso": created_items, "falhas": errors})

    return created_items

@router.get("/{id}", response_model=ProdutoResponse)
def get_produto(id: str):
    product = get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return product

@router.get("/", response_model=List[ProdutoResponse])
def get_all_produtos():
    return list_products()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(id: str):
    product = get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    delete_product_by_id(id)
    return None
