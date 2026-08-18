from fastapi import FastAPI, HTTPException, status

from livro_service import LivroService
from schemas import LivroResponse, LivroCreate, LivroUpdate

service = LivroService()

app = FastAPI()

@app.get("/")
def inicio():
    return{
        "mensagem": "API da Biblioteca Funcionando!"
    }

@app.get("/livros",
         response_model=list[LivroResponse]) # Essa rota retorna uma lista de LivroResponse
def listar_livros():
    return service.listar_livros()

@app.post("/livros",
          response_model=LivroResponse,
          status_code=status.HTTP_201_CREATED)
def cadastrar_livro(dados: LivroCreate):    # Essa função precisa receber um objeto LivroCreate.
    livro = service.cadastrar_livro(
        dados.titulo,
        dados.autor,
        dados.ano
    )
    return livro

@app.get("/livros/{id_livro}",
         response_model=LivroResponse)
def buscar_livro_por_id(id_livro: int):
    livro = service.buscar_por_id(id_livro)

    if livro is None:
        raise HTTPException(                    # raise -> Interrompa a execução normal e lance essa exceção.
            status_code=404,
            detail="Livro não encontrado"
        )

    return livro

@app.put("/livros/{id_livro}")
def atualizar_livro(id_livro: int, livro_novo: LivroUpdate):

    livro = service.buscar_por_id(id_livro)

    if livro is None:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado."
        )
    
    sucesso = service.atualizar_livro(id_livro, livro_novo.titulo, livro_novo.autor, livro_novo.ano)

    if not sucesso:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível atualizar o livro."
        )
    return livro

@app.delete("/livros/{id_livro}",
            status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(id_livro: int):
    sucesso = service.excluir_livro(id_livro)
    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )