from collections import defaultdict
from src.utils.enums import StatusPedido


def gerar_relatorio_vendas(pedidos, top_n=5):
    """
    Gera relatório de:
    - Top N produtos mais vendidos (por quantidade)
    - Ticket médio (pedidos não cancelados)
    """

    vendas_por_produto = defaultdict(int)
    total_faturado = 0
    qtd_pedidos_validos = 0

    for pedido in pedidos:
        if pedido.status == StatusPedido.CANCELADO:
            continue

        # ticket médio
        total_faturado += pedido.total
        qtd_pedidos_validos += 1

        # contagem de produtos
        for item in pedido.itens:
            vendas_por_produto[item.nome] += item.quantidade

    # ordena do mais vendido para o menos vendido
    top_produtos = sorted(
        vendas_por_produto.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    ticket_medio = (
        total_faturado / qtd_pedidos_validos
        if qtd_pedidos_validos > 0 else 0
    )

    return top_produtos, ticket_medio
