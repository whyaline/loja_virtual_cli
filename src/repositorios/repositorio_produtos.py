from src.utils import validar_string, validar_numero
from src.modelos.produto import Produto, ProdutoDigital, ProdutoFisico
from src.dados.dados import salvar_lista, carregar_lista

class RepositorioProdutos:
    def __init__(self):
        self.__produtos = []
        self.__proximo_sku = 1

    # ======================
    # CRUD
    # ======================
    def adicionar_produto(self, produto: Produto):
        if not isinstance(produto, Produto):
            raise ValueError("O produto deve ser uma instância de Produto")

        produto._definir_sku(self.__proximo_sku)
        self.__proximo_sku += 1
        self.__produtos.append(produto)

    def buscar_produto_por_sku(self, sku):
        validar_numero(sku, "SKU", tipo=int, permitir_zero=False)
        return next((p for p in self.__produtos if p.sku == sku), None)

    def listar_produtos(self, somente_ativos=False):
        if somente_ativos:
            return [p for p in self.__produtos if p.ativo]
        return self.__produtos.copy()

    def alterar_produto(self, sku, nome_novo=None, categoria_nova=None, preco_novo=None, estoque_novo=None, ativo_novo=None):
        validar_numero(sku, "SKU", tipo=int, permitir_zero=False)
        produto = self.buscar_produto_por_sku(sku)
        if produto is None:
            raise ValueError("Produto não encontrado")

        if nome_novo is not None:
            produto.nome = nome_novo
        if categoria_nova is not None:
            produto.categoria = categoria_nova
        if preco_novo is not None:
            produto.preco = preco_novo
        if estoque_novo is not None:
            produto.estoque = estoque_novo
        if ativo_novo is not None:
            if not isinstance(ativo_novo, bool):
                raise ValueError("Ativo deve ser um valor booleano")
            produto.ativo = ativo_novo

    def remover_produto_por_sku(self, sku):
        validar_numero(sku, "SKU", tipo=int, permitir_zero=False)
        produto = self.buscar_produto_por_sku(sku)
        if produto is None:
            raise ValueError("Produto não encontrado")
        self.__produtos.remove(produto)

    # ======================
    # PERSISTÊNCIA
    # ======================
    def salvar_dados(self):
        salvar_lista(
            "produtos",
            {
                "proximo_sku": self.__proximo_sku,
                "produtos": [p.to_dict() for p in self.__produtos]
            }
        )
        print("Produtos salvos com sucesso.")

    def carregar_dados(self):
        dados = carregar_lista("produtos")
        if not dados:
            print("Nenhum produto encontrado. Repositório vazio.")
            return

        self.__proximo_sku = dados.get("proximo_sku", 1)
        self.__produtos = []

        for item in dados.get("produtos", []):
            tipo = item.get("tipo")
            if tipo == "fisico":
                produto = ProdutoFisico.from_dict(item)
            elif tipo == "digital":
                produto = ProdutoDigital.from_dict(item)
            else:
                print(f"Aviso: Produto com tipo desconhecido ignorado: {item}")
                continue
            self.__produtos.append(produto)

        print(f"{len(self.__produtos)} produtos carregados com sucesso.")
