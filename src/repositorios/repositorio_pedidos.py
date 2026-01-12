from src.modelos.pedido import Pedido

class RepositorioPedidos:
    def __init__(self):
        self.pedidos = []
        self.__proximo_id = 1 # Inicializa o contador para IDs de pedidos

    def adicionar_pedido(self, pedido: Pedido):
        if not isinstance(pedido, Pedido):
            raise ValueError("O objeto deve ser uma instância de Pedido")

        pedido._definir_id(self.__proximo_id)
        self.__proximo_id += 1
        self.pedidos.append(pedido)

    def buscar_pedido_por_id(self, id):
        for pedido in self.pedidos:
            if pedido.id == id:
                return pedido
        return None

    def listar_pedidos(self):
        return self.pedidos.copy()