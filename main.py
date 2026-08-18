from database import engine, Base
from biblioteca_carga_inicial import BibliotecaCargaInicial
from livro_service import LivroService
from livro import Livro

def cadastrar_livro():
    print("\n--- CADASTRAR LIVRO ---")

    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = int(input("Ano: "))

    livro = service.cadastrar_livro(
        titulo,
        autor,
        ano
    )

    print(f"Livro cadastrado com ID {livro.id}.")

def cadastrar_por_isbn():
    print("\n--- CADASTRAR POR ISBN ---")

    isbn = input("Digite o ISBN: ")

    print("Consultando API...")

    livro = service.cadastrar_por_isbn(isbn)

    if livro is None:
        print("Não foi possível encontrar o livro.")
        return

    print("\n--- LIVRO ENCONTRADO ---")
    livro.exibir()

    print("Livro cadastrado com sucesso!")

def listar_livros():
    print("\n--- LISTA DE LIVROS ---")

    livros = service.listar_livros()

    if not livros:
        print("Nenhum livro cadastrado.")
        return

    for livro in livros:
        livro.exibir()

def buscar_livro():
    print("\n--- BUSCAR LIVRO ---")
    print("Você pode buscar por: ")
    print("1 - Por Titulo")
    print("2 - Por Autor")
    print("3 - Por ID")

    buscarPor = int(input("Digite o índice do campo que deseja buscar: "))

    livros = []
    if buscarPor == 1:
        titulo = input("Título para buscar: ")
        livros = service.buscar_por_titulo(titulo)
    elif buscarPor == 2:
        autor = input("Autor(a) para buscar: ")
        livros = service.buscar_por_autor(autor)
    elif buscarPor == 3:
        id_livro = input("Id para buscar: ")
        livro = service.buscar_por_id(id_livro)
        if livro is not None:
            livros.append(livro)
    else:
        print("Opção não disponível")
        return

    if livros is None or len(livros) == 0:
        print("Nenhum livro encontrado.")
        return

    print("\n--- LIVROS ENCONTRADOS ---")
    for livro in livros:
        livro.exibir()

def buscar_livro_por_id(id_livro):
    print("\n--- BUSCAR LIVRO ---")

    try:
        livro = service.buscar_livro(id_livro)

        if livro is None:
            print("Livro não encontrado.")
            return

        livro.exibir()

    except ValueError:
        print("Digite um ID válido.")

def atualizar_livro():
    print("\n--- ATUALIZAR LIVRO ---")

    try:
        id_livro = int(input("Digite o ID: "))

        titulo = input("Novo título: ")
        autor = input("Novo autor: ")
        ano = int(input("Novo ano: "))

        sucesso = service.atualizar_livro(
            id_livro,
            titulo,
            autor,
            ano
        )

        if sucesso:
            print("Livro atualizado com sucesso!")
        else:
            print("Livro não encontrado.")

    except ValueError:
        print("Dados inválidos.")


def excluir_livro():
    print("\n--- EXCLUIR LIVRO ---")

    try:
        id_livro = int(input("Digite o ID: "))

        sucesso = service.excluir_livro(id_livro)

        if sucesso:
            print("Livro excluído com sucesso!")
        else:
            print("Livro não encontrado.")

    except ValueError:
        print("Digite um ID válido.")

def menu():

    while True:

        print("\n===== BIBLIOTECA =====")
        print("1 - Cadastrar livro manualmente")
        print("2 - Cadastrar livro por ISBN")
        print("3 - Listar livros")
        print("4 - Buscar livro")
        print("5 - Atualizar livro")
        print("6 - Excluir livro")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_livro()

        elif opcao == "2":
            cadastrar_por_isbn()

        elif opcao == "3":
            listar_livros()

        elif opcao == "4":
            buscar_livro()

        elif opcao == "5":
            atualizar_livro()

        elif opcao == "6":
            excluir_livro()

        elif opcao == "0":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    service = LivroService()
    biblioteca = BibliotecaCargaInicial()
    menu()