class Pedido: #criar a partir do carrinho
    def __init__(self, id, cliente: Cliente, carrinho: Carrinho, endereco: Endereco, frete: Frete, desconto):
        self.id = id
        self.cliente = cliente
        self.itens = self._criar_itens(carrinho)
        self.endereco = endereco
        self.frete = frete
        self.desconto = desconto
        self.estado = StatusPedido.CRIADO
        self.total = self.calcular_total()
        self.pagamentos = []

    def _criar_itens(self, carrinho: Carrinho):
        itens = []
        for item in carrinho.itens:
            itens.append(
                ItemPedido(
                    sku = item.produto.sku,
                    nome = item.produto.nome,
                    preco = item.produto.preco,
                    qtde = item.qtde
                )
            )
        return itens

    def validar(self):
        if not self.itens:
            raise ValueError("O pedido deve conter pelo menos um item")
        
        if self.frete.valor < 0:
            raise ValueError("O valor do frete deve ser maior ou igual a zero")

        if self.desconto < 0:
            raise ValueError("O desconto deve ser maior ou igual a zero")

        if self.total < 0:
            raise ValueError("O total do pedido deve ser maior ou igual a zero")

    def calcular_total(self):
        subtotal = sum(item.subtotal() for item in self.itens)
        return subtotal + self.frete.valor - self.desconto

    def confirmar_pagamento(self, pagamento):
        self.pagamentos.append(pagamento)

        total_pago = sum(p.valor for p in self.pagamentos)
        if total_pago >= self.total:
            self.estado = StatusPedido.PAGO

    def cancelar(self):
        if self.estado not in [StatusPedido.CRIADO, StatusPedido.PAGO]:
            raise ValueError("Pedido não pode ser cancelado neste estado")

        self.estado = StatusPedido.CANCELADO

    def gerar_resumo(self):
        pass

    #métodos especiais
    def __str__(self):
        return
    
    def __repr__(self):
        pass

    #persistencia
    def to_dict(self):
        pass

    def from_dict(cls, dict):
        pass

    
    
