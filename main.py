from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Minha API de Produtos",
    version="1.0.0"
)

# Permite que o HTML converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo dos produtos
class Produto(BaseModel):
    nome: str
    preco: float
    quantidade: int


# Lista de produtos
produtos = [
    {
        "id": 1,
        "nome": "Notebook",
        "preco": 2500.00,
        "quantidade": 5
    },
    {
        "id": 2,
        "nome": "Mouse",
        "preco": 50.00,
        "quantidade": 20
    }
]


# Rota inicial
@app.get("/")
def inicio():
    return {
        "mensagem": "Minha API está funcionando!",
        "documentacao": "/docs"
    }


# Listar todos os produtos
@app.get("/produtos")
def listar_produtos():
    return produtos


# Buscar um produto pelo ID
@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):

    for produto in produtos:
        if produto["id"] == produto_id:
            return produto

    return {"erro": "Produto não encontrado"}


# Cadastrar um produto
@app.post("/produtos")
def cadastrar_produto(produto: Produto):

    novo_produto = {
        "id": len(produtos) + 1,
        "nome": produto.nome,
        "preco": produto.preco,
        "quantidade": produto.quantidade
    }

    produtos.append(novo_produto)

    return {
        "mensagem": "Produto cadastrado com sucesso!",
        "produto": novo_produto
    }


# Atualizar um produto
@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, produto: Produto):

    for item in produtos:
        if item["id"] == produto_id:

            item["nome"] = produto.nome
            item["preco"] = produto.preco
            item["quantidade"] = produto.quantidade

            return {
                "mensagem": "Produto atualizado com sucesso!",
                "produto": item
            }

    return {"erro": "Produto não encontrado"}


# Excluir um produto
@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):

    for produto in produtos:
        if produto["id"] == produto_id:

            produtos.remove(produto)

            return {
                "mensagem": "Produto excluído com sucesso!"
            }

    return {"erro": "Produto não encontrado"}