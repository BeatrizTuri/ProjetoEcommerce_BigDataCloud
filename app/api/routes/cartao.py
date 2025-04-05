from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from uuid import uuid4
from app.core.sql_db import SessionLocal
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario
from app.schemas.cartao_credito import CartaoCreditoCreate, CartaoCreditoResponse
from app.schemas.transacao import TransacaoRequest, TransacaoResponse
from app.schemas.alterar_saldo import CartaoCreditoUpdateSaldo

router = APIRouter(prefix="/cartao_de_credito/{id_usuario}", tags=["Cartão"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CartaoCreditoResponse, status_code=status.HTTP_201_CREATED)
def criar_cartao(id_usuario: int, cartao: CartaoCreditoCreate, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    novo_cartao = CartaoCredito(**cartao.model_dump(), id_usuario_cartao=id_usuario)
    db.add(novo_cartao)
    db.commit()
    db.refresh(novo_cartao)
    
    usuario.cartoes.append(novo_cartao)
    db.commit()
    
    return novo_cartao

@router.get("/", response_model=List[CartaoCreditoResponse])
def listar_cartoes(id_usuario: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    if not usuario.cartoes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum cartão encontrado para este usuário")
    
    return usuario.cartoes

@router.post("/autorizar", response_model=TransacaoResponse)
def autorizar_transacao(id_usuario: int, requisicao: TransacaoRequest, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    cartao_compra = None

    for cartao in usuario.cartoes:
        if cartao.numero == requisicao.numero and cartao.cvv == requisicao.cvv:
            cartao_compra = cartao
            break
    
    if not cartao_compra:
        return TransacaoResponse(
            status="NAO_AUTORIZADO",
            dtTransacao=date.today(),
            message="Cartão não encontrado para o usuário",
            codigoAutorizacao=None
        )
    
    if cartao_compra.dtExpiracao < date.today():
        return TransacaoResponse(
            status="NAO_AUTORIZADO",
            dtTransacao=date.today(),
            message="Cartão Expirado",
            codigoAutorizacao=None
        )
    
    if cartao_compra.saldo < requisicao.valor:
        return TransacaoResponse(
            status="NAO_AUTORIZADO",
            dtTransacao=date.today(),
            message="Sem saldo para realizar a compra",
            codigoAutorizacao=None
        )
    
    cartao_compra.saldo -= requisicao.valor
    db.add(cartao_compra)
    db.commit()
    db.refresh(cartao_compra)
    
    return TransacaoResponse(
        status="AUTORIZADO",
        dtTransacao=date.today(),
        message="Compra autorizada",
        codigoAutorizacao=uuid4()
    )
    
@router.patch("/{id_cartao}/saldo", response_model=CartaoCreditoResponse)
def adicionar_saldo_cartao(id_usuario: int, id_cartao: int, dados_atualizacao: CartaoCreditoUpdateSaldo, db: Session = Depends(get_db)):
    cartao = db.query(CartaoCredito).filter(CartaoCredito.id == id_cartao, CartaoCredito.id_usuario_cartao == id_usuario).first()
    if not cartao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cartão não encontrado para este usuário")
    if dados_atualizacao.saldo <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O valor deve ser positivo.")
    cartao.saldo += dados_atualizacao.saldo
    db.commit()
    db.refresh(cartao)
    return cartao