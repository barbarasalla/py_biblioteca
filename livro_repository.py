from sqlalchemy import func
from sqlalchemy.orm import Session

from livro import Livro

class LivroRepository:

    def __init__(self, session: Session):  # Repositorio recebe uma sessão, assim ele não sabe qual banco tá usando, só entende "me deram uma Session. Vou usá-la", importante também para os testes, para passar um banco para teste apenas, por exemplo, em memória
        self.session = session 


    def salvar(self, livro):
        self.session.add(livro)
        self.session.commit()
        self.session.refresh(livro) # Isso é importante porque o banco gerou o ID

    def listar(self):                   # A função listar() faz: SELECT -> SQLite -> tuplas -> objeto Livro
        livros = self.session.query(Livro).all()
        return livros

    def buscar_por_id(self, id_livro):
        return self.session.get(Livro, id_livro)

    def buscar_por_autor(self, autor):
        livros = self.session.query(Livro).filter(
            func.lower(Livro.autor) == autor.lower()
        ).all()

        return livros

    def buscar_por_titulo(self, titulo):
        livros = self.session.query(Livro).filter(
            func.lower(Livro.titulo.ilike(f'%{titulo.lower()}%'))   # Buscar parcialmente pelo título
        )

        return livros.all()


    def excluir(self, id_livro):
        livro = self.session.get(Livro, id_livro)

        if livro is None:
            return False

        self.session.delete(livro)
        self.session.commit()

        return True

    def atualizar(self, livro):
        livro_banco = self.session.get(Livro, livro.id)

        if livro_banco is None: 
            return False

        livro_banco.titulo = livro.titulo
        livro_banco.autor = livro.autor
        livro_banco.ano = livro.ano

        self.session.commit()
        return True
        
    def existe_livros(self):
        livro = self.session.query(Livro).first()
        return livro is not None