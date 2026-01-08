class RepositorioClientes:
    #CRUD
    def __init__(self):
        self.__clientes = [] #lista com as instâncias criadas

    def existe_cpf(self, cpf, exceto=None):
        return any(c.cpf == cpf and c is not exceto for c in self.__clientes)

    def existe_email(self, email, exceto = None):
        return any(c.email == email and c is not exceto for c in self.__clientes)

    # criar lista de clientes
    def adicionar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ValueError("O cliente deve ser uma instância de Cliente")
        
        if self.existe_cpf(cliente.cpf):
            raise ValueError(f'Já existe um cliente com CPF {cliente.cpf}')
        
        if self.existe_email(cliente.email):
            raise ValueError(f'Já existe um cliente com email {cliente.email}')

        self.__clientes.append(cliente)

    # buscar cliente
    def buscar_cliente_por_id(self, id):
        for cliente in self.__clientes:
            if cliente.id == id:
                return cliente
        return None

    def buscar_cliente_por_cpf(self, cpf):
        for cliente in self.__clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    # alterar cliente
    def alterar_cliente_por_id(self, id, nome_novo=None, cpf_novo=None, email_novo=None):
        cliente = self.buscar_cliente_por_id(id)

        if cliente is None:
            raise ValueError("Cliente não encontrado")
        
        if nome_novo is not None:
            cliente.nome = nome_novo

        if cpf_novo is not None:
            if self.existe_cpf(cpf_novo, cliente):
                raise ValueError(f'Já existe um cliente com CPF {cpf_novo}')
            cliente.cpf = cpf_novo

        if email_novo is not None:
            if self.existe_email(email_novo, cliente):
                  raise ValueError(f'Já existe um cliente com email {email_novo}')
            cliente.email = email_novo

    def alterar_cliente_por_cpf(self, cpf, nome_novo=None, cpf_novo=None, email_novo=None):
        cliente = self.buscar_cliente_por_cpf(cpf)

        if cliente is None:
            raise ValueError("Cliente não encontrado")
        
        if nome_novo is not None:
            cliente.nome = nome_novo

        if cpf_novo is not None:
            if self.existe_cpf(cpf_novo, cliente):
                raise ValueError(f'Já existe um cliente com CPF {cpf_novo}')
            cliente.cpf = cpf_novo

        if email_novo is not None:
            if self.existe_email(email_novo, cliente):
                  raise ValueError(f'Já existe um cliente com email {email_novo}')
            cliente.email = email_novo


    # listar clientes
    def listar_clientes(self):
        return self.__clientes.copy()

    # remover cliente
    def remover_cliente_por_id(self, id):
        cliente = self.buscar_cliente_por_id(id)

        if cliente is None:
            raise ValueError("Cliente não encontrado")

        self.__clientes.remove(cliente)

    def remover_cliente_por_cpf(self, cpf):
        cliente = self.buscar_cliente_por_cpf(cpf)

        if cliente is None:
            raise ValueError("Cliente não encontrado")

        self.__clientes.remove(cliente)

    #salvar dados
    def salvar_dados(self):
      pass

    #carregar dados
    def carregar_dados(self):
      pass

