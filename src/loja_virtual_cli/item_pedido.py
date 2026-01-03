class ItemPedido:
    def __init__(self, sku, nome, preco, qtde):
        self.sku = sku
        self.nome = nome
        self.preco = preco
        self.qtde = qtde

    def subtotal(self):
        return self.preco * self.qtde

    def __str__(self):
        return f'SKU: {self.sku}, Nome: {self.nome}: {self.qtde} x R$ {self.subtotal():.2f}'
