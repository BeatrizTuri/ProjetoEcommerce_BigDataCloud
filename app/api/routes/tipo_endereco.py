from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.sql_db import SessionLocal
from app.models.tipo_endereco import TipoEndereco
from app.schemas.tipo_endereco import TipoEnderecoCreate, TipoEnderecoResponse

router = APIRouter(prefix="/tipos_endereco", tags=["Tipos de Endereço"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[TipoEnderecoResponse])
def listar_tipos_endereco(db: Session = Depends(get_db)):
    tipos = db.query(TipoEndereco).all()
    if not tipos:
        raise HTTPException(status_code=404, detail="Nenhum tipo de endereço encontrado")
    return tipos


@router.post("/", response_model=TipoEnderecoResponse, status_code=status.HTTP_201_CREATED)
def criar_tipo_endereco(tipo: TipoEnderecoCreate, db: Session = Depends(get_db)):
    novo_tipo = TipoEndereco(**tipo.model_dump())
    db.add(novo_tipo)
    db.commit()
    db.refresh(novo_tipo)
    return novo_tipo
