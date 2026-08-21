from app.database.database import SessionLocal
from app.repositories.livro_repository import LivroRepository
from app.services.livro_service import LivroService


def get_service():          # SETUP # Função executada pelo FastAPI
    """
    Cria as dependências necessárias para atender uma requisição.

    Fluxo: Session -> Repository -> Service
    """

    session = SessionLocal()        # Cria uma sessão com o banco.

    try:
        repository = LivroRepository(session)   # Cria o Repository passando a Session

        service = LivroService(repository)  # Cria o Service passando o Repository

        yield service       # Entregue esse objeto para o endpoint, mas depois que o endpoint terminar, volte aqui para eu fazer a limpeza
                            # yield: retorna um valor temporariamente, pausando a execução da função.
                            # Quando a execução for retomada, ela continua a partir do yield.
                            
    finally:                # Executa de qualquer forma, mesmo que haja uma exceção
        session.close() # TEARDOWN