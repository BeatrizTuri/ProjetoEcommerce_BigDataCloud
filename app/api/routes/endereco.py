from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.sql_db import SessionLocal
from app.models.endereco import Endereco
from app.models.usuario import Usuario
from app.schemas.endereco import EnderecoCreate, EnderecoRead

router = APIRouter(prefix="/endereco/{id_usuario}", tags=["Endereço"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EnderecoRead, status_code=status.HTTP_201_CREATED)
def criar_endereco(id_usuario: int, endereco: EnderecoCreate, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    novo_endereco = Endereco(**endereco.model_dump())
    novo_endereco.id_usuario = usuario.id  

    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)

    usuario.enderecos.append(novo_endereco)
    db.commit()
    
    return novo_endereco

@router.get("/", response_model=List[EnderecoRead])
def listar_enderecos(id_usuario: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    if not usuario.enderecos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum endereço encontrado para este usuário")
    
    return usuario.enderecos