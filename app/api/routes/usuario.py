from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.sql_db import SessionLocal
from app.models.cartao_credito import CartaoCredito
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.alterar_usuario import UsuarioUpdate
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[UsuarioResponse])
def obter_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    if not usuarios:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum usuário encontrado")
    return usuarios


@router.get("/buscar-id-por-cpf")
def buscar_id_por_cpf(cpf: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.cpf == cpf).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado com esse CPF.")
    return {"id_usuario": usuario.id}

@router.get("/{id}", response_model=UsuarioResponse)
def obter_usuario_por_id(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        # Verifica se já existe usuário com o mesmo e-mail ou CPF
        if db.query(Usuario).filter(Usuario.email == usuario.email).first():
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
        if db.query(Usuario).filter(Usuario.cpf == usuario.cpf).first():
            raise HTTPException(status_code=400, detail="CPF já cadastrado.")

        novo_usuario = Usuario(**usuario.model_dump(exclude={"cartao_credito"}))
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {str(e)}")

    if usuario.cartao_credito:
        try:
            novo_cartao = CartaoCredito(
                **usuario.cartao_credito.model_dump(),
                id_usuario_cartao=novo_usuario.id
            )
            db.add(novo_cartao)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Usuário criado, mas erro ao cadastrar cartão: {str(e)}")

    return novo_usuario

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    db.delete(usuario)
    db.commit()
    return None

@router.patch("/{id}", response_model=UsuarioResponse)
def atualizar_usuario(id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if usuario_update.email:
        usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_update.email).first()
        if usuario_existente and usuario_existente.id != id:  
            print("Este email já está sendo usado")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já está em uso.")

    for campo, valor in usuario_update.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario
