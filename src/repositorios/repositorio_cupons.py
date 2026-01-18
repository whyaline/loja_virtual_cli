from src.modelos.cupom import Cupom
from src.dados.dados import salvar_lista, carregar_lista

class RepositorioCupons:
    def __init__(self):
        self.__cupons = []

    # ======================
    # CONSULTAS
    # ======================
    def buscar_por_codigo(self, codigo: str):
        return next((c for c in self.__cupons if c.codigo == codigo), None)

    def listar_cupons(self, somente_validos=False):
        if not somente_validos:
            return self.__cupons.copy()

        cupons_validos = []
        for cupom in self.__cupons:
            try:
                cupom.validar_uso()
                cupons_validos.append(cupom)
            except ValueError:
                continue
        return cupons_validos

    # ======================
    # CRUD
    # ======================
    def adicionar_cupom(self, cupom: Cupom):
        if not isinstance(cupom, Cupom):
            raise ValueError("Cupom inválido")
        if self.buscar_por_codigo(cupom.codigo):
            raise ValueError(f"Cupom '{cupom.codigo}' já existe")
        self.__cupons.append(cupom)

    def remover_cupom(self, codigo: str):
        cupom = self.buscar_por_codigo(codigo)
        if not cupom:
            raise ValueError("Cupom não encontrado")
        self.__cupons.remove(cupom)

    # ======================
    # USO DO CUPOM
    # ======================
    def aplicar_cupom(self, codigo: str, total_pedido: float, categoria=None):
        cupom = self.buscar_por_codigo(codigo)
        if not cupom:
            raise ValueError("Cupom inexistente")
        desconto = cupom.calcular_desconto(total_pedido)
        cupom.registrar_uso(categoria)
        return desconto

    # ======================
    # PERSISTÊNCIA VIA dados.py
    # ======================
    def salvar_dados(self):
        salvar_lista("cupons", [c.to_dict() for c in self.__cupons])
        print("Cupons salvos com sucesso.")

    def carregar_dados(self):
        dados = carregar_lista("cupons")
        if not dados:
            print("Nenhum cupom encontrado. Repositório vazio.")
            return
        self.__cupons = [Cupom.from_dict(c) for c in dados]
        print(f"{len(self.__cupons)} cupons carregados com sucesso.")
