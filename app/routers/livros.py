from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_service
from app.services.livro_service import LivroService
from app.schemas.schemas import LivroResponse, LivroCreate, LivroUpdate
from app.exceptions.api_exceptions import LivroNaoEncontradoError, APIConsumeError, LivroDadosInvalidosError


# grupo de endpoints
router = APIRouter(
    prefix="/livros",   # Define o prefixo para toda as rotas da classe
    tags=["Livros"]
)

@router.get("/")
def inicio():
    return{
        "mensagem": "API da Biblioteca Funcionando!"
    }

@router.get("",
         response_model=list[LivroResponse]) # Essa rota retorna uma lista de LivroResponse
def listar_livros(
     service: LivroService = Depends(get_service)   # Indica uma dependencia ao FastAPI, que para executar essa função, é necessário um service. E, para conseguir esse service, execute get_service()
):
    return service.listar_livros()


@router.post("",
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

@router.post("/isbn/{isbn}",
          response_model=LivroResponse,
          status_code=status.HTTP_201_CREATED)
def cadastrar_livro_por_isbn(isbn: int,
                             service: LivroService = Depends(get_service)):

    try:
        livro = service.cadastrar_por_isbn(isbn)
    except LivroNaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except APIConsumeError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )
    except LivroDadosInvalidosError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    return livro

@router.get("/autor",
         response_model=list[LivroResponse])
def buscar_livro_por_autor(autor: str,
                           service: LivroService = Depends(get_service)):

    livros = service.buscar_por_autor(autor)
    return livros

@router.get("/titulo",
         response_model=list[LivroResponse])
def buscar_livro_por_titulo(titulo: str,
                           service: LivroService = Depends(get_service)):

    livros = service.buscar_por_titulo(titulo)
    return livros

@router.get("/{id_livro}",
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

@router.put("/{id_livro}",
         response_model=LivroResponse)
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

@router.delete("/{id_livro}",
            status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(id_livro: int,
                  service: LivroService = Depends(get_service)):
    sucesso = service.excluir_livro(id_livro)
    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado"
        )