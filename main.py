from biblioteca import Biblioteca
from livro import Livro
from buscar_livro_api import buscar_livro_por_isbn

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
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = int(input("Ano: "))

            biblioteca.adicionar_livro(
                titulo,
                autor,
                ano
            )

        elif opcao == "2":
            cadastrar_por_isbn()

        elif opcao == "3":

            biblioteca.listar_livros()

        elif opcao == "4":

            print("Você pode buscar por: ")
            print("1 - Por Titulo")
            print("2 - Por Autor")

            buscarPor = int(input("Digite o índice do campo que deseja buscar: "))

            if buscarPor == 1:
                titulo = input("Título para buscar: ")
                biblioteca.buscar_livro_por_titulo(titulo)

            elif buscarPor == 2:
                autor = input("Autor(a) para buscar: ")
                biblioteca.buscar_por_autor(autor)

            else:
                print("Opção não disponível")

        elif opcao == "5":

            id_livro = int(input("ID: "))
            titulo = input("Novo título: ")
            autor = input("Novo autor: ")
            ano = int(input("Novo ano: "))

            biblioteca.atualizar_livro(
                id_livro,
                titulo,
                autor,
                ano
            )

        elif opcao == "6":

            id_livro = int(input("ID: "))

            biblioteca.excluir_livro(id_livro)

        elif opcao == "0":

            print("Programa encerrado.")
            break

        else:

            print("Opção inválida.")

def cadastrar_por_isbn():
    isbn = input("Digite o ISBN: " )

    dados = buscar_livro_por_isbn(isbn)

    if dados is None:
        print("Não foi possível obter os dados do livro.")
        return

    print("\n--- LIVRO ENCONTRADO ---")

    print(f"Título: {dados['titulo']}")
    print(f"Autor: {dados['autor']}")
    print(f"Ano: {dados['ano']}")

    confirmar = input("\nDeseja cadastrar este livro? (s/n): ")

    if confirmar.lower() == "s":
        biblioteca.adicionar_livro(dados["titulo"], dados["autor"], dados["ano"])

if __name__ == "__main__":

    biblioteca = Biblioteca()
    biblioteca.carregar()
    menu()