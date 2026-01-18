from src.utils.config import carregar_tabela_frete
from src.modelos.endereco import Endereco
#from src.modelos.carrinho import Carrinho
from src.modelos.produto import ProdutoFisico


class Frete:
    def __init__(self, endereco: Endereco):
        if not isinstance(endereco, Endereco):
            raise TypeError("endereço deve ser uma instância de Endereco")

        self.endereco = endereco
        self.valor = 0
        self.prazo = 0
        self.tabela_frete = carregar_tabela_frete()

    def _buscar_regra(self):
        cep = self.endereco.cep.replace("-", "")
        uf = self.endereco.uf

        for faixa in self.tabela_frete["faixas_cep"]:
            inicio = faixa["inicio"].replace("-", "")
            fim = faixa["fim"].replace("-", "")

            if faixa["uf"] == uf and inicio <= cep <= fim:
                return faixa

        return self.tabela_frete["default"]

    def calcular_preview(self, carrinho):
        if not hasattr(carrinho, "itens"):
            raise TypeError("Objeto carrinho inválido")

        tem_produto_fisico = any(
            isinstance(item.produto, ProdutoFisico)
            for item in carrinho.itens
        )

        if tem_produto_fisico:
            regra = self._buscar_regra()
            self.valor = regra["valor"]
            self.prazo = regra["prazo"]
        else:
            self.valor = 0
            self.prazo = 0

        return {
            "valor": self.valor,
            "prazo": self.prazo
        }
