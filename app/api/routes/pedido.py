from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.core.database import get_db
from app.crud import pedido

router = APIRouter()

@router.post("/pedidos/", response_model=schemas.PedidoRead)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):

    novo_pedido = pedido.criar_pedido(db=db, pedido=pedido)
    return novo_pedido

@router.post("/pedidos/finalizar", response_model=schemas.PedidoRead)
def finalizar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return pedido.finalizar_pedido(db, pedido)