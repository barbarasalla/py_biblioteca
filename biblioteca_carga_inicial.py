import json

from livro import Livro
from livro_repository import LivroRepository

class BibliotecaCargaInicial:

    def __init__(self):
        self.repository = LivroRepository()

        if not self.repository.existe_livros():
            self.carregar()

    def carregar(self):
        try:
            with open("biblioteca.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                livro = Livro.from_dict(item)
                livro.id = None
                self.repository.salvar(livro)

        except FileNotFoundError:
            print("Não foi possível carregar dados do arquivo 'biblioteca.json'!")


   

    



    