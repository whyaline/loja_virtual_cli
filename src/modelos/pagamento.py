from datetime import datetime
from src.utils.enums import FormaPagamento, StatusPagamento
from src.modelos.pedido import Pedido

class Pagamento:
    def __init__(self, pedido, valor: float, forma: FormaPagamento, data=None):
        #verifica se os valores e tipos são válidos para criar a instância
        if valor <= 0:
            raise ValueError("O valor do pagamento deve ser positivo")

        if not isinstance(pedido, Pedido):
            raise TypeError("Pagamento precisa estar associado a um Pedido")

        if not isinstance(forma, FormaPagamento):
            raise ValueError("Forma de pagamento inválida")

        self.pedido = pedido
        self.valor = valor
        self.forma = forma
        self.data = data or datetime.now()
        self.status = StatusPagamento.PENDENTE # usando o enum para o status

    #processar o pagamento, alterando o status de pendente pra confirmado
    def processar(self):
        if self.status != StatusPagamento.PENDENTE:
            print(f"Pagamento de R$ {self.valor:.2f} já processado ou em outro estado ({self.status.value}).")
            return False

        self.status = StatusPagamento.CONFIRMADO
        print(f"Pagamento de R$ {self.valor:.2f} processado com sucesso via {self.forma.value}.")
        return True

    #regras de estorno: só realiza se o pagamento estiver confirmado
    def estornar(self):
        if self.status == StatusPagamento.ESTORNADO:
            raise ValueError("Pagamento já estornado")
        if self.status != StatusPagamento.CONFIRMADO:
            raise ValueError(f"Não é possível estornar um pagamento com status {self.status.value}")

        self.status = StatusPagamento.ESTORNADO
        print(f"Estorno realizado: R$ {self.valor:.2f} - Forma: {self.forma.value}")

    #regras de cancelamento: só cancela se estiver pendente, se já tiver sido pago deve solicitar o estorno
    def cancelar_pagamento(self):
        if self.status == StatusPagamento.CANCELADO:
            raise ValueError("Pagamento já cancelado")
        if self.status != StatusPagamento.PENDENTE:
            raise ValueError(f"Não é possível cancelar um pagamento com status {self.status.value}")

        self.status = StatusPagamento.CANCELADO
        print(f"Pagamento cancelado: R$ {self.valor:.2f} - Forma: {self.forma.value}")

    # persistência
    def to_dict(self):
        return {
            "pedido_id": self.pedido.id,
            "valor": self.valor,
            "forma": self.forma.value,
            "data": self.data.isoformat(),
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict, pedido: 'Pedido'):
        # o pedido deve ser fornecido externamente ao recriar o pagamento
        pagamento = cls(
            pedido=pedido,
            valor=data["valor"],
            forma=FormaPagamento[data["forma"]],
            data=datetime.fromisoformat(data["data"])
        )
        # atualização do status após a criação
        pagamento.status = StatusPagamento[data['status']]
        return pagamento