class Produto:
    def __init__(self, sku, nome, categoria, preco, estoque, ativo):
        self.sku = sku #unico
        self.nome = nome #validar - não vazio
        self.categoria = categoria #validar - não vazia
        self.preco = preco #validar - > 0
        self.estoque = estoque #validar -  >=0
        self.ativo = ativo

    def adicionar_estoque(self, qtde):
        self.estoque += qtde

    def remover_estoque(self, qtde):
        self.estoque -= qtde

    def ativar(self):
        self.ativo = True

    def desativar(self):
        self.ativo = False

    #update
    def alterar_nome(self, nome):
        self.nome = nome

    def alterar_preco(self, preco):
        self.preco = preco

    def alterar_categoria(self, categoria):
        self.categoria = categoria

    #métodos especiais
    def __str__(self):
        return f'{self.sku}, {self.nome}, {self.preco}'

    def __repr__(self):
        pass

    def __eq__(self): #por sku
        pass

    def __lt__(self): #ordenar por preço ou nome
        pass 

class ProdutoFisico(Produto):
    def __init__(self, sku, nome, categoria, preco, estoque, ativo, peso):
        super().__init__(sku, nome, categoria, preco, estoque, ativo)
        self.peso = peso #validar - > 0

    def tem_frete(self):
       return True

    #persistência
    def to_dict(self): #incluir tipo físico
        pass

    def from_dict(cls, dict):
        pass
        

class ProdutoDigital(Produto):
    def tem_frete(self):
        return False

    #persistência
    def to_dict(self): #incluir tipo digital
        pass

    def from_dict(cls, dict):
        pass




