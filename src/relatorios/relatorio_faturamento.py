from datetime import date
from typing import List, Tuple

from src.repositorios.repositorio_pedidos import RepositorioPedidos
from src.utils.enums import StatusPedido
from src.modelos.pedido import Pedido


def gerar_relatorio_faturamento(
    repositorio: RepositorioPedidos,
    data_inicio: date,
    data_fim: date
) -> Tuple[float, List[Pedido]]:
    """
    Gera relatório de faturamento no período informado.

    Regras:
    - Considera apenas pedidos com status PAGO ou ENTREGUE
    - Usa a data de criação do pedido
    - Retorna o total faturado e a lista de pedidos considerados
    """

    if not isinstance(repositorio, RepositorioPedidos):
        raise TypeError("repositorio deve ser uma instância de RepositorioPedidos")

    if not isinstance(data_inicio, date) or not isinstance(data_fim, date):
        raise TypeError("data_inicio e data_fim devem ser do tipo date")

    if data_inicio > data_fim:
        raise ValueError("data_inicio não pode ser maior que data_fim")

    total_faturamento = 0.0
    pedidos_faturados = []

    for pedido in repositorio.listar_pedidos():
        data_pedido = pedido.data_criacao.date()

        if data_inicio <= data_pedido <= data_fim:
            if pedido.status in (StatusPedido.PAGO, StatusPedido.ENTREGUE):
                total_faturamento += pedido.total
                pedidos_faturados.append(pedido)

    return total_faturamento, pedidos_faturados
