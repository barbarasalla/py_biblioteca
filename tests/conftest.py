import pytest

from app.models.livro import Livro
from app.repositories.livro_repository import LivroRepository
from app.services.livro_service import LivroService
from app.main import app
from app.dependencies import get_service

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient  # O FastAPI utiliza o httpx para o TestClient nas versões atuais, necessário importar httpx. 

from app.database.database import Base

@pytest.fixture
def livro():
    return Livro(
        titulo="Clean Code",
        autor="Robert C. Martin",
        ano=2008
    )

@pytest.fixture             # Criado uma fixture para o banco
def engine_test():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={
            "check_same_thread": False  # Permite que a conexão SQLite seja utilizada por threads diferentes.
        },
        poolclass=StaticPool   # Permite que a conexão SQLite seja utilizada por threads diferentes.
    )

    Base.metadata.create_all(engine)

    return engine

@pytest.fixture
def session_test(engine_test):      # Cada teste recebe o seu próprio SQLite :memory:

    SessionTest = sessionmaker( # Criar Session
        bind=engine_test
    )

    session = SessionTest()     # Entreguar para o teste

    yield session               # Esperar o teste terminar

    session.close()             # Fechar a Session (Necessário sempre para Session, arquivo, conexão, cliente HTTP e outros)

@pytest.fixture
def service_test(session_test):
    repository = LivroRepository(session_test)
    return LivroService(repository)

@pytest.fixture
def client(service_test):
    def override_get_service():
        return service_test

    app.dependency_overrides[get_service]=override_get_service

    client = TestClient(app)    # O TestClient permite fazer requisições HTTP para sua aplicação sem precisar iniciar o Uvicorn e sem abrir o Swagger.

    yield client

    app.dependency_overrides.clear()