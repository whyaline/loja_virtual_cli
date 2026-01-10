from src.utils import validar_string, validar_numero
from src.modelos.produto import Produto, ProdutoDigital, ProdutoFisico
import json

class RepositorioProdutos:
    def __init__(self):
        self.__produtos = []
        self.__proximo_sku = 1
        self.arquivo_dados = "produtos_data.json" # nome do arquivo para persistência

    def adicionar_produto(self, produto: Produto):
        if not isinstance(produto, Produto):
            raise ValueError("O produto deve ser uma instância de Produto")

        produto._definir_sku(self.__proximo_sku)
        self.__proximo_sku += 1

        self.__produtos.append(produto)


    def buscar_produto_por_sku(self, sku):
        validar_numero(sku, "SKU", tipo=int, permitir_zero=False)

        for produto in self.__produtos:
            if produto.sku == sku:
                return produto

        return None

    def listar_produtos(self, somente_ativos=False):
        if somente_ativos:
            return [produto for produto in self.__produtos if produto.ativo]

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

    #persistência
    def salvar_dados(self):
        data_to_save = {
            "proximo_sku": self.__proximo_sku,
            "produtos": [p.to_dict() for p in self.__produtos]
        }
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        print(f"Dados de produtos salvos em {self.arquivo_dados}")

    def carregar_dados(self):
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)
            self.__proximo_sku = data_loaded.get("proximo_sku", 1)
            self.__produtos = []
            for item_data in data_loaded.get("produtos", []):
                if item_data.get("tipo") == "fisico":
                    produto = ProdutoFisico.from_dict(item_data)
                elif item_data.get("tipo") == "digital":
                    produto = ProdutoDigital.from_dict(item_data)
                else:
                    # Fallback or raise error if type is unknown
                    continue
                self.__produtos.append(produto)
            print(f"Dados de produtos carregados de {self.arquivo_dados}")
        except FileNotFoundError:
            print(f"Arquivo de dados {self.arquivo_dados} não encontrado. Iniciando com repositório vazio.")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON de {self.arquivo_dados}. Iniciando com repositório vazio.")