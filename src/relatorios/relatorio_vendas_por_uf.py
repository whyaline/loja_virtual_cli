from collections import defaultdict
from src.utils.enums import StatusPedido


def gerar_relatorio_vendas_por_uf(pedidos):
    """
    Gera o total de vendas por UF (estado).
    Considera apenas pedidos não cancelados.
    """

    vendas_por_uf = defaultdict(float)

    for pedido in pedidos:
        if pedido.status == StatusPedido.CANCELADO:
            continue

        vendas_por_uf[pedido.endereco.uf] += pedido.total

    return vendas_por_uf
