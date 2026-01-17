from datetime import datetime, timedelta

from src.modelos.cliente import Cliente
from src.modelos.endereco import Endereco
from src.modelos.produto import ProdutoFisico
from src.modelos.item_carrinho import ItemCarrinho
from src.modelos.carrinho import Carrinho
from src.modelos.pedido import Pedido

from src.repositorios.repositorio_pedidos import RepositorioPedidos
from src.utils.enums import StatusPedido

from collections import defaultdict

from src.relatorios.relatorio_vendas_por_categoria import gerar_relatorio_vendas_por_categoria
from src.relatorios.relatorio_vendas_por_uf import gerar_relatorio_vendas_por_uf


def criar_pedido_teste(nome_produto, categoria, preco, qtde, uf, status, dias_atras):
    cliente = Cliente(
        nome="Cliente Teste",
        cpf=12345678901,
        email="teste@email.com"
    )

    endereco = Endereco(
        cidade="Cidade Teste",
        uf=uf,
        cep=63000000
    )

    produto = ProdutoFisico(
        nome=nome_produto,
        categoria=categoria,
        preco=preco,
        estoque=100,
        ativo=True,
        peso=1.0
    )

    item = ItemCarrinho(produto=produto, qtde=qtde)

    carrinho = Carrinho()
    carrinho.adicionar_item(item)

    pedido = Pedido(cliente, endereco, carrinho)
    pedido.status = status
    pedido.data_criacao = datetime.now() - timedelta(days=dias_atras)

    return pedido


def main():
    repositorio = RepositorioPedidos()

    pedidos_teste = [
        criar_pedido_teste("Teclado", "PERIFERICOS", 150.00, 1, "CE", StatusPedido.PAGO, 5),
        criar_pedido_teste("Mouse", "PERIFERICOS", 100.00, 2, "CE", StatusPedido.ENTREGUE, 3),
        criar_pedido_teste("Monitor", "INFORMATICA", 900.00, 1, "PE", StatusPedido.PAGO, 2),
        criar_pedido_teste("Notebook", "INFORMATICA", 3500.00, 1, "CE", StatusPedido.CANCELADO, 1),
        criar_pedido_teste("Mouse", "PERIFERICOS", 100.00, 1, "PE", StatusPedido.PAGO, 1),
    ]

    for pedido in pedidos_teste:
        repositorio.adicionar_pedido(pedido)

    pedidos = repositorio.listar_pedidos()

    # Relatório por categoria
    vendas_categoria = gerar_relatorio_vendas_por_categoria(pedidos)

    print("\nRELATÓRIO DE VENDAS POR CATEGORIA\n")
    for categoria, total in vendas_categoria.items():
        print(f"{categoria}: R$ {total:.2f}")

    # Relatório por UF
    vendas_uf = gerar_relatorio_vendas_por_uf(pedidos)

    print("\nRELATÓRIO DE VENDAS POR UF\n")
    for uf, total in vendas_uf.items():
        print(f"{uf}: R$ {total:.2f}")


if __name__ == "__main__":
    main()
