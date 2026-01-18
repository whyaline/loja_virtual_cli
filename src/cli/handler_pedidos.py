# src/cli/handler_pedidos.py
from src.repositorios.repositorio_pedidos import RepositorioPedidos
from src.repositorios.repositorio_clientes import RepositorioClientes
from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.modelos.carrinho import Carrinho
from src.modelos.pedido import Pedido
from src.modelos.pagamento import Pagamento
from src.utils.enums import StatusPagamento

repo_clientes = RepositorioClientes()
repo_clientes.carregar_dados()

repo_produtos = RepositorioProdutos()
repo_produtos.carregar_dados()

repo_pedidos = RepositorioPedidos()
# opcional: carregar pedidos de JSON se implementar persistência
# repo_pedidos.carregar_dados()

carrinhos = {}  # carrinho por cliente_id

def handle_pedidos(args):
    if not args:
        print("Comando de pedidos não especificado")
        return

    comando = args[0].lower()

    if comando == "add":
        cliente_id = int(args[1])
        sku = int(args[2])
        qtde = int(args[3])

        cliente = repo_clientes.buscar_cliente_por_id(cliente_id)
        produto = repo_produtos.buscar_produto_por_sku(sku)

        if cliente is None or produto is None:
            print("Cliente ou produto não encontrado")
            return

        if cliente_id not in carrinhos:
            carrinhos[cliente_id] = Carrinho()
        carrinhos[cliente_id].adicionar_item(produto, qtde)
        print(f"Produto {produto.nome} adicionado ao carrinho do cliente {cliente.nome}")

    elif comando == "listar":
        cliente_id = int(args[1])
        if cliente_id not in carrinhos:
            print("Carrinho vazio")
            return
        print(carrinhos[cliente_id])

    elif comando == "fechar":
        cliente_id = int(args[1])
        cliente = repo_clientes.buscar_cliente_por_id(cliente_id)
        if cliente_id not in carrinhos:
            print("Carrinho vazio")
            return
        carrinho = carrinhos.pop(cliente_id)
        pedido = Pedido(cliente, cliente.endereco, carrinho)
        repo_pedidos.adicionar_pedido(pedido)
        print(f"Pedido {pedido.id} criado para cliente {cliente.nome}")

    elif comando == "pagar":
        pedido_id = int(args[1])
        pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
        if pedido is None:
            print("Pedido não encontrado")
            return
        pagamento = Pagamento(pedido.total, StatusPagamento.CONFIRMADO)
        pedido.registrar_pagamento(pagamento)
        print(f"Pedido {pedido.id} pago!")

    elif comando == "enviar":
        pedido_id = int(args[1])
        pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
        if pedido is None:
            print("Pedido não encontrado")
            return
        pedido.enviar()

    elif comando == "entregar":
        pedido_id = int(args[1])
        pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
        if pedido is None:
            print("Pedido não encontrado")
            return
        pedido.entregar()
        print(f"Pedido {pedido.id} entregue!")

    elif comando == "cancelar":
        pedido_id = int(args[1])
        pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
        if pedido is None:
            print("Pedido não encontrado")
            return
        pedido.cancelar()
        print(f"Pedido {pedido.id} cancelado!")

    else:
        print(f"Comando '{comando}' não reconhecido para pedidos/carrinho")
