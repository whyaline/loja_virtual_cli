class Frete:
    def __init__(self, endereco: Endereco):
        self.endereco = Endereco
        self.valor = 0
        self.prazo = 0

    def calcular_valor(self, carrinho: Carrinho, tabela_frete):
        total = 0

        for item in carrinho.itens:
            produto = item.produto

            # só produtos físicos geram frete
            if isinstance(produto, ProdutoFisico):
                regra = tabela_frete.get(self.endereco.uf)

                if regra:
                    total += regra["valor"] * item.qtde
                else:
                    total += 15 * item.qtde  # valor padrão
        self.valor = total
        return self.valor

    def calcular_prazo(self, tabela_frete):
        pass
