import sqlite3

conexao = sqlite3.connect("biblioteca.db") # Cria o banco se ele não existir

cursor = conexao.cursor() # Cursor é o objeto que usamos para enviar comandos SQL ao banco

cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano INTEGER NOT NULL
    )
""") # Execute este SQL no banco.

cursor.execute("""
        INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)
    """, ("Clean Code", "Robert C. Martin", 2008)
    )

titulo = "A Montanha Magica"
autor = "Thomas Mann"
ano = 1924

cursor.execute("""
    INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)
""", (titulo, autor, ano))

cursor.execute("SELECT * FROM livros")
livros = cursor.fetchall()

for livro in livros:
    print(livro)

cursor.execute("SELECT ano FROM livros WHERE autor = ?", (autor,))
l = cursor.fetchall()

for li in l:
    print(li)

cursor.execute(
    """
    SELECT * FROM livros
    WHERE autor = :autor
    AND ano = :ano
    """,
    {
        "autor": autor,
        "ano": ano
    }
)
l2 = cursor.fetchall()

for li in l2:
    print(li)

conexao.commit()

conexao.close()