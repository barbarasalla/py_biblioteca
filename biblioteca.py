import json

from livro import Livro
from livro_repository import LivroRepository

class Biblioteca:

    def __init__(self):
        self.repository = LivroRepository()

    def carregar(self):
        try:
            with open("biblioteca.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                livro = Livro.from_dict(item)
                livro.id = None
                self.repository.salvar(livro)

        except FileNotFoundError:
            print("Nõa foi possível carregar dados do arquivo 'biblioteca.json'!")
            return


    def adicionar_livro(self, titulo, autor, ano):

        # Cria um objeto Livro
        livro = Livro(
            None,
            titulo,
            autor,
            ano
        )

        self.repository.salvar(livro)

        print(
            f"Livro '{titulo}' cadastrado com sucesso!"
        )

    def listar_livros(self):

        livros = self.repository.listar()

        if not livros:
            print("Nenhum livro cadastrado.")
            return

        print("\n--- LIVROS ---")

        for livro in livros:
            livro.exibir()

    def buscar_livro_por_titulo(self, titulo):

        encontrados = self.repository.buscar_por_titulo(titulo)

        if encontrados is None:
            print("Nenhum livro encontrado.")
            return

        print("\n--- LIVROS ENCONTRADOS ---")
        for livro in encontrados:
            livro.exibir()

    def buscar_por_autor(self, autor):

        encontrados = self.repository.buscar_por_autor(autor)

        if encontrados is None:
            print(f"Nenhum livro encontrado para o autor {autor}")
            return

        print("\n--- LIVROS ENCONTRADOS ---")
        for livro in encontrados:
            livro.exibir()

    def buscar_por_id(self, id):
        livro = self.repository.buscar_por_id(id)

        if livro is None:
            return None

        return livro

    def atualizar_livro(
        self,
        id_livro,
        novo_titulo,
        novo_autor,
        novo_ano
    ):
        livro = self.repository.buscar_por_id(id_livro)

        if livro is None:
            print("Livro não encontrado.")
            return

        livro.titulo = novo_titulo
        livro.autor = novo_autor
        livro.ano = novo_ano

        self.repository.atualizar(livro)

        print("Livro atualizado com sucesso!")

    def excluir_livro(self, id_livro):

        livro = self.repository.buscar_por_id(id_livro)

        if livro is None:
            print("Livro não encontrado.")
            return

        self.repository.excluir(id_livro)

        print(f"Livro '{livro.titulo}' removido com sucesso!")