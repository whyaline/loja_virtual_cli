from src.utils import validar_string, validar_numero
from src.modelos.endereco import Endereco

class Cliente:
    def __init__(self, nome, cpf, email):
        self.__id = None #atribuído pelo repositório 
        self.nome = nome #validar
        self.cpf = cpf #validar
        self.email = email #validar
        self.__enderecos = []

    @property
    def id(self):
        return self.__id

    def _definir_id(self, id):
        if self.__id is not None:
            raise ValueError("ID já definido")

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

    def tem_endereco(self):
        return len(self.__enderecos) > 0

    def adicionar_endereco(self, endereco):
        if not isinstance(endereco, Endereco):
            raise ValueError("Endereço inválido")

        if endereco in self.__enderecos:
            raise ValueError("Endereço já cadastrado")

        self.__enderecos.append(endereco)

    def buscar_endereco_por_cep(self, cep):
        for endereco in self.__enderecos:
            if endereco.cep == cep:
                return endereco

        return None

    def alterar_endereco(self, cep, cidade_novo=None, uf_novo=None, cep_novo=None):
        endereco = self.buscar_endereco_por_cep(cep)

        if endereco is None:
            raise ValueError("Endereço não encontrado")

        if cidade_novo is not None:
            endereco.cidade = cidade_novo

        if uf_novo is not None:
            endereco.uf = uf_novo

        if cep_novo is not None:
            endereco.cep = cep_novo

    def remover_endereco(self, cep): #remover por cep
        endereco = self.buscar_endereco_por_cep(cep)

        if endereco is None:
            raise ValueError("Endereço não encontrado")

        self.__enderecos.remove(endereco)


    # métodos especiais
    def __str__(self):
        if self.__enderecos:
            enderecos_str = '; '.join(str(e) for e in self.__enderecos)
        else:
            enderecos_str = "Nenhum"

        return f'Nome: {self.nome}, CPF: {self.cpf}, Email: {self.email}, Endereços: [{enderecos_str}]'

    def __repr__(self):
        return (f"Cliente(id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r}, "
                f"email={self.email!r}, enderecos={self.__enderecos!r})")

    def __eq__(self, outro): #por cpf ou email
        if not isinstance(outro, Cliente):
            return NotImplemented

        return self.cpf == outro.cpf or self.email == outro.email


    #persistência
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "enderecos": [endereco.to_dict() for endereco in self.__enderecos]
        }

    @classmethod
    def from_dict(cls, dict):
        cliente = cls(
            nome=dict["nome"],
            cpf=dict["cpf"],
            email=dict["email"]
        )
        if dict["id"] is not None:
            cliente._definir_id(dict["id"])

        for endereco_data in dict["enderecos"]:
            cliente.adicionar_endereco(Endereco.from_dict(endereco_data))
        return cliente