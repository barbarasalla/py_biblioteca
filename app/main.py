from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.livros import router as livros_router
from app.startup.biblioteca_carga_inicial import carregar_biblioteca


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Cria as tabelas do banco caso ainda não existam
    Base.metadata.create_all(engine)

    # Carrega os livros iniciais do biblioteca.json
    carregar_biblioteca()

    # A aplicação começa a atender as requisições
    yield


app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
def inicio():
    return {
        "mensagem": "API da Biblioteca Funcionando!"
    }


app.include_router(livros_router)