from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.sql_db import SessionLocal
from app.models.endereco import Endereco
from app.models.usuario import Usuario
from app.schemas.endereco import EnderecoCreate, EnderecoRead

router = APIRouter(prefix="/address/{id_user}", tags=["endereco"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EnderecoRead, status_code=status.HTTP_201_CREATED)
def create_endereco(id_user: int, endereco: EnderecoCreate, db: Session = Depends(get_db)):
   
    usuario = db.query(Usuario).filter(Usuario.id == id_user).first()
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
