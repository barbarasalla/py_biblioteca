from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.livros import router as livros_router
from app.startup.biblioteca_carga_inicial import carregar_biblioteca


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Define operações executadas durante o ciclo de vida
    da aplicação.

    O código antes do yield representa o startup.

    O código depois do yield representaria operações
    de shutdown.
    """
    # O Alembic é responsável por criar e alterar a estrutura do banco.


    # Carrega os livros iniciais do biblioteca.json
    carregar_biblioteca()

    # A aplicação começa a atender as requisições
    yield

# Cria a aplicação FastAPI utilizando o lifespan.
app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
def inicio():
    return {
        "mensagem": "API da Biblioteca Funcionando!"
    }

# Registra as rotas de livros na aplicação.
app.include_router(livros_router)