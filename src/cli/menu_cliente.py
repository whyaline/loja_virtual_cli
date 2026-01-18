from src.repositorios.repositorio_clientes import RepositorioClientes
from src.modelos.cliente import Cliente
from src.modelos.endereco import Endereco
import src.sessao as Sessao

repo_clientes = RepositorioClientes()


def menu_cliente():
    while True:
        print("\n1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Editar cliente")
        print("4 - Remover cliente")
        print("5 - Gerenciar endereços do cliente")
        print("6 - Selecionar cliente")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")

            try:
                cliente = Cliente(nome, cpf, email)
                repo_clientes.adicionar_cliente(cliente)
                print("Cliente cadastrado com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "2":
            for cliente in repo_clientes.listar_clientes():
                print(cliente)

        elif opcao == "3":
            try:
                id_cliente = int(input("ID do cliente: "))
                nome = input("Novo nome (enter para manter): ")
                cpf = input("Novo CPF (enter para manter): ")
                email = input("Novo email (enter para manter): ")

                repo_clientes.alterar_cliente_por_id(
                    id_cliente,
                    nome_novo=nome or None,
                    cpf_novo=cpf or None,
                    email_novo=email or None
                )
                print("Cliente atualizado.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "4":
            try:
                id_cliente = int(input("ID do cliente: "))
                repo_clientes.remover_cliente_por_id(id_cliente)
                print("Cliente removido.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "5":
            id_cliente = int(input("ID do cliente: "))
            cliente = repo_clientes.buscar_cliente_por_id(id_cliente)

            if cliente is None:
                print("Cliente não encontrado.")
                continue

            while True:
                print("\n1 - Adicionar endereço")
                print("2 - Alterar endereço")
                print("3 - Remover endereço")
                print("0 - Voltar")

                opc = input("Escolha: ")

                if opc == "1":
                    cidade = input("Cidade: ")
                    uf = input("UF: ")
                    cep = int(input("CEP: "))
                    cliente.adicionar_endereco(Endereco(cidade, uf, cep))
                    print("Endereço adicionado.")

                elif opc == "2":
                    cep = int(input("CEP atual: "))
                    cidade = input("Nova cidade: ")
                    uf = input("Nova UF: ")
                    cliente.alterar_endereco(cep, cidade or None, uf or None)

                elif opc == "3":
                    cep = int(input("CEP: "))
                    cliente.remover_endereco(cep)

                elif opc == "0":
                    break

        elif opcao == "6":
            id_cliente = int(input("ID do cliente: "))
            cliente = repo_clientes.buscar_cliente_por_id(id_cliente)

            if cliente is None:
                print("Cliente não encontrado.")
                continue

            if not cliente.tem_endereco():
                print("Cliente não possui endereço.")
                continue

            Sessao.iniciar_carrinho(cliente)
            print(f"Cliente '{cliente.nome}' selecionado.")
            print("Carrinho iniciado.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
