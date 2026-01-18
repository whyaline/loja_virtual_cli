from abc import ABC, abstractmethod
from src.utils import validar_string, validar_numero

class Produto (ABC):
    def __init__(self, nome, categoria, preco, estoque, ativo):
        self.__sku = None #unico -> validar em repositório
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.ativo = ativo

    @property
    def sku(self):
        return self.__sku #implementar automático no repositório

    def _definir_sku(self, sku):
        if self.__sku is not None:
            raise ValueError("SKU já definido")

        validar_numero(sku, "SKU", tipo=int, permitir_zero=False)
        self.__sku = sku

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        validar_string(nome, "Nome")
        self.__nome = nome

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        validar_string(categoria, "Categoria")
        self.__categoria = categoria.upper()

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, preco):
        validar_numero(preco, "Preço", tipo=float)
        self.__preco = preco

    @property
    def estoque(self):
        return self.__estoque

    @estoque.setter
    def estoque(self, estoque):
        validar_numero(estoque, "Estoque", tipo=int, permitir_zero=True)
        self.__estoque = estoque

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, ativo):
        if not isinstance(ativo, bool):
            raise ValueError("Ativo deve ser um valor booleano")
        self.__ativo = ativo


    #######
    def tem_estoque(self):
        return self.estoque > 0

    def adicionar_estoque(self, qtde):
        if not self.ativo:
            raise ValueError("Produto inativo!")

        validar_numero(qtde, "Quantidade", tipo=int, permitir_zero=False)
        self.estoque += qtde

    def remover_estoque(self, qtde):
        if not self.ativo:
            raise ValueError("Produto inativo!")

        validar_numero(qtde, "Quantidade", tipo=int, permitir_zero=False)

        if qtde > self.estoque:
            raise ValueError("Quantidade em estoque insuficiente!")

        self.estoque -= qtde

    def ativar(self):
        self.ativo = True

    def desativar(self):
        self.ativo = False

    @abstractmethod
    def tem_frete(self):
        pass

    #métodos especiais
    def __str__(self):
        return f'SKU: {self.sku}, Nome: {self.nome}, Categoria: {self.categoria}, Preço: {self.preco}, Estoque: {self.estoque}, Ativo: {self.ativo}'

    def __repr__(self):
        return f'Produto(sku={self.sku!r}, nome={self.nome!r}, categoria={self.categoria!r}, preco={self.preco!r}, estoque={self.estoque!r},  ativo={self.ativo!r})'

    def __eq__(self, outro): #por sku
        if not isinstance(outro, Produto):
            return NotImplemented

        if self.sku is None or outro.sku is None:
            return False

        return self.sku == outro.sku

    def __lt__(self, outro): #ordenar por preço ou nome
        if not isinstance(outro, Produto):
            return NotImplemented

        return self.preco < outro.preco

    # persistência
    def to_dict(self):
        return {
            "sku": self.sku,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "estoque": self.estoque,
            "ativo": self.ativo
        }


class ProdutoFisico(Produto):
    def __init__(self, nome, categoria, preco, estoque, ativo, peso):
        super().__init__(nome, categoria, preco, estoque, ativo)
        self.peso = peso #validar - > 0


    @property
    def peso(self):
        return self.__peso

    @peso.setter
    def peso(self, peso):
        validar_numero(peso, "Peso", tipo=float, permitir_zero=False)

        self.__peso = peso

    def tem_frete(self):
       return True

    def __str__(self):
        return f"{super().__str__()}, Peso: {self.peso}"

    #persistência
    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "fisico"
        data["peso"] = self.peso
        return data

    @classmethod
    def from_dict(cls, data):
        produto = cls(
            nome=data["nome"],
            categoria=data["categoria"],
            preco=data["preco"],
            estoque=data["estoque"],
            ativo=data["ativo"],
            peso=data["peso"]
        )
        if data["sku"] is not None:
            produto._definir_sku(data["sku"])
        return produto


class ProdutoDigital(Produto):
    def __init__(self, nome, categoria, preco, ativo):
        super().__init__(nome, categoria, preco, estoque=0, ativo=ativo)

    def tem_frete(self):
        return False

    #persistência
    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "digital"
        return data

    @classmethod
    def from_dict(cls, data):
        produto = cls(
            nome=data["nome"],
            categoria=data["categoria"],
            preco=data["preco"],
            ativo=data["ativo"]
        )
        if data["sku"] is not None:
            produto._definir_sku(data["sku"])
        return produto