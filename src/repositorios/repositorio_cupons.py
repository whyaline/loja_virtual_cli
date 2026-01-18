import json
from src.modelos.cupom import Cupom


class RepositorioCupons:
    def __init__(self):
        self.__cupons = []
        self.arquivo_dados = "cupons_data.json"

    # ======================
    # CONSULTAS
    # ======================

    def buscar_por_codigo(self, codigo: str):
        for cupom in self.__cupons:
            if cupom.codigo == codigo:
                return cupom
        return None

    def listar_cupons(self, somente_validos=False):
        if not somente_validos:
            return self.__cupons.copy()

        cupons_validos = []
        for cupom in self.__cupons:
            try:
                cupom.validar_uso()
                cupons_validos.append(cupom)
            except ValueError:
                pass

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
    # PERSISTÊNCIA
    # ======================

    def salvar_dados(self):
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(
                [c.to_dict() for c in self.__cupons],
                f,
                ensure_ascii=False,
                indent=2
            )

    def carregar_dados(self):
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                dados = json.load(f)

            self.__cupons = [Cupom.from_dict(d) for d in dados]

        except FileNotFoundError:
            self.__cupons = []

        except json.JSONDecodeError:
            raise ValueError("Erro ao ler arquivo de cupons")
