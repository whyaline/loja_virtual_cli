class Endereco:
    def __init__(self, cidade, uf, cep):
        self.cidade = cidade
        self.uf = uf
        self.cep = cep

    def validar_string(self, valor, campo):
        if not isinstance(valor, str) or len(valor.strip()) <= 0:
            raise ValueError(f"{campo} deve ser uma string e não pode ser vazio!")

        if not valor.replace(" ", "").isalpha():
            raise ValueError(f"{campo} deve conter apenas letras!")


    def validar_numero(self, valor, campo, tamanho=None):
        valor = str(valor)

        if not valor.isdigit():
            raise ValueError(f"{campo} deve conter apenas números")

        if tamanho is not None and len(valor) != tamanho:
            raise ValueError(f"{campo} deve conter {tamanho} dígitos")

    @property
    def cidade(self):
        return self.__cidade

    #validação
    @cidade.setter
    def cidade(self, cidade):
        self.validar_string(cidade, "Cidade")

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
        self.validar_numero(cep, "CEP", 8)
        self.__cep = cep

    #métodos especiais
    def __str__(self):
        return f'{self.cep}, {self.cidade}, {self.uf}'

    def __repr__(self):
        pass

    def __eq__(self): #comparar se dois endereços são iguais ao remover de um cliente
        pass


    #persistência
    def to_dict(self):
        pass

    def from_dict(cls, dict):
        pass

e = Endereco ("crato", "ce", "10201001") #o input sempre irá retornar string, cep entre aspas para facilitar testes
print(e.cidade)
print(e.uf)
print(e.cep)
