from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from app.api.routes.cartao import get_db
from app.schemas.carrinho import ItemCarrinho, FinalizarCarrinhoRequest
from app.services.cosmos_carrinho import (
    get_cart,
    add_to_cart,
    remove_from_cart,
    clear_cart,
    finalize_cart
)

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

@router.get("/{id_usuario}")
def visualizar_carrinho(id_usuario: str):
    return get_cart(id_usuario)

@router.post("/{id_usuario}/adicionar")
def adicionar_ao_carrinho(id_usuario: str, item: ItemCarrinho):
    try:
        return add_to_cart(id_usuario, item.dict())  
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_usuario}/remover/{id_produto}")
def remover_do_carrinho(id_usuario: str, id_produto: str):
    return remove_from_cart(id_usuario, id_produto)

@router.delete("/{id_usuario}/limpar")
def limpar_carrinho(id_usuario: str):
    return clear_cart(id_usuario)

@router.post("/{id_usuario}/finalizar")
def finalizar_carrinho(id_usuario: str, body:FinalizarCarrinhoRequest, db: Session = Depends(get_db)):
    try:
        return finalize_cart(id_usuario, db=db, cvv=body.cvv)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
