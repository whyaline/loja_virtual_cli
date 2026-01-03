class Endereco:
    def __init__(self, cidade, uf, cep):
        self.cidade = cidade
        self.uf = uf
        self.cep = cep

    def validar(self):
        uf_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
                  'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
                  'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        if self.uf not in uf_validas:
            raise ValueError(f"UF inválida: {self.uf}")
        if not self.cep.replace("-", "").isdigit() or len(self.cep.replace("-", "")) != 8:
            raise ValueError(f"CEP inválido: {self.cep}")

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
