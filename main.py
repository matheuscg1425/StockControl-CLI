"""
StockControl CLI - Sistema de Controle de Estoque
Ponto de entrada do programa. Exibe o menu principal e direciona
o usuário para as funções corretas do módulo funcoes.py.
"""

from funcoes import (
    carregar_dados,
    salvar_dados,
    cadastrar_produto,
    listar_produtos,
    buscar_produto,
    editar_produto,
    excluir_produto,
)


def exibir_menu():
    print("\n===== StockControl - Sistema de Controle de Estoque =====")
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Buscar produto")
    print("4. Editar produto")
    print("5. Excluir produto")
    print("6. Salvar e sair")
    print("===========================================================")


def main():
    produtos = carregar_dados()
    print(f"{len(produtos)} produto(s) carregado(s) do arquivo dados.json.")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(produtos)
            salvar_dados(produtos)
        elif opcao == "2":
            listar_produtos(produtos)
        elif opcao == "3":
            buscar_produto(produtos)
        elif opcao == "4":
            editar_produto(produtos)
            salvar_dados(produtos)
        elif opcao == "5":
            excluir_produto(produtos)
            salvar_dados(produtos)
        elif opcao == "6":
            salvar_dados(produtos)
            print("Dados salvos. Até logo!")
            break
        else:
            print("Opção inválida. Escolha um número entre 1 e 6.")


if __name__ == "__main__":
    main()
