class Cliente:
    def __init__(self, id, nome, cpf, email):
        self.id = id
        self.nome = nome #validar
        self.cpf = cpf #validar
        self.email = email #validar
        self.enderecos = []
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        validar_numero(id, "ID", tipo=int, permitir_zero=False)
        self.__id = id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        validar_string(nome, "Nome")
        self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        validar_numero(cpf, "CPF", tipo=int, tamanho=11)
        self.__cpf = cpf

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if '@' not in email or '.' not in email:
            raise ValueError ("Email Inválido")
        else:
            self.__email = email

    @property
    def enderecos(self):
        return self.__enderecos.copy()

    def adicionar_endereco(self, endereco: Endereco):
        self.enderecos.append(endereco)

    # Read
    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente)

    def listar_enderecos(self):
        for endereco in self.enderecos:
            print(endereco)

    def tem_endereco(self, endereco: Endereco):
        #retorna true or false

    # Update: setter?
    def alterar_nome(self, nome):
        self.nome = nome

    def alterar_email(self, email):
        self.email = email
        #impedir se duplicado

    def alterar_cpf(self, cpf):
        self.cpf = cpf
        #impedir se duplicado

    def alterar_endereco(self, endereco):
        #lista os endereços e escolhe um pra alterar
        pass

    # Delete
    def remover_endereco(self, endereco: Endereco):
        self.enderecos.remove(endereco)
        #remover por cep

    # métodos especiais
    def __str__(self):
        return f'Nome: {self.nome}, Email: {self.email}, CPF: {self.cpf}'

    def __repr__(self):
        pass

    def __eq__(self):
        #por email/cpf
        pass

    
    #persistência
    def to_dict(self):
        pass

    def from_dict(cls, dict):
        pass



for endereco in c.enderecos:
    print(endereco)
