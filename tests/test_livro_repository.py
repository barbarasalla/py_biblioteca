from livro import Livro
from livro_repository import LivroRepository

# Testes de integração (LivroRepository -> SQLAlchemy -> SQLite :memory:)
# Verifica se as partes realmente conseguem trabalhar juntas

def test_salvar_livro(session_test):
    repository = LivroRepository(session_test)

    livro = Livro(
        titulo="Clean Code",
        autor="Robert C. Martin",
        ano=2008)

    repository.salvar(livro)

    assert livro.id is not None

def test_buscar_livro_por_id(session_test, livro):
    repository = LivroRepository(session_test)

    repository.salvar(livro)

    resultado = repository.buscar_por_id(livro.id)

    assert resultado is not None
    assert resultado.titulo=="Clean Code"
    assert resultado.autor=="Robert C. Martin"
    assert resultado.ano==2008

def test_buscar_livro_inexistente(session_test):

    repository = LivroRepository(session_test)

    resultado = repository.buscar_por_id(9999)

    assert resultado is None

def test_buscar_por_titulo(session_test, livro):
    repository = LivroRepository(session_test)

    repository.salvar(livro)
    
    resultado = repository.buscar_por_titulo(livro.titulo)

    assert resultado is not None
    assert resultado[0].titulo=="Clean Code"

def test_buscar_por_autor(session_test, livro):
    repository = LivroRepository(session_test)

    repository.salvar(livro)

    resultado = repository.buscar_por_autor(livro.autor)

    assert resultado is not None
    assert resultado[0].autor==livro.autor

def test_excluir(session_test, livro):
    repository=LivroRepository(session_test)

    repository.salvar(livro)

    resultado = repository.excluir(livro.id)

    assert resultado==True