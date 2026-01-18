from src.cli.menu_cliente import menu_cliente
from src.cli.menu_produto import menu_produto
from src.cli.menu_carrinho import menu_carrinho
import src.sessao as Sessao


def menu_principal():
    while True:
        print("\n=== LOJA VIRTUAL ===")
        print("1 - Cliente")
        print("2 - Produto")

        if Sessao.cliente_atual is not None:
            print("3 - Carrinho")

        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cliente()

        elif opcao == "2":
            menu_produto()

        elif opcao == "3" and Sessao.carrinho is not None:
            menu_carrinho()

        elif opcao == "0":
            print("Encerrando sistema.")
            break

        else:
            print("Opção inválida.")
