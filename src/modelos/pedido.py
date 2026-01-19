from datetime import datetime, timedelta
import random
import string

from src.modelos.item_pedido import ItemPedido
from src.modelos.pagamento import Pagamento

from src.utils.enums import StatusPagamento, StatusPedido
from src.utils.validacoes import validar_numero
from src.utils.config import obter_janela_cancelamento_horas


class Pedido:
    def __init__(self, cliente, endereco, carrinho=None, itens=None, frete_valor=0, desconto=0):
        """
        Cria um pedido.
        - carrinho: usado no fluxo normal de criação de pedido.
        - itens: usado ao reconstruir pedido do JSON.
        """
        self.__id = None
        self.cliente = cliente
        self.endereco = endereco
        self.frete_valor = frete_valor
        self.desconto = desconto
        self.status = StatusPedido.CRIADO
        self.data_criacao = datetime.now()
        self.pagamentos = []
        self.codigo_rastreio = None
        self.data_entrega = None

        if itens is not None:
            self.itens = itens
        elif carrinho is not None and carrinho.itens:
            self.itens = [ItemPedido(produto=item.produto, quantidade=item.qtde) for item in carrinho.itens]
        else:
            raise ValueError("O pedido deve ter itens")

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

    # ===============================
    # PAGAMENTO
    # ===============================
    def registrar_pagamento(self, pagamento: 'Pagamento'):
        if self.status in (StatusPedido.ENTREGUE, StatusPedido.CANCELADO):
            raise ValueError("Não é possível pagar um pedido finalizado ou cancelado")

        self.pagamentos.append(pagamento)

        if self.total_pago >= self.total and self.status == StatusPedido.CRIADO:
            self.status = StatusPedido.PAGO

    @property
    def total_pago(self):
        return sum(p.valor for p in self.pagamentos if p.status == StatusPagamento.CONFIRMADO)

    @property
    def saldo_devedor(self):
        return max(self.total - self.total_pago, 0)

    # ===============================
    # CANCELAMENTO
    # ===============================
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

        mensagens_estorno = []
        for pagamento in self.pagamentos:
            if pagamento.status == StatusPagamento.CONFIRMADO:
                pagamento.estornar()
                mensagens_estorno.append(f"Estorno realizado: R$ {pagamento.valor:.2f} - Forma: {pagamento.forma.value}")
            elif pagamento.status == StatusPagamento.PENDENTE:
                pagamento.cancelar_pagamento()
                mensagens_estorno.append(f"Pagamento pendente cancelado: R$ {pagamento.valor:.2f} - Forma: {pagamento.forma.value}")

        for msg in mensagens_estorno:
            print(msg)

    # ===============================
    # ENVIO E ENTREGA
    # ===============================
    def _gerar_codigo_rastreio(self, length=13):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def enviar(self):
        if self.saldo_devedor > 0:
            raise ValueError(f"Não é possível enviar. Pagamento incompleto. Falta R$ {self.saldo_devedor:.2f}")
        if self.status != StatusPedido.PAGO:
            raise ValueError("Só é possível enviar um pedido que está PAGO")
        self.status = StatusPedido.ENVIADO
        self.codigo_rastreio = self._gerar_codigo_rastreio()
        print(f"Pedido {self.id} enviado. Código de rastreio: {self.codigo_rastreio}")

    def entregar(self, data_entrega: datetime = None):
        if self.status != StatusPedido.ENVIADO:
            raise ValueError("Só é possível entregar um pedido que está ENVIADO")
        self.status = StatusPedido.ENTREGUE
        self.data_entrega = data_entrega or datetime.now()

    # ===============================
    # RESUMO
    # ===============================
    def resumo(self):
        endereco_str = f"{self.endereco.cidade}-{self.endereco.uf}, CEP: {self.endereco.cep}"

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
        linhas.append(f"Total pago: R$ {self.total_pago:.2f}")
        if self.saldo_devedor > 0:
            linhas.append(f"Saldo restante: R$ {self.saldo_devedor:.2f}")
        return "\n".join(linhas)

    def __str__(self):
        return self.resumo()

    def __repr__(self):
        return (f"Pedido(id={self.id!r}, cliente={self.cliente!r}, itens={self.itens!r}, "
                f"frete_valor={self.frete_valor}, desconto={self.desconto})")

    # ===============================
    # PERSISTÊNCIA
    # ===============================
    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente.id,
            "endereco": self.endereco.to_dict(),
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
            "total": self.total,
            # ====== Adiciona os pagamentos ======
            "pagamentos": [pg.to_dict() for pg in self.pagamentos]
        }

    @classmethod
    def from_dict(cls, data, cliente, endereco, produtos_dict):
        itens = []
        for item_data in data["itens"]:
            sku = item_data["sku"]
            produto = produtos_dict.get(sku)
            if not produto:
                raise ValueError(f"Produto com SKU {sku} não encontrado para recriar ItemPedido")
            itens.append(ItemPedido(
                produto=produto,
                quantidade=item_data["quantidade"]
            ))

        pedido = cls(cliente, endereco, itens=itens,
                    frete_valor=data.get("frete_valor", 0),
                    desconto=data.get("desconto", 0))
        pedido._definir_id(data["id"])
        pedido.status = StatusPedido(data["status"])
        pedido.data_criacao = datetime.fromisoformat(data["data_criacao"])
        pedido.codigo_rastreio = data.get("codigo_rastreio")
        if data.get("data_entrega"):
            pedido.data_entrega = datetime.fromisoformat(data["data_entrega"])

        # ===== Reconstruir pagamentos do JSON =====
        for pg_data in data.get("pagamentos", []):
            from src.modelos.pagamento import Pagamento
            from src.utils.enums import FormaPagamento, StatusPagamento

            pg = Pagamento.from_dict(pg_data, pedido)
            pedido.pagamentos.append(pg)

        return pedido
