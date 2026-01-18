# cli/menu_principal.py

from src.cli.menu_cliente import menu_cliente
from src.cli.menu_produto import menu_produto

def menu_principal():
    while True:
        print("\n=== LOJA VIRTUAL ===")
        print("1 - Cliente")
        print("2 - Produto")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cliente()
        elif opcao == "2":
            menu_produto()
        elif opcao == "0":
            print("Encerrando sistema.")
            break
        else:
            print("Opção inválida.")
