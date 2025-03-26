from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from app.core.sql_db import get_db
from app.crud import pedido

router = APIRouter()

# POST /pedidos/ - Cria um novo pedido
@router.post("/pedidos/", response_model=schemas.PedidoRead)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = pedido.criar_pedido(db=db, pedido=pedido)
    return novo_pedido

# POST /pedidos/finalizar - Finaliza um pedido
@router.post("/pedidos/finalizar", response_model=schemas.PedidoRead)
def finalizar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return pedido.finalizar_pedido(db, pedido)

# GET /pedidos - Lista todos os pedidos
@router.get("/pedidos/", response_model=list[schemas.PedidoRead])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = pedido.listar_pedidos(db)
    return pedidos

# GET /pedidos/{id} - Busca um pedido por ID
@router.get("/pedidos/{id}", response_model=schemas.PedidoRead)
def buscar_pedido(id: int, db: Session = Depends(get_db)):
    pedido_db = pedido.buscar_pedido(db, id)
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido_db

# PUT /pedidos/{id} - Atualiza um pedido
@router.put("/pedidos/{id}", response_model=schemas.PedidoRead)
def atualizar_pedido(id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return pedido.atualizar_pedido(db, id, pedido)

# DELETE /pedidos/{id} - Deleta um pedido
@router.delete("/pedidos/{id}", status_code=204)
def deletar_pedido(id: int, db: Session = Depends(get_db)):
    return pedido.deletar_pedido(db, id)

# GET /pedidos/{id}/produtos - Lista os produtos de um pedido
@router.get("/pedidos/{id}/produtos", response_model=list[schemas.ProdutoPedidoRead])
def listar_produtos_pedido(id: int, db: Session = Depends(get_db)):
    produtos = pedido.listar_produtos_pedido(db, id)
    return produtos

# POST /pedidos/{id}/produtos - Adiciona um produto a um pedido
@router.post("/pedidos/{id}/produtos", response_model=schemas.ProdutoPedidoRead)
def adicionar_produto_pedido(id: int, produto: schemas.ProdutoPedidoCreate, db: Session = Depends(get_db)):
    return pedido.adicionar_produto_pedido(db, id, produto)

# DELETE /pedidos/{id_pedido}/produtos/{id_produto} - Remove um produto de um pedido
@router.delete("/pedidos/{id_pedido}/produtos/{id_produto}", status_code=204)
def remover_produto_pedido(id_pedido: int, id_produto: int, db: Session = Depends(get_db)):
    return pedido.remover_produto_pedido(db, id_pedido, id_produto)

# PUT /pedidos/{id_pedido}/produtos/{id_produto} - Atualiza um produto de um pedido  
@router.put("/pedidos/{id_pedido}/produtos/{id_produto}", response_model=schemas.ProdutoPedidoRead)
def atualizar_produto_pedido(id_pedido: int, id_produto: int, produto: schemas.ProdutoPedidoCreate, db: Session = Depends(get_db)):
    return pedido.atualizar_produto_pedido(db, id_pedido, id_produto, produto)
