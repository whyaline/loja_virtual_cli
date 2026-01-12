from src.modelos.produto import Produto

class ItemPedido:
    def __init__(self, produto, quantidade: int):
        if not isinstance(produto, Produto):
            raise TypeError("produto deve ser uma instância de Produto")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        if produto.preco <= 0:
            raise ValueError("O preço do produto deve ser maior que zero")

        self.produto = produto
        self.sku = produto.sku
        self.nome = produto.nome
        self.preco_unitario = produto.preco
        self.quantidade = quantidade

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f'SKU: {self.sku}, Nome: {self.nome}: {self.quantidade} x R$ {self.subtotal:.2f}'

    def __repr__(self):
        return f"ItemPedido(sku={self.sku!r}, nome={self.nome!r}, quantidade={self.quantidade!r}, preco_unitario={self.preco_unitario!r})"