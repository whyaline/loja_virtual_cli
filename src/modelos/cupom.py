from datetime import date, timedelta

class Cupom:
    def __init__(self, codigo: str, tipo: str, valor: float, data_validade: date = None, uso_maximo: int = 0, usos_feitos: int = 0, categorias_elegiveis=None):

        #verifica no momento da criação do cupom se o uso máximo e os usos feitos são válidos
        if uso_maximo <= 0:
            raise ValueError("Uso máximo deve ser maior que zero")

        if usos_feitos < 0 or usos_feitos > uso_maximo:
            raise ValueError("Usos feitos inválido")

        self.__codigo = codigo
        self.tipo = tipo.upper() #VALOR ou PERCENTUAL
        self.valor = valor

        if data_validade is None:
            #usa a validade padrão de cupom definido no settings
            global default_coupon_validity_days
            self.data_validade = date.today() + timedelta(days=default_coupon_validity_days)
        else:
            self.data_validade = data_validade

        self.uso_maximo = uso_maximo
        self.__usos_feitos = usos_feitos
        self.__categorias_elegiveis = categorias_elegiveis or []

    #ENCAPSULAMENTO DOS ATRIBUTOS
    @property
    def codigo(self):
        return self.__codigo

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        tipo = tipo.upper()
        if tipo not in ("VALOR", "PERCENTUAL"):
            raise ValueError("Tipo deve ser VALOR ou PERCENTUAL")
        self.__tipo = tipo

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if valor <= 0:
            raise ValueError("Valor do cupom deve ser positivo")
        self.__valor = valor

    @property
    def data_validade(self):
        return self.__data_validade

    @data_validade.setter
    def data_validade(self, data):
        if data < date.today():
            raise ValueError("Data de validade não pode ser no passado")
        self.__data_validade = data

    @property
    def uso_maximo(self):
        return self.__uso_maximo

    @uso_maximo.setter
    def uso_maximo(self, uso_maximo):
        if uso_maximo <= 0:
            raise ValueError("Uso máximo deve ser maior que zero")

        self.__uso_maximo = uso_maximo

    @property
    def usos_feitos(self):
        return self.__usos_feitos

    @property
    def categorias_elegiveis(self):
        return self.__categorias_elegiveis.copy()

    #VALIDAÇÃO DO CUPOM
    def validar_uso(self, categoria=None): #se está no prazo, se está esgotado
        hoje = date.today()

        if self.data_validade < hoje:
            raise ValueError("Cupom expirado")

        if self.usos_feitos >= self.uso_maximo:
            raise ValueError("Cupom já atingiu o limite de usos")

        if self.categorias_elegiveis:
            if categoria is None:
                raise ValueError("Categoria deve ser informada para este cupom")

            if categoria.upper() not in self.categorias_elegiveis:
                raise ValueError("Cupom não é válido para essa categoria")

        return True

    #CÁLCULO DE DESCONTO
    def calcular_desconto(self, total_pedido):
      if self.tipo == "VALOR":
        return min(self.valor, total_pedido)

      elif self.tipo == "PERCENTUAL":
        return total_pedido * (self.valor / 100)

      else:
        raise ValueError("Tipo de cupom inválido")


    def registrar_uso(self, categoria=None):
        self.validar_uso(categoria)

        self.__usos_feitos += 1


    #MÉTODOS ESPECIAIS
    def __str__(self): #string apresentável
        return f'Cupom: {self.codigo}, Tipo: {self.tipo}, Valor: {self.valor}'

    def __repr__(self): #string p/ dev
        return f"Cupom(codigo={self.codigo!r}, tipo={self.tipo!r}, valor={self.valor!r}, data_validade={self.data_validade!r}, uso_maximo={self.uso_maximo!r}, usos_feitos={self.usos_feitos!r}, categorias_elegiveis={self.categorias_elegiveis!r})"

    def __eq__(self, other): #comparação de cupons
        if not isinstance(other, Cupom):
            return NotImplemented
        return self.codigo == other.codigo

    def __hash__(self): #int hash
        return hash(self.codigo)

    #PERSISTÊNCIA
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "valor": self.valor,
            "data_validade": self.data_validade.isoformat(),
            "uso_maximo": self.uso_maximo,
            "usos_feitos": self.usos_feitos,
            "categorias_elegiveis": self.categorias_elegiveis
        }

    @classmethod
    def from_dict(cls, data: dict):
        data_validade = None
        if "data_validade" in data:
            data_validade = date.fromisoformat(data["data_validade"])

        return cls(
            codigo=data["codigo"],
            tipo=data["tipo"],
            valor=data["valor"],
            data_validade=data_validade,
            uso_maximo=data["uso_maximo"],
            usos_feitos=data["usos_feitos"],
            categorias_elegiveis=data.get("categorias_elegiveis")
        )