from app.core.sql_db import container_usuarios
from app import schemas
from fastapi import HTTPException
import uuid

def criar_usuario(usuario: schemas.UsuarioCreate):
    usuario_id = str(uuid.uuid4())
    novo_usuario = {
        "id": usuario_id,
        "nome": usuario.nome,
        "email": usuario.email,
        "cpf": usuario.cpf,
        "telefone": usuario.telefone
    }
    container_usuarios.upsert_item(novo_usuario)
    return novo_usuario

def buscar_usuario(id_usuario: str):
    query = f"SELECT * FROM Usuarios WHERE Usuarios.id = '{id_usuario}'"
    usuarios = list(container_usuarios.query_items(query=query, enable_cross_partition_query=True))
    
    if not usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuarios[0]
