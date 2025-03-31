from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pytest import Session
from app.api.routes.cartao import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.services.cosmos_pedido import create_pedido, get_pedido_by_id, list_pedidos, delete_pedido_by_id

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.post("/", response_model=PedidoResponse)
def create_new_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    pedido_dict = pedido.to_dict()
    created_pedido = create_pedido(pedido_dict, db=db)
    return created_pedido

@router.get("/{id}", response_model=PedidoResponse)
def get_pedido(id: str):
    pedido = get_pedido_by_id(id)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    return pedido

@router.get("/", response_model=List[PedidoResponse])
def get_all_pedidos():
    return list_pedidos()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pedido(id: str):
    pedido = get_pedido_by_id(id)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    delete_pedido_by_id(id)
    return None
