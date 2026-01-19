from src.modelos.pedido import Pedido
from src.dados.dados import salvar_lista, carregar_lista
from src.modelos.endereco import Endereco

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
        self.salvar_dados()  # salva automaticamente ao adicionar

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

    def carregar_dados(self, clientes_dict, produtos_dict, carrinhos_dict=None, enderecos_dict=None):
        """
        Carrega os pedidos do JSON.
        clientes_dict: {cliente_id: Cliente}
        produtos_dict: {sku: Produto} - usado para reconstruir os itens
        """
        from src.modelos.pagamento import Pagamento
        from src.utils.enums import StatusPagamento, FormaPagamento

        dados = carregar_lista("pedidos")
        if not dados:
            print("Nenhum pedido encontrado. Repositório vazio.")
            return

        self.__proximo_id = dados.get("proximo_id", 1)
        self.__pedidos = []

        for pedido_data in dados.get("pedidos", []):
            pedido_id = pedido_data.get("id")
            cliente_id = pedido_data.get("cliente_id")
            cliente = clientes_dict.get(cliente_id)

            if not cliente:
                print(f"Aviso: Pedido {pedido_id} ignorado. Cliente não encontrado.")
                continue

            # Recupera endereço
            endereco_data = pedido_data.get("endereco")
            if endereco_data:
                endereco = Endereco.from_dict(endereco_data)
            else:
                endereco = cliente.enderecos[0] if cliente.enderecos else None

            if not endereco:
                print(f"Aviso: Pedido {pedido_id} ignorado. Endereço não encontrado.")
                continue

            # Reconstrói o pedido
            try:
                pedido = Pedido.from_dict(
                    pedido_data,
                    cliente,
                    endereco,
                    produtos_dict
                )

                # ======= CORREÇÃO: criar pagamento para pedidos PAGO =======
                if pedido.status == pedido.status.PAGO and pedido.total_pago == 0:
                    pagamento = Pagamento(
                        pedido=pedido,
                        valor=pedido.total,
                        forma=FormaPagamento.DINHEIRO  # forma genérica
                    )
                    pagamento.status = StatusPagamento.CONFIRMADO
                    pedido.pagamentos.append(pagamento)
                    # total_pago agora será igual a pedido.total

            except ValueError as e:
                print(f"Aviso: Pedido {pedido_id} ignorado. {e}")
                continue

            self.__pedidos.append(pedido)

        print(f"{len(self.__pedidos)} pedidos carregados com sucesso.")
