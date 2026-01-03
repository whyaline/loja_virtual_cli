class RepositorioClientes:
    #CRUD
    def __init__(self):
        self.clientes = []

    # criar lista de clientes
    def adicionar_cliente_repositorio(self, cliente: Cliente):
        self.clientes.append(cliente)

    # buscar cliente
    def buscar_cliente(self, id):
      pass
    
    # remover cliente
    def remover_cliente(self, cliente: Cliente):
      pass
    
    #salvar dados
    def salvar_dados(self):
      pass

    #carregar dados
    def carregar_dados(self):
      pass
