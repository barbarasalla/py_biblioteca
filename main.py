from database import engine, Base
from biblioteca_carga_inicial import BibliotecaCargaInicial
from livro_service import LivroService
from livro import Livro
from database import SessionLocal

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session = SessionLocal()
    service = LivroService(session)
    biblioteca = BibliotecaCargaInicial()