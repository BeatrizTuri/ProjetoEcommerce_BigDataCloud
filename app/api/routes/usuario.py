from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/users", tags=["users"])

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
    return users

# GET /users/{id} - Busca um usuário por ID
@router.get("/{id}", response_model=UsuarioResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# POST /users - Cria um novo usuário
@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_user(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    new_user = Usuario(**usuario.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# DELETE /users/{id} - Deleta um usuário
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return None
