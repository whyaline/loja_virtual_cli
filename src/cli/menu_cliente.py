# cli/menu_cliente.py

from src.repositorios.repositorio_clientes import RepositorioClientes
from src.modelos.cliente import Cliente
from src.modelos.endereco import Endereco

repo_clientes = RepositorioClientes()

def menu_cliente():
    while True:
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Editar cliente")
        print("4 - Remover cliente")
        print("5 - Gerenciar endereços do cliente")
        print("0 - Voltar")


        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")

            try:
                cliente = Cliente(nome=nome, cpf=cpf, email=email)
                repo_clientes.adicionar_cliente(cliente)
                print("Cliente cadastrado com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "2":
            clientes = repo_clientes.listar_clientes()
            if not clientes:
                print("Nenhum cliente cadastrado.")
            for cliente in clientes:
                print(cliente)

        elif opcao == "3":
            try:
                id_cliente = int(input("ID do cliente: "))
                nome = input("Novo nome (enter para manter): ")
                cpf = input("Novo CPF (enter para manter): ")
                email = input("Novo email (enter para manter): ")

                repo_clientes.alterar_cliente_por_id(
                    id=id_cliente,
                    nome_novo=nome or None,
                    cpf_novo=cpf or None,
                    email_novo=email or None
                )
                print("Cliente atualizado com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "4":
            try:
                id_cliente = int(input("ID do cliente: "))
                repo_clientes.remover_cliente_por_id(id_cliente)
                print("Cliente removido com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "5":
            try:
                id_cliente = int(input("ID do cliente: "))
                cliente = repo_clientes.buscar_cliente_por_id(id_cliente)

                if cliente is None:
                    print("Cliente não encontrado.")
                    continue

                while True:
                    print("\n=== ENDEREÇOS DO CLIENTE ===")
                    print("1 - Adicionar endereço")
                    print("2 - Buscar endereço por CEP")
                    print("3 - Alterar endereço")
                    print("4 - Remover endereço")
                    print("0 - Voltar")

                    opc_end = input("Escolha uma opção: ")

                    # 1 - adicionar_endereco
                    if opc_end == "1":
                        try:
                            cidade = input("Cidade: ")
                            uf = input("UF: ")
                            cep = input("CEP (apenas números): ")

                            endereco = Endereco(
                                cidade=cidade,
                                uf=uf,
                                cep=int(cep)
                            )

                            cliente.adicionar_endereco(endereco)
                            print("Endereço adicionado com sucesso.")

                        except ValueError as e:
                            print(f"Erro: {e}")

                    # 2 - buscar_endereco_por_cep
                    elif opc_end == "2":
                        try:
                            cep = int(input("Informe o CEP: "))
                            endereco = cliente.buscar_endereco_por_cep(cep)

                            if endereco:
                                print(endereco)
                            else:
                                print("Endereço não encontrado.")

                        except ValueError as e:
                            print(f"Erro: {e}")

                    # 3 - alterar_endereco
                    elif opc_end == "3":
                        try:
                            cep = int(input("CEP do endereço a alterar: "))

                            cidade = input("Nova cidade (enter para manter): ")
                            uf = input("Nova UF (enter para manter): ")
                            cep_novo = input("Novo CEP (enter para manter): ")

                            cliente.alterar_endereco(
                                cep=cep,
                                cidade_novo=cidade or None,
                                uf_novo=uf or None,
                                cep_novo=int(cep_novo) if cep_novo else None
                            )

                            print("Endereço alterado com sucesso.")

                        except ValueError as e:
                            print(f"Erro: {e}")

                    # 4 - remover_endereco
                    elif opc_end == "4":
                        try:
                            cep = int(input("CEP do endereço a remover: "))
                            cliente.remover_endereco(cep)
                            print("Endereço removido com sucesso.")

                        except ValueError as e:
                            print(f"Erro: {e}")

                    elif opc_end == "0":
                        break

                    else:
                        print("Opção inválida.")

            except ValueError as e:
                print(f"Erro: {e}")


        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
