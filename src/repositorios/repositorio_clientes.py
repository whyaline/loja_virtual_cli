from src.modelos.cliente import Cliente
from src.dados.dados import salvar_lista, carregar_lista

class RepositorioClientes:
    def __init__(self):
        self.__clientes = []
        self.__proximo_id = 1

    # CRUD
    def adicionar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ValueError("O cliente deve ser uma instância de Cliente")
        
        if self.existe_cpf(cliente.cpf):
            raise ValueError(f'Já existe um cliente com CPF {cliente.cpf}')
        
        if self.existe_email(cliente.email):
            raise ValueError(f'Já existe um cliente com email {cliente.email}')

        cliente._definir_id(self.__proximo_id)
        self.__proximo_id += 1
        self.__clientes.append(cliente)

    def listar_clientes(self):
        return self.__clientes.copy()

    def buscar_cliente_por_id(self, id):
        return next((c for c in self.__clientes if c.id == id), None)

    def buscar_cliente_por_cpf(self, cpf):
        return next((c for c in self.__clientes if c.cpf == cpf), None)

    def alterar_cliente_por_id(self, id, nome_novo=None, cpf_novo=None, email_novo=None):
        cliente = self.buscar_cliente_por_id(id)
        if cliente is None:
            raise ValueError("Cliente não encontrado")
        if nome_novo: cliente.nome = nome_novo
        if cpf_novo:
            if self.existe_cpf(cpf_novo, cliente):
                raise ValueError(f'Já existe um cliente com CPF {cpf_novo}')
            cliente.cpf = cpf_novo
        if email_novo:
            if self.existe_email(email_novo, cliente):
                raise ValueError(f'Já existe um cliente com email {email_novo}')
            cliente.email = email_novo

    def remover_cliente_por_id(self, id):
        cliente = self.buscar_cliente_por_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        self.__clientes.remove(cliente)

    # Validações
    def existe_cpf(self, cpf, exceto=None):
        return any(c.cpf == cpf and c is not exceto for c in self.__clientes)

    def existe_email(self, email, exceto=None):
        return any(c.email == email and c is not exceto for c in self.__clientes)

    # Persistência via dados.py
    def salvar_dados(self):
        data_to_save = {
            "proximo_id": self.__proximo_id,
            "clientes": [c.to_dict() for c in self.__clientes]
        }
        salvar_lista("clientes", data_to_save)
        print("Clientes salvos com sucesso.")

    def carregar_dados(self):
        dados = carregar_lista("clientes")
        if not dados:
            print("Nenhum cliente encontrado. Repositório vazio.")
            return

        self.__proximo_id = dados.get("proximo_id", 1)
        self.__clientes = [Cliente.from_dict(c) for c in dados.get("clientes", [])]
        print(f"{len(self.__clientes)} clientes carregados com sucesso.")
