class itemCarrinho:
    def __init__(self, produto: Produto, qtde):
        self.produto = produto
        self.qtde = qtde

    def adicionar_qtde(self, qtde):
        self.qtde += qtde #validar se qtde > estoque

    def remover_qtde(self, qtde):
        self.qtde -= qtde #validar: restante >=0

    def calcular_subtotal(self):
        return self.produto.preco * self.qtde

    #métodos especiais
    def __str__(self):
        return f'{self.produto.nome}, {self.qtde}'

    def __eq__(self):
        pass #verificar se o produto já está no carrinho e apenas aumentar sua quantidade

