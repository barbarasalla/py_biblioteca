import json

from livro import Livro

class Biblioteca:

    def __init__(self):
        self.livros = []

        self.proximo_id = 1

    def salvar(self):
        dados = []

        for livro in self.livros:
            dados.append(livro.to_dict())

        with open("biblioteca.json", "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False, # Para não transformar caracteres especiais em códigos ASCII
                indent=4 # Define a indentação do JSON (4 espaços)
            )

    def carregar(self):
        try:
            with open("biblioteca.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.livros = []

            for item in dados:
                livro = Livro.from_dict(item)

                self.livros.append(livro)

            if self.livros:
                self.proximo_id = max(
                    livro.id for livro in self.livros
                ) + 1

        except FileNotFoundError:
            self.livros = []
            self.proximo_id = 1


    def adicionar_livro(self, titulo, autor, ano):

        # Cria um objeto Livro
        livro = Livro(
            self.proximo_id,
            titulo,
            autor,
            ano
        )

        # Adiciona o objeto à lista
        self.livros.append(livro)

        # Incrementa o ID para o próximo livro
        self.proximo_id += 1

        print(
            f"Livro '{titulo}' cadastrado com ID "
            f"{livro.id}."
        )


    def listar_livros(self):

        if not self.livros:
            print("Nenhum livro cadastrado.")
            return

        print("\n--- LIVROS ---")

        for livro in self.livros:
            livro.exibir()


    def buscar_livro_por_titulo(self, titulo):

        encontrados = []

        for livro in self.livros:

            if titulo.lower() in livro.titulo.lower():
                encontrados.append(livro)

        if not encontrados:
            print("Nenhum livro encontrado.")
            return

        print("\n--- LIVROS ENCONTRADOS ---")

        for livro in encontrados:
            livro.exibir()

    def buscar_por_autor(self, autor):

        encontrados = []

        for livro in self.livros:
            if autor.lower() in livro.autor.lower():
                encontrados.append(livro)

        if not encontrados:
            print(f"Nenhum livro encontrado para o autor {autor}")

        print("\n--- LIVROS ENCONTRADOS ---")
        for livro in encontrados:
            livro.exibir()


    def atualizar_livro(
        self,
        id_livro,
        novo_titulo,
        novo_autor,
        novo_ano
    ):

        for livro in self.livros:

            if livro.id == id_livro:

                livro.titulo = novo_titulo
                livro.autor = novo_autor
                livro.ano = novo_ano

                print("Livro atualizado com sucesso!")
                return

        print("Livro não encontrado.")

    def excluir_livro(self, id_livro):

        for livro in self.livros:

            if livro.id == id_livro:

                self.livros.remove(livro)

                print("Livro removido com sucesso!")
                return

        print("Livro não encontrado.")