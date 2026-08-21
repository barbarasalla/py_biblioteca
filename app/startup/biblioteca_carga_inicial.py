import json

from app.database.database import SessionLocal
from app.models.livro import Livro
from app.repositories.livro_repository import LivroRepository
from app.config import settings

class BibliotecaCargaInicial:

    def __init__(self, repository):
        self.repository = repository

        if not self.repository.existe_livros():
            self.carregar()

    def carregar(self):
        try:
            with open(settings.biblioteca_json, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                livro = Livro.from_dict(item)
                livro.id = None
                self.repository.salvar(livro)

        except FileNotFoundError:
            print("Não foi possível carregar dados do arquivo 'biblioteca.json'!")


def carregar_biblioteca():

    session = SessionLocal()

    try:
        repository = LivroRepository(session)

        BibliotecaCargaInicial(repository)

    finally:
        session.close()