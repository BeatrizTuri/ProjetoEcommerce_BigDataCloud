from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.services.cosmos_product import criar_produto, obter_produto_por_id, listar_produtos, deletar_produto_por_id, atualizar_produto
from app.schemas.alterar_produto import ProdutoUpdate


router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/batch", response_model=List[ProdutoResponse], status_code=status.HTTP_201_CREATED)
def criar_produtos(produtos: List[ProdutoCreate]):
    itens_criados = []
    erros = []
    
    for produto in produtos:
        try:
            produto_dict = produto.to_dict()
            item_criado = criar_produto(produto_dict)
            itens_criados.append(item_criado)
        except Exception as e:
            erros.append({"produto": produto.productName, "erro": str(e)})

    if erros:
        raise HTTPException(status_code=207, detail={"sucesso": itens_criados, "falhas": erros})

    return itens_criados

@router.get("/{id}", response_model=ProdutoResponse)
def obter_produtos(id: str):
    produto = obter_produto_por_id(id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

@router.get("/", response_model=List[ProdutoResponse])
def listar_todos_produtos():
    return listar_produtos()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produtos(id: str):
    produto = obter_produto_por_id(id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    deletar_produto_por_id(id)
    return None

@router.patch("/{id}", response_model=ProdutoResponse)
def atualizar_produtos(id: str, produto_update: ProdutoUpdate):
    produto = obter_produto_por_id(id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    campos_atualizados = produto_update.model_dump(exclude_unset=True)

    print(campos_atualizados)

    for campo, valor in campos_atualizados.items():
        produto[campo] = valor
        print(f"Atualizando campo {campo} para {valor}")
        
    
    try:
        produto_atualizado = atualizar_produto(id, produto)  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao atualizar produto no Cosmos DB: {str(e)}")
    
    return produto_atualizado