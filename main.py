from biblioteca import Biblioteca
from livro import Livro

def menu():

    while True:

        print("\n===== BIBLIOTECA =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Buscar")
        print("4 - Atualizar")
        print("5 - Excluir")
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

            biblioteca.salvar()

        elif opcao == "2":

            biblioteca.listar_livros()

        elif opcao == "3":

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

        elif opcao == "4":

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

            biblioteca.salvar()

        elif opcao == "5":

            id_livro = int(input("ID: "))

            biblioteca.excluir_livro(id_livro)

            biblioteca.salvar()

        elif opcao == "0":

            print("Programa encerrado.")
            break

        else:

            print("Opção inválida.")

if __name__ == "__main__":

    biblioteca = Biblioteca()
    biblioteca.carregar()
    menu()