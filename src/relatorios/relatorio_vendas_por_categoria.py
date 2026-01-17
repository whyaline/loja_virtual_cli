from collections import defaultdict
from src.utils.enums import StatusPedido


def gerar_relatorio_vendas_por_categoria(pedidos):
    """
    Gera o total de vendas por categoria de produto.
    Considera apenas pedidos não cancelados.
    """

    vendas_por_categoria = defaultdict(float)

    for pedido in pedidos:
        if pedido.status == StatusPedido.CANCELADO:
            continue

        for item in pedido.itens:
            categoria = item.produto.categoria
            vendas_por_categoria[categoria] += item.subtotal

    return vendas_por_categoria
