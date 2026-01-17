from collections import defaultdict
from src.utils.enums import StatusPedido
from src.utils.config import obter_top_n_produtos


def gerar_relatorio_top_n_produtos(pedidos, top_n=None):
    """
    Relatório de Top N produtos mais vendidos e ticket médio
    """

    if top_n is None:
        top_n = obter_top_n_produtos()

    vendas_por_produto = defaultdict(int)
    total_faturado = 0
    qtd_pedidos_validos = 0

    for pedido in pedidos:
        if pedido.status == StatusPedido.CANCELADO:
            continue

        total_faturado += pedido.total
        qtd_pedidos_validos += 1

        for item in pedido.itens:
            vendas_por_produto[item.nome] += item.quantidade

    top_produtos = sorted(
        vendas_por_produto.items(),
        key=lambda item: item[1],
        reverse=True
    )[:top_n]

    ticket_medio = (
        total_faturado / qtd_pedidos_validos
        if qtd_pedidos_validos > 0 else 0
    )

    return {
        "top_produtos": top_produtos,
        "ticket_medio": ticket_medio,
        "total_faturado": total_faturado,
        "qtd_pedidos": qtd_pedidos_validos
    }
