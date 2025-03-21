from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.sql_db import SessionLocal
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET /users - Lista todos os usuários
@router.get("/", response_model=List[UsuarioResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(Usuario).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuários não encontrados")
    return users

# GET /users/{id} - Busca um usuário por ID
@router.get("/{id}", response_model=UsuarioResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

# POST /users - Cria um novo usuário
@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_user(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    new_user = Usuario(**usuario.model_dump(exclude={"cartao_credito"}))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Criar o cartão se foi enviado no payload
    if usuario.cartao_credito:
        novo_cartao = CartaoCredito(
            **usuario.cartao_credito.model_dump(),
            id_usuario_cartao=new_user.id
        )
        db.add(novo_cartao)
        db.commit()
        db.refresh(novo_cartao)

    return new_user

# DELETE /users/{id} - Deleta um usuário
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return None
