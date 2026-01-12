from src.modelos.endereco import Endereco
from src.modelos.carrinho import Carrinho
from src.modelos.produto import ProdutoFisico

class Frete:
    def __init__(self, endereco: Endereco):
        if not isinstance(endereco, Endereco):
            raise TypeError("endereço deve ser uma instância de Endereco")

        self.endereco = endereco
        self.valor = 0
        self.prazo = 0

    def _buscar_regra(self, tabela_frete):
        return tabela_frete.get(self.endereco.uf, tabela_frete["default"])

    def calcular_preview(self, carrinho: Carrinho, tabela_frete):
        if not isinstance(carrinho, Carrinho):
            raise TypeError("carrinho deve ser uma instância de Carrinho")

        regra = self._buscar_regra(tabela_frete)

        valores_frete = []
        prazos = []

        for item in carrinho.itens:
            if isinstance(item.produto, ProdutoFisico):
                valores_frete.append(regra["valor"])
                prazos.append(regra["prazo"])

        self.valor = max(valores_frete) if valores_frete else 0
        self.prazo = max(prazos) if prazos else 0

        return {"valor": self.valor, "prazo": self.prazo}
