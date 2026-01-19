from src.cli.menu_cliente import menu_cliente
from src.cli.menu_produto import menu_produto
from src.cli.menu_carrinho import menu_carrinho
from src.cli.menu_pedido_cliente import menu_pedido_cliente
from src.cli.menu_pedido_admin import menu_pedido_admin
import src.sessao as Sessao

from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.repositorios.repositorio_clientes import RepositorioClientes
from src.repositorios.repositorio_pedidos import RepositorioPedidos

# =========================
# REPOSITÓRIOS
# =========================
repo_produtos = RepositorioProdutos()
repo_produtos.carregar_dados()

repo_clientes = RepositorioClientes()
repo_clientes.carregar_dados()

repo_pedidos = RepositorioPedidos()

# Dicionários auxiliares para carregar pedidos existentes
produtos_dict = {p.sku: p for p in repo_produtos.listar_produtos()}
clientes_dict = {c.id: c for c in repo_clientes.listar_clientes()}
enderecos_dict = {c.id: c.enderecos[0] for c in repo_clientes.listar_clientes() if c.enderecos}
carrinhos_dict = {}  # Carrinhos vazios

# Carrega pedidos do JSON usando os mesmos objetos de produtos e clientes
repo_pedidos.carregar_dados(clientes_dict, produtos_dict, carrinhos_dict, enderecos_dict)


# =========================
# MENU PRINCIPAL
# =========================
def menu_principal():
    while True:
        print("\n=== LOJA VIRTUAL ===")
        print("1 - Cliente")
        print("2 - Produto")
        print("3 - Carrinho")
        print("4 - Meus Pedidos (cliente)")
        print("5 - Gerenciar Pedidos (admin)")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cliente()
        elif opcao == "2":
            menu_produto()
        elif opcao == "3":
            if Sessao.cliente_atual is None:
                print("Selecione um cliente antes de acessar o carrinho.")
            elif Sessao.carrinho is None:
                print("Carrinho não iniciado. Selecione cliente para iniciar.")
            else:
                menu_carrinho(repo_pedidos)
        elif opcao == "4":
            if Sessao.cliente_atual is None:
                print("Nenhum cliente selecionado.")
            else:
                menu_pedido_cliente(repo_pedidos)  # Passa a mesma instância
        elif opcao == "5":
            menu_pedido_admin(repo_pedidos)    # Passa a mesma instância
        elif opcao == "0":
            print("Encerrando sistema.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
