# src/cli/dispatcher.py
import sys
from src.cli.handler_clientes import handle_clientes
from src.cli.handler_produtos import handle_produtos
from src.cli.handler_pedidos import handle_pedidos
from src.cli.handler_relatorios import handle_relatorios
from src.cli.handler_seed import handle_seed

def dispatch(args):
    if len(args) < 2:
        print("Uso: loja <entidade> <comando> [opções]")
        return

    entidade = args[0].lower()
    comando_args = args[1:]

    if entidade == "cliente":
        handle_clientes(comando_args)
    elif entidade == "produto":
        handle_produtos(comando_args)
    elif entidade == "carrinho":
        handle_pedidos(comando_args)  # carrinho tratado junto de pedidos
    elif entidade == "pedido":
        handle_pedidos(comando_args)
    elif entidade == "relatorio":
        handle_relatorios(comando_args)
    elif entidade == "seed":
        handle_seed()
    else:
        print(f"Entidade '{entidade}' não reconhecida.")
