from src.modelos.cliente import Cliente
import json

class RepositorioClientes:
    #CRUD
    def __init__(self):
        self.__clientes = [] #lista com as instâncias criadas
        self.__proximo_id = 1
        self.arquivo_dados = "clientes_data.json"

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

        cliente._definir_id(self.__proximo_id)
        self.__proximo_id += 1

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


    #persistência
    def salvar_dados(self):
        data_to_save = {
            "proximo_id": self.__proximo_id,
            "clientes": [c.to_dict() for c in self.__clientes]
        }
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        print(f"Dados de clientes salvos em {self.arquivo_dados}")

    #carregar dados
    def carregar_dados(self):
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)
            self.__proximo_id = data_loaded.get("proximo_id", 1)
            self.__clientes = []
            for cliente_data in data_loaded.get("clientes", []):
                cliente = Cliente.from_dict(cliente_data)
                self.__clientes.append(cliente)
            print(f"Dados de clientes carregados de {self.arquivo_dados}")
        except FileNotFoundError:
            print(f"Arquivo de dados {self.arquivo_dados} não encontrado. Iniciando com repositório vazio.")
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON de {self.arquivo_dados}. Iniciando com repositório vazio.")
