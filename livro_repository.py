import sqlite3

from livro import Livro

class LivroRepository:
    def __init__(self):
        self.conexao = sqlite3.connect("biblioteca.db")  # Cria o banco se ele não existir
        self.criar_tabela()

    def criar_tabela(self):

        cursor = self.conexao.cursor() # Cursor é o objeto que usamos para enviar comandos SQL ao banco

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano TEXT NOT NULL)
        """)

        self.conexao.commit()

    def salvar(self, livro):
        cursor = self.conexao.cursor()

        cursor.execute("""
            INSERT INTO livros (titulo, autor, ano) VALUES(?, ?, ?)
        """, (livro.titulo, livro.autor, livro.ano))

        self.conexao.commit()

    def listar(self):                   # A função listar() faz: SELECT -> SQLite -> tuplas -> objeto Livro
        cursor = self.conexao.cursor()

        cursor.execute("SELECT * FROM livros")

        registros = cursor.fetchall()

        livros = []

        for registro in registros:
            livro = Livro(registro[0], registro[1], registro[2], registro[3])
            livros.append(livro)

        return livros

    def buscar_por_id(self, id):
        cursor = self.conexao.cursor()

        cursor.execute("SELECT * FROM livros WHERE id = (:id)", {"id": id})

        registro = cursor.fetchone()

        if registro is None:
            return None

        return Livro(registro[0], registro[1], registro[2], registro[3])

    def buscar_por_autor(self, autor):
        cursor = self.conexao.cursor()

        cursor.execute("SELECT * FROM livros WHERE LOWER(autor) = ?", (autor.lower(),))

        registros = cursor.fetchall()

        if registros is None:
            return None

        livros = []
        for registro in registros:
            livro = Livro(registro[0], registro[1], registro[2], registro[3]) 
            livros.append(livro)

        return livros

    def buscar_por_titulo(self, titulo):
        cursor = self.conexao.cursor()

        cursor.execute(
            "SELECT * FROM livros WHERE LOWER(titulo) = LOWER(:titulo)",
            {"titulo": titulo}
        )

        registros = cursor.fetchall()

        if registros is None: 
            return None

        livros = []
        for registro in registros:
            livro = Livro(registro[0], registro[1], registro[2], registro[3]) 
            livros.append(livro)

        return livros


    def excluir(self, id):
        cursor = self.conexao.cursor()

        cursor.execute("DELETE FROM livros WHERE id = ?", (id,)) # (id,) Isso é uma tupla de um elemento.

        self.conexao.commit()

    def atualizar(self, livro):
        cursor = self.conexao.cursor()

        cursor.execute("""
            UPDATE livros SET titulo = ?,
            autor = ?,
            ano = ?
            WHERE id = ?
        """, (livro.titulo, livro.autor, livro.ano, livro.id))

        self.conexao.commit()

    def existe_livros(self):
        cursor = self.conexao.cursor()

        cursor.execute("SELECT 1 FROM livros LIMIT 1")

        return cursor.fetchone() is not None

    def fechar(self):
        self.conexao.close()
