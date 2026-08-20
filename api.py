from fastapi import FastAPI, Depends, HTTPException, status

from database import SessionLocal, Base, engine
from livro_service import LivroService
from livro_repository import LivroRepository
from schemas import LivroResponse, LivroCreate, LivroUpdate

Base.metadata.create_all(engine)

app = FastAPI()


def get_service():             # Função executada pelo FastAPI

    session = SessionLocal()        # Cria uma sessão com o banco.

    try:
        repository = LivroRepository(session)   # Cria o Repository passando a Session

        service = LivroService(repository)  # Cria o Service passando o Repository

        yield service       # Entregue esse objeto para o endpoint, mas depois que o endpoint terminar, volte aqui para eu fazer a limpeza
                            # yield: retorna um valor temporariamente, pausando a execução da função.
                            # Quando a execução for retomada, ela continua a partir do yield.
                            
    finally:                # Executa de qualquer forma, mesmo que haja uma exceção
        session.close()


@app.get("/")
def inicio():
    return{
        "mensagem": "API da Biblioteca Funcionando!"
    }

@app.get("/livros",
         response_model=list[LivroResponse]) # Essa rota retorna uma lista de LivroResponse
def listar_livros(
     service: LivroService = Depends(get_service)   # Indica uma dependencia ao FastAPI, que para executar essa função, é necessário um service. E, para conseguir esse service, execute get_service()
):
    return service.listar_livros()


@app.post("/livros",
          response_model=LivroResponse,
          status_code=status.HTTP_201_CREATED)
def cadastrar_livro(dados: LivroCreate,
                    service: LivroService = Depends(get_service)):    # Essa função precisa receber um objeto LivroCreate.
    livro = service.cadastrar_livro(
        dados.titulo,
        dados.autor,
        dados.ano
    )
    return livro

@app.get("/livros/{id_livro}",
         response_model=LivroResponse)
def buscar_livro_por_id(id_livro: int,
                        service: LivroService = Depends(get_service)):
    livro = service.buscar_por_id(id_livro)

    if livro is None:
        raise HTTPException(                    # raise -> Interrompa a execução normal e lance essa exceção.
            status_code=404,
            detail="Livro não encontrado"
        )

    return livro

@app.put("/livros/{id_livro}")
def atualizar_livro(id_livro: int, livro_novo: LivroUpdate, 
                    service: LivroService = Depends(get_service)):

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
def deletar_livro(id_livro: int,
                  service: LivroService = Depends(get_service)):
    sucesso = service.excluir_livro(id_livro)
    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )