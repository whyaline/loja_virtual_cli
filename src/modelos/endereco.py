from src.utils import validar_string, validar_numero

class Endereco:
    def __init__(self, cidade, uf, cep):
        self.cidade = cidade
        self.uf = uf
        self.cep = cep

    @property
    def cidade(self):
        return self.__cidade

    #validação
    @cidade.setter
    def cidade(self, cidade):
        validar_string(cidade, "Cidade")

        self.__cidade = cidade.strip()

    @property
    def uf(self):
        return self.__uf

    #validação
    @uf.setter
    def uf(self, uf):
        #se digitou estados que existem
        uf_validos = {
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        }

        if uf.upper() not in uf_validos:
            raise ValueError(f"UF {uf.upper()} não existe")

        self.__uf = uf.upper()

    @property
    def cep(self):
        return self.__cep

    #validação
    @cep.setter
    def cep(self, cep):
        validar_numero(cep, "CEP", tipo=int, tamanho=8, permitir_zero=False)
        self.__cep = cep

    #métodos especiais
    def __str__(self):
        return f'Cidade: {self.cidade}, UF: {self.uf}, CEP: {self.cep}'

    def __repr__(self):
        return f'Endereco(cidade={self.cidade!r}, uf={self.uf!r}, cep={self.cep!r})'

    def __eq__(self, outro): #comparar se dois endereços são iguais ao remover de um cliente
        if not isinstance(outro, Endereco):
            return NotImplemented

        return self.cidade == outro.cidade and self.uf == outro.uf and self.cep == outro.cep


    #persistência
    def to_dict(self):
        pass

    def from_dict(cls, dict):
        pass

