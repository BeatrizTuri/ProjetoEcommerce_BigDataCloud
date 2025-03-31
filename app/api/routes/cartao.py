from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from app.core.sql_db import SessionLocal
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario
from app.schemas.cartao_credito import CartaoCreditoCreate, CartaoCreditoResponse
from app.schemas.transacao import TransacaoRequest, TransacaoResponse

router = APIRouter(prefix="/credit_card/{id_user}", tags=["cartao"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CartaoCreditoResponse, status_code=status.HTTP_201_CREATED)
def create_cartao(id_user: int, cartao: CartaoCreditoCreate, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_user).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    novo_cartao = CartaoCredito(**cartao.model_dump(), id_usuario_cartao=id_user)
    db.add(novo_cartao)
    db.commit()
    db.refresh(novo_cartao)
    
    usuario.cartoes.append(novo_cartao)
    db.commit()
    
    return novo_cartao

@router.post("/authorize", response_model=TransacaoResponse)
def authorize_transacao(id_user: int, request: TransacaoRequest, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_user).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    cartao_compra = None

    for cartao in usuario.cartoes:
        if cartao.numero == request.numero and cartao.cvv == request.cvv:
            cartao_compra = cartao
            break
    
    if not cartao_compra:
        return TransacaoResponse(
            status="NOT_AUTHORIZED",
            dtTransacao=datetime.now(),
            message="Cartão não encontrado para o usuário",
            codigoAutorizacao=None
        )
    
    if cartao_compra.dtExpiracao < datetime.now():
        return TransacaoResponse(
            status="NOT_AUTHORIZED",
            dtTransacao=datetime.now(),
            message="Cartão Expirado",
            codigoAutorizacao=None
        )
    
    if cartao_compra.saldo < request.valor:
        return TransacaoResponse(
            status="NOT_AUTHORIZED",
            dtTransacao=datetime.now(),
            message="Sem saldo para realizar a compra",
            codigoAutorizacao=None
        )
    
    cartao_compra.saldo -= request.valor
    db.add(cartao_compra)
    db.commit()
    db.refresh(cartao_compra)
    
    return TransacaoResponse(
        status="AUTHORIZED",
        dtTransacao=datetime.now(),
        message="Compra autorizada",
        codigoAutorizacao=uuid4()
    )
