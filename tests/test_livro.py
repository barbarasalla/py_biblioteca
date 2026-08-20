from livro import Livro

def test_criar_livro():
    livro = Livro(
        titulo="Livro 1",
        autor="Autor 1",
        ano=2000
    )
    assert livro.titulo=="Livro 1"
    assert livro.autor=="Autor 1"
    assert livro.ano==2000

# Testes utilizando objeto comum criado para contexto dos testes no arquivo configtest.py
# O pytest encontra automaticamente as fixtures definidas em conftest.py. sem precisar importar
def test_livro_titulo(livro):
    assert livro.titulo == "Clean Code"

def test_livro_autor(livro):
    assert livro.autor == "Robert C. Martin"

def test_livro_ano(livro):
    assert livro.ano == 2008