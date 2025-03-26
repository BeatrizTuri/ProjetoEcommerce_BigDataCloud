import uuid
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

def criar_pedido(db: Session, pedido: schemas.PedidoCreate):
    novo_pedido = models.Pedido(
        id_usuario=pedido.id_usuario,
        valor_total=0,  
        status="pendente"
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

def adicionar_produto_pedido(db: Session, id_pedido: int, produto: schemas.ProdutoPedidoCreate):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    novo_produto = models.ProdutoPedido(
        id_pedido=id_pedido,
        id_produto=produto.id_produto,
        quantidade=produto.quantidade,
        preco_unitario=50  
    )

    pedido.valor_total += novo_produto.quantidade * novo_produto.preco_unitario
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

def listar_produtos_pedido(db: Session, id_pedido: int):
    produtos = db.query(models.ProdutoPedido).filter(models.ProdutoPedido.id_pedido == id_pedido).all()
    return produtos

def remover_produto_pedido(db: Session, id_pedido: int, id_produto: int):
    produto = db.query(models.ProdutoPedido).filter(
        models.ProdutoPedido.id_pedido == id_pedido,
        models.ProdutoPedido.id_produto == id_produto
    ).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado no pedido")

    db.delete(produto)
    db.commit()
    return {"message": "Produto removido do pedido"}

def finalizar_pedido(db: Session, pedido: schemas.PedidoCreate):
    pedido_db = db.query(models.Pedido).filter(models.Pedido.id == pedido.id).first()
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido_db.status = "finalizado"
    db.commit()
    return pedido_db
