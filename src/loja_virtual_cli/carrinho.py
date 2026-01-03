class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item: itemCarrinho):
        #se já existir o produto apenas aumenta sua qtde
        self.itens.append(item)

    def remover_item(self, produto: Produto):
        self.itens.remove(item) #se qtde do item <=0 = retira do carrinho

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def listar_itens(self):
        if not self.itens:
            return "Carrinho vazio."
        
        linhas = []
        for i, item in enumerate(self.itens, start=1):
            linhas.append(f"{i} - {item.produto.nome} - Qtde: {item.qtde} - Subtotal: R$ {item.calcular_subtotal():.2f}")
        linhas.append(f"Total do carrinho: R$ {self.calcular_total():.2f}")
        return "\n".join(linhas)

    #métodos especiais
    def __str__(self):
        produtos = ["Carrinho:"]
        for produto in self.itens:
            produtos.append(str(produto))

        total = sum(item.calcular_subtotal() for item in self.itens)
        produtos.append(f"Total: R$ {total:.2f}")

        return "\n".join(produtos)

    def __len__(self):
        pass

