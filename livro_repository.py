from database import SessionLocal
from sqlalchemy import func

from livro import Livro

class LivroRepository:

    def salvar(self, livro):
        with SessionLocal() as session:
            session.add(livro)
            session.commit()
            session.refresh(livro) # Isso é importante porque o banco gerou o ID

    def listar(self):                   # A função listar() faz: SELECT -> SQLite -> tuplas -> objeto Livro
        with SessionLocal() as session:
            livros = session.query(Livro).all()
            return livros

    def buscar_por_id(self, id_livro):
        with SessionLocal() as session:
            return session.get(Livro, id_livro)

    def buscar_por_autor(self, autor):
        with SessionLocal() as session:
            livros = session.query(Livro).filter(
                func.lower(Livro.autor) == autor.lower()
            ).all()

            return livros

    def buscar_por_titulo(self, titulo):
        with SessionLocal() as session:
            livros = session.query(Livro).filter(
                func.lower(Livro.titulo.ilike(f'%{titulo.lower()}%'))   # Buscar parcialmente pelo título
            )

            return livros.all()


    def excluir(self, id_livro):
        with SessionLocal() as session:
            livro = session.get(Livro, id_livro)

            if livro is None:
                return False

            session.delete(livro)
            session.commit()

            return True

    def atualizar(self, livro):

        with SessionLocal() as session:
            livro_banco = session.get(Livro, livro.id)

            if livro_banco is None: 
                return False

            livro_banco.titulo = livro.titulo
            livro_banco.autor = livro.autor
            livro_banco.ano = livro.ano

            session.commit()
            return True
        
    def existe_livros(self):
        with SessionLocal() as session:
            livro = session.query(Livro).first()
            return livro is not None