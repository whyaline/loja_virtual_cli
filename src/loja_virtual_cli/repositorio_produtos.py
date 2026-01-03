class RepositorioProdutos:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto: Produto):
        self.produtos.append(produto)

    def buscar_produto(self, sku):
        pass

    def listar_produtos(self):
        return self.produtos

    def remover_produto(self, produto: Produto):
        self.produtos.remove(produto)

    #persistência
    def salvar_dados(self):
        pass

    def carregar_dados(self):
        pass
