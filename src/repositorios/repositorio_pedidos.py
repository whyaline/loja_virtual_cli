from src.modelos.pedido import Pedido
from src.dados.dados import salvar_lista, carregar_lista

class RepositorioPedidos:
    def __init__(self):
        self.__pedidos = []
        self.__proximo_id = 1

    # ======================
    # CRUD
    # ======================
    def adicionar_pedido(self, pedido: Pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("O objeto deve ser uma instância de Pedido")
        pedido._definir_id(self.__proximo_id)
        self.__proximo_id += 1
        self.__pedidos.append(pedido)

    def buscar_pedido_por_id(self, id):
        return next((p for p in self.__pedidos if p.id == id), None)

    def listar_pedidos(self):
        return self.__pedidos.copy()

    # ======================
    # PERSISTÊNCIA
    # ======================
    def salvar_dados(self):
        salvar_lista(
            "pedidos",
            {
                "proximo_id": self.__proximo_id,
                "pedidos": [p.to_dict() for p in self.__pedidos]
            }
        )
        print("Pedidos salvos com sucesso.")

    def carregar_dados(self, clientes_dict, carrinhos_dict, enderecos_dict):
        """
        Carrega os pedidos do JSON.
        clientes_dict: dicionário {cliente_id: Cliente}
        carrinhos_dict: dicionário {pedido_id: Carrinho}
        enderecos_dict: dicionário {cliente_id: Endereco}
        """
        dados = carregar_lista("pedidos")
        if not dados:
            print("Nenhum pedido encontrado. Repositório vazio.")
            return

        self.__proximo_id = dados.get("proximo_id", 1)
        self.__pedidos = []

        for pedido_data in dados.get("pedidos", []):
            cliente_id = pedido_data.get("cliente_id")
            pedido_id = pedido_data.get("id")

            cliente = clientes_dict.get(cliente_id)
            carrinho = carrinhos_dict.get(pedido_id)
            endereco = enderecos_dict.get(cliente_id)

            if not cliente or not carrinho or not endereco:
                print(f"Aviso: Pedido {pedido_id} ignorado. Dados incompletos.")
                continue

            pedido = Pedido.from_dict(pedido_data, cliente, endereco, carrinho)
            self.__pedidos.append(pedido)

        print(f"{len(self.__pedidos)} pedidos carregados com sucesso.")
