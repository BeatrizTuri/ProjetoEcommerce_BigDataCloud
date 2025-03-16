from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from app.core.database import SessionLocal
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

# Endpoint para criar um cartão de crédito e associá-lo a um usuário
@router.post("/", response_model=CartaoCreditoResponse, status_code=status.HTTP_201_CREATED)
def create_cartao(id_user: int, cartao: CartaoCreditoCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.id == id_user).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    # Cria o cartão, associando o id do usuário
    novo_cartao = CartaoCredito(**cartao.dict(), id_usuario_cartao=id_user)
    db.add(novo_cartao)
    db.commit()
    db.refresh(novo_cartao)
    
    # Opcional: também pode adicionar o cartão à lista do usuário
    usuario.cartoes.append(novo_cartao)
    db.commit()
    
    return novo_cartao

# Endpoint para autorizar uma transação no cartão de crédito
@router.post("/authorize", response_model=TransacaoResponse)
def authorize_transacao(id_user: int, request: TransacaoRequest, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.id == id_user).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    cartao_compra = None
    # Busca o cartão do usuário que corresponde ao número e cvv
    for cartao in usuario.cartoes:
        if cartao.numero == request.numero and cartao.cvv == request.cvv:
            cartao_compra = cartao
            break
    
    # Se não encontrou, retorna NOT_AUTHORIZED
    if not cartao_compra:
        return TransacaoResponse(
            status="NOT_AUTHORIZED",
            dtTransacao=datetime.now(),
            message="Cartão não encontrado para o usuário",
            codigoAutorizacao=None
        )
    
    # Verifica se o cartão está expirado
    if cartao_compra.dtExpiracao < datetime.now():
        return TransacaoResponse(
            status="NOT_AUTHORIZED",
            dtTransacao=datetime.now(),
            message="Cartão Expirado",
            codigoAutorizacao=None
        )
    
    # Verifica se há saldo suficiente para a transação
    if cartao_compra.saldo < request.valor:
        return TransacaoResponse(
            status="NOT_AUTHORIZED",
            dtTransacao=datetime.now(),
            message="Sem saldo para realizar a compra",
            codigoAutorizacao=None
        )
    
    # Debita o valor da compra
    cartao_compra.saldo -= request.valor
    db.add(cartao_compra)
    db.commit()
    db.refresh(cartao_compra)
    
    # Retorna resposta autorizada com um código de autorização gerado
    return TransacaoResponse(
        status="AUTHORIZED",
        dtTransacao=datetime.now(),
        message="Compra autorizada",
        codigoAutorizacao=uuid4()
    )
