from app.services.livro_service import LivroService
from unittest.mock import Mock
from app.models.livro import Livro

# Testes unitários (LivroService)

def test_cadastrar_livro():

    repository = Mock()
    service = LivroService(repository)

    livro = service.cadastrar_livro(
        "Clean Code",
        "Robert C. Martin",
        2008
    )

    assert livro.titulo=="Clean Code"
    assert livro.autor=="Robert C. Martin"
    assert livro.ano==2008

    repository.salvar.assert_called_once_with(livro) # A função salvar do repository foi chamada corretamente exatamente uma vez?

def test_listar_livros(livro):
    repository = Mock()

    livros = [livro, Livro(titulo="Livro A", autor="Autor A", ano=1900)]

    repository.listar.return_value = livros # Quando alguém chamar listar(), finja que o resultado é livros.

    service = LivroService(repository)

    resultado = service.listar_livros()

    assert resultado is not None
    assert resultado == livros

    repository.listar.assert_called_once()


def test_buscar_por_id():
    repository = Mock()

    livro = Livro(
        id=1,
        titulo="Clean Code",
        autor="Robert C. Martin",
        ano=2008
    )

    repository.buscar_por_id.return_value=livro

    service = LivroService(repository)

    resultado = service.buscar_por_id(1)

    assert resultado == livro

    repository.buscar_por_id.assert_called_once_with(1)

def test_buscar_por_id_livro_nao_encontrado():
    repository = Mock()

    repository.buscar_por_id.return_value = None

    service = LivroService(repository)

    resultado = service.buscar_por_id(999)

    assert resultado is None
    repository.buscar_por_id.assert_called_once_with(999)

def test_buscar_por_titulo(livro):
    repository = Mock()

    repository.buscar_por_titulo.return_value = livro

    service = LivroService(repository)

    resultado = service.buscar_por_titulo(livro.titulo)

    assert resultado.titulo==livro.titulo

    repository.buscar_por_titulo.assert_called_once_with(livro.titulo)

def test_buscar_por_autor(livro):
    repository = Mock()

    repository.buscar_por_autor.return_value=livro

    service = LivroService(repository)

    resultado = service.buscar_por_autor(livro.autor)

    assert resultado.autor==livro.autor

    repository.buscar_por_autor.assert_called_once_with(livro.autor)

def test_atualizar_livro(livro):
    repository = Mock()

    repository.buscar_por_id.return_value=livro
    repository.atualizar.return_value=True

    service = LivroService(repository)

    resultado = service.atualizar_livro(livro.id, "Novo Titulo", "Novo Autor", 1400)

    assert resultado==True

    repository.buscar_por_id.assert_called_once_with(livro.id)
    repository.atualizar.assert_called_once_with(livro)

def test_atualizar_livro_nao_encontrado():

    repository = Mock()

    repository.buscar_por_id.return_value = None

    service = LivroService(repository)

    resultado = service.atualizar_livro(
        999,
        "Novo título",
        "Novo autor",
        2025
    )

    assert resultado is False

    repository.atualizar.assert_not_called()


def test_excluir_livro():
    repository = Mock()

    repository.buscar_por_id.return_value=any
    repository.excluir.return_value=True

    service = LivroService(repository)

    resultado = service.excluir_livro(any)

    assert resultado==True

    repository.buscar_por_id.assert_called_once_with(any)
    repository.excluir.assert_called_once_with(any)

def test_excluir_livro_nao_encontrado():

    repository = Mock()

    repository.buscar_por_id.return_value = None

    service = LivroService(repository)

    resultado = service.excluir_livro(999)

    assert resultado is False

    repository.excluir.assert_not_called()