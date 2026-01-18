from collections import defaultdict
from src.utils.enums import StatusPedido

def gerar_relatorio_vendas_por_categoria(pedidos):
    vendas_por_categoria = defaultdict(float)

    for pedido in pedidos:
        if pedido.status == StatusPedido.CANCELADO:
            continue

        for item in pedido.itens:
            categoria = getattr(item.produto, "categoria", "OUTROS")
            vendas_por_categoria[categoria] += item.subtotal

    return dict(vendas_por_categoria)
