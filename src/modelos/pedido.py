from datetime import datetime, timedelta
import random
import string

from src.modelos.item_pedido import ItemPedido
from src.modelos.pagamento import Pagamento
from src.modelos.produto import ProdutoFisico

from src.utils.enums import StatusPagamento, StatusPedido
from src.utils.validacoes import validar_numero
from src.utils.config import obter_janela_cancelamento_horas

class Pedido:
    def __init__(self, cliente, endereco, carrinho, frete_valor=0, desconto=0):
        if not carrinho.itens:
            raise ValueError("O carrinho está vazio")

        self.__id = None
        self.cliente = cliente
        self.endereco = endereco
        self.itens = [ItemPedido(produto=item.produto, quantidade=item.qtde) for item in carrinho.itens]
        self.frete_valor = frete_valor
        self.desconto = desconto
        self.status = StatusPedido.CRIADO
        self.data_criacao = datetime.now()
        self.pagamentos = []
        self.codigo_rastreio = None
        self.data_entrega = None

    @property
    def id(self):
        return self.__id

    def _definir_id(self, id):
        if self.__id is not None:
            raise ValueError("ID já definido para o pedido")
        validar_numero(id, "ID do Pedido", tipo=int, permitir_zero=False)
        self.__id = id

    @property
    def total_produtos(self):
        return sum(item.subtotal for item in self.itens)

    @property
    def total(self):
        return max(self.total_produtos + self.frete_valor - self.desconto, 0)

    def pagar(self):
        if self.status != StatusPedido.CRIADO:
            raise ValueError("Só é possível pagar um pedido que está CRIADO")
        self.status = StatusPedido.PAGO

    def registrar_pagamento(self, pagamento: 'Pagamento'):
        if self.status in (StatusPedido.ENTREGUE, StatusPedido.CANCELADO):
            raise ValueError("Não é possível pagar um pedido finalizado ou cancelado")

        self.pagamentos.append(pagamento)

        total_pago = sum(p.valor for p in self.pagamentos if p.status == StatusPagamento.CONFIRMADO)
        if total_pago >= self.total and self.status == StatusPedido.CRIADO:
            self.status = StatusPedido.PAGO



    def cancelar(self):
        if self.status not in (StatusPedido.CRIADO, StatusPedido.PAGO):
            raise ValueError("Pedido não pode ser cancelado neste estado")

        janela_horas = obter_janela_cancelamento_horas()
        limite = self.data_criacao + timedelta(hours=janela_horas)

        if datetime.now() > limite:
            raise ValueError(
                f"Cancelamento permitido apenas até {janela_horas}h após a criação do pedido"
            )

        self.status = StatusPedido.CANCELADO

        # reposição de estoque
        for item in self.itens:
            if isinstance(item.produto, ProdutoFisico):
                item.produto.adicionar_estoque(item.quantidade)

        # estorno financeiro
        for pagamento in self.pagamentos:
            if pagamento.status == StatusPagamento.CONFIRMADO:
                pagamento.estornar()
            elif pagamento.status == StatusPagamento.PENDENTE:
                pagamento.cancelar_pagamento()

    def _gerar_codigo_rastreio(self, length=13):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def enviar(self):
        if self.status != StatusPedido.PAGO:
            raise ValueError("Só é possível enviar um pedido que está PAGO")
        self.status = StatusPedido.ENVIADO
        self.codigo_rastreio = self._gerar_codigo_rastreio() # gera o código de rastreio
        print(f"Pedido {self.id} enviado. Código de rastreio: {self.codigo_rastreio}")

    def entregar(self, data_entrega: datetime = None):
        if self.status != StatusPedido.ENVIADO:
            raise ValueError("Só é possível entregar um pedido que está ENVIADO")
        self.status = StatusPedido.ENTREGUE
        self.data_entrega = data_entrega or datetime.now() # registra a data de entrega

    def resumo(self):
        endereco = self.endereco
        endereco_str = f"{endereco.cidade}-{endereco.uf}, CEP: {endereco.cep}"

        linhas = [
            f"Pedido ID: {self.id}",
            f"Pedido - Status: {self.status.value}"
        ]
        if self.codigo_rastreio:
            linhas.append(f"Código de Rastreio: {self.codigo_rastreio}")
        if self.data_entrega:
            linhas.append(f"Data de Entrega: {self.data_entrega.strftime('%d/%m/%Y %H:%M')}")

        linhas.extend([
            f"Cliente: {self.cliente.nome}",
            f"Endereço: {endereco_str}",
            "Itens:"
        ])
        for item in self.itens:
            linhas.append(f"  {item}")
        linhas.append(f"Subtotal produtos: R$ {self.total_produtos:.2f}")
        linhas.append(f"Frete: R$ {self.frete_valor:.2f}")
        linhas.append(f"Desconto: R$ {self.desconto:.2f}")
        linhas.append(f"Total: R$ {self.total:.2f}")
        return "\n".join(linhas)


    #métodos especiais
    def __str__(self):
        return self.resumo()

    def __repr__(self):
        return (f"Pedido(id={self.id!r}, cliente={self.cliente!r}, itens={self.itens!r}, "
                f"frete_valor={self.frete_valor}, desconto={self.desconto})")

    #persistencia
    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente.id,
            "itens": [
                {"sku": item.sku, "nome": item.nome, "quantidade": item.quantidade, "preco_unitario": item.preco_unitario}
                for item in self.itens
            ],
            "frete_valor": self.frete_valor,
            "desconto": self.desconto,
            "status": self.status.value,
            "data_criacao": self.data_criacao.isoformat(),
            "codigo_rastreio": self.codigo_rastreio,
            "data_entrega": self.data_entrega.isoformat() if self.data_entrega else None,
            "total": self.total
        }

    @classmethod
    def from_dict(cls, data, cliente, endereco, carrinho):
        pedido = cls(cliente, carrinho, frete_valor=data["frete_valor"], desconto=data["desconto"])
        pedido._definir_id(data["id"])
        pedido.status = StatusPedido(data["status"])
        pedido.data_criacao = datetime.fromisoformat(data["data_criacao"])
        pedido.codigo_rastreio = data.get("codigo_rastreio")
        if data.get("data_entrega"):
            pedido.data_entrega = datetime.fromisoformat(data["data_entrega"])
        return pedido