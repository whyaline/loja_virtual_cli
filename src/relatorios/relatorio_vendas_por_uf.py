from collections import defaultdict
from src.utils.enums import StatusPedido

def gerar_relatorio_vendas_por_uf(pedidos):
    vendas_por_uf = defaultdict(float)

    for pedido in pedidos:
        if pedido.status == StatusPedido.CANCELADO:
            continue

        uf = getattr(pedido.endereco, "uf", "OUTROS")
        vendas_por_uf[uf] += pedido.total

    return dict(vendas_por_uf)
