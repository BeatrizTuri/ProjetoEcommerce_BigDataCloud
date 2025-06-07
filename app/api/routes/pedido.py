from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from pytest import Session
from app.api.routes.cartao import get_db
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.services.cosmos_pedido import create_pedido, get_pedido_by_id, list_pedidos, delete_pedido_by_id, list_pedidos_por_usuario

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResponse)
def criar_novo_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    pedido_dict = pedido.to_dict()
    pedido_criado = create_pedido(pedido_dict, db=db)
    return pedido_criado

@router.get("/search", response_model=List[PedidoResponse])
def obter_pedidos_por_usuario(usuario_id: str = Query(...)):
    pedidos = list_pedidos_por_usuario(usuario_id)

    if not pedidos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum pedido encontrado para o ID informado."
        )

    return pedidos

@router.get("/{id}", response_model=PedidoResponse)
def obter_pedido(id: str):
    pedido = get_pedido_by_id(id)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    return pedido

@router.get("/", response_model=List[PedidoResponse])
def obter_todos_pedidos():
    return list_pedidos()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pedido(id: str):
    pedido = get_pedido_by_id(id)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    delete_pedido_by_id(id)
    return None




