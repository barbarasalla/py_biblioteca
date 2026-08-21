from app.models.livro import Livro
from app.repositories.livro_repository import LivroRepository
from app.apis.buscar_livro_api import buscar_livro_por_isbn

class LivroService:
    def __init__(self, repository):
        self.repository = repository

    def cadastrar_por_isbn(self, isbn):

        dados = buscar_livro_por_isbn(isbn)

        livro = Livro(
            titulo=dados["titulo"], autor=dados["autor"], ano=dados["ano"]
        )

        self.repository.salvar(livro)

        return livro

    def cadastrar_livro(self, titulo, autor, ano):
    
        # Cria um objeto Livro
        livro = Livro(
            titulo=titulo,
            autor=autor,
            ano=ano
        )

        self.repository.salvar(livro)
        return livro

    def listar_livros(self):
        return self.repository.listar()

    def buscar_por_id(self, id):
        return self.repository.buscar_por_id(id)

    def buscar_por_titulo(self, titulo):    
        return self.repository.buscar_por_titulo(titulo)
    
    def buscar_por_autor(self, autor):
        return self.repository.buscar_por_autor(autor)

    def atualizar_livro(
            self,
            id_livro,
            novo_titulo,
            novo_autor,
            novo_ano
        ):

        livro = self.repository.buscar_por_id(id_livro)

        if livro is None:
            return False

        livro.titulo = novo_titulo
        livro.autor = novo_autor
        livro.ano = novo_ano

        self.repository.atualizar(livro)

        return True
    
    def excluir_livro(self, id_livro):

        livro = self.repository.buscar_por_id(id_livro)

        if livro is None:
            return False

        self.repository.excluir(id_livro)

        return True