from src.utils.validacoes import validar_numero
from src.modelos.produto import Produto

class ItemCarrinho:
    def __init__(self, produto: Produto, qtde: int):
        validar_numero(qtde, "Quantidade", tipo=int, permitir_zero=False)

        if qtde > produto.estoque:
            raise ValueError(f"Quantidade solicitada ({qtde}) é maior que o estoque disponível ({produto.estoque})")

        self.produto = produto
        self.qtde = qtde

    def adicionar_qtde(self, qtde): #validar se qtde > estoque
        validar_numero(qtde, "Quantidade", tipo=int, permitir_zero=False)

        if self.qtde + qtde > self.produto.estoque:
            raise ValueError(f"Quantidade solicitada ({qtde}) é maior que o estoque disponível ({self.produto.estoque})")

        self.qtde += qtde

    def remover_qtde(self, qtde):
        validar_numero(qtde, "Quantidade", tipo=int, permitir_zero=False)

        if self.qtde - qtde < 0:
            raise ValueError(f"Quantidade não pode ser negativa")

        self.qtde -= qtde #validar: restante >=0

    def calcular_subtotal(self):
        return self.produto.preco * self.qtde

    #métodos especiais
    def __str__(self):
        return (f'Produto: {self.produto.nome}, '
                f'Preço unitário: {self.produto.preco}, '
                f'Quantidade: {self.qtde}, '
                f'Subtotal: {self.calcular_subtotal()}'
        )

    def __repr__(self):
        return (f"ItemCarrinho(produto={self.produto!r}, qtde={self.qtde!r})")

    def __eq__(self, outro):
        if not isinstance(outro, ItemCarrinho):
            return NotImplemented

        return self.produto.sku == outro.produto.sku