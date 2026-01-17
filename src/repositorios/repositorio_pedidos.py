from src.modelos.pedido import Pedido
from src.dados.dados import salvar_lista, carregar_lista

class RepositorioPedidos:
    def __init__(self):
        self.__pedidos = []
        self.__proximo_id = 1 # Inicializa o contador para IDs de pedidos

    def adicionar_pedido(self, pedido: Pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("O objeto deve ser uma instância de Pedido")

        pedido._definir_id(self.__proximo_id)
        self.__proximo_id += 1
        self.__pedidos.append(pedido)

    def buscar_pedido_por_id(self, id):
        for pedido in self.__pedidos:
            if pedido.id == id:
                return pedido
        return None

    def listar_pedidos(self):
        return self.__pedidos.copy()

    def salvar(self):
        salvar_lista(
            "pedidos",
            {
                "proximo_id": self.__proximo_id,
                "pedidos": [p.to_dict() for p in self.__pedidos]
            }
        )

    def carregar(self, clientes, carrinhos, enderecos):
        dados = carregar_lista("pedidos")

        if not dados:
            return

        self.__proximo_id = dados.get("proximo_id", 1)
        self.__pedidos = []

        for pedido_data in dados.get("pedidos", []):
            cliente = clientes[pedido_data["cliente_id"]]
            carrinho = carrinhos[pedido_data["id"]]
            endereco = enderecos[cliente.id]

            pedido = Pedido.from_dict(
                pedido_data,
                cliente,
                endereco,
                carrinho
            )

            self.__pedidos.append(pedido)