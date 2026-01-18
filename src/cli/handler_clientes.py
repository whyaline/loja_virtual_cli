# src/cli/handler_clientes.py
from src.repositorios.repositorio_clientes import RepositorioClientes
from src.modelos.cliente import Cliente

repo_clientes = RepositorioClientes()
repo_clientes.carregar_dados()

def handle_clientes(args):
    if not args:
        print("Comando do cliente não especificado")
        return

    comando = args[0].lower()

    if comando == "cadastrar":
        nome = input("Nome: ")
        cpf = input("CPF: ")
        email = input("Email: ")
        cliente = Cliente(nome=nome, cpf=cpf, email=email)
        repo_clientes.adicionar_cliente(cliente)
        repo_clientes.salvar_dados()
        print(f"Cliente {nome} cadastrado com sucesso!")

    elif comando == "listar":
        for c in repo_clientes.listar_clientes():
            print(c)

    elif comando == "editar":
        id_cliente = int(input("ID do cliente: "))
        nome = input("Novo nome (Enter para manter): ")
        cpf = input("Novo CPF (Enter para manter): ")
        email = input("Novo email (Enter para manter): ")
        repo_clientes.alterar_cliente_por_id(id_cliente, nome or None, cpf or None, email or None)
        repo_clientes.salvar_dados()
        print(f"Cliente {id_cliente} editado com sucesso!")

    elif comando == "remover":
        id_cliente = int(input("ID do cliente: "))
        repo_clientes.remover_cliente_por_id(id_cliente)
        repo_clientes.salvar_dados()
        print(f"Cliente {id_cliente} removido com sucesso!")

    else:
        print(f"Comando '{comando}' não reconhecido para cliente")
