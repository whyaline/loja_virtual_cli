class Cupom:
    def __init__(self, codigo, tipo, valor, data_validade, uso_maximo, usos_feitos, categorias_elegiveis):
        self.codigo = codigo
        self.tipo = tipo
        self.valor = valor
        self.data_validade = data_validade
        self.uso_maximo = uso_maximo
        self.usos_feitos = usos_feitos
        self.categorias_elegiveis = categorias_elegiveis or []

    def validar(self):
        return self.usos_feitos < self.uso_maximo
        #ver se o código está correto, se está no prazo, se está esgotado

    def calcular_desconto(self):
      pass

    def registrar_uso(self):
        if self.usos_feitos < self.uso_maximo:
            self.usos_feitos += 1
        else:
            raise ValueError("Cupom já atingiu o limite de usos")

    #métodos especiais
    def __str__(self):
        return f'{self.codigo}, {self.tipo}, {self.valor}'

    def __eq__(self):
        pass

    #persistência
    def to_dict(self):
        pass

    def from_dict(cls, dict):
        pass
