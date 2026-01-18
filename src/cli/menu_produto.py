# src/cli/menu_produto.py

from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.modelos.produto import ProdutoFisico, ProdutoDigital

repo_produtos = RepositorioProdutos()
repo_produtos.carregar_dados()

def menu_produto():
    while True:
        print("\n=== MENU PRODUTO ===")
        print("1 - Cadastrar produto físico")
        print("2 - Cadastrar produto digital")
        print("3 - Listar produtos")
        print("4 - Editar produto")
        print("5 - Remover produto")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        # ======================
        # CADASTRAR FÍSICO
        # ======================
        if opcao == "1":
            try:
                nome = input("Nome: ")
                categoria = input("Categoria: ")
                preco = float(input("Preço: "))
                estoque = int(input("Estoque: "))
                peso = float(input("Peso: "))
                ativo = True

                produto = ProdutoFisico(
                    nome=nome,
                    categoria=categoria,
                    preco=preco,
                    estoque=estoque,
                    ativo=ativo,
                    peso=peso
                )

                repo_produtos.adicionar_produto(produto)
                repo_produtos.salvar_dados()
                print("Produto físico cadastrado com sucesso.")

            except ValueError as e:
                print(f"Erro: {e}")

        # ======================
        # CADASTRAR DIGITAL
        # ======================
        elif opcao == "2":
            try:
                nome = input("Nome: ")
                categoria = input("Categoria: ")
                preco = float(input("Preço: "))
                ativo = True

                produto = ProdutoDigital(
                    nome=nome,
                    categoria=categoria,
                    preco=preco,
                    ativo=ativo
                )

                repo_produtos.adicionar_produto(produto)
                repo_produtos.salvar_dados()
                print("Produto digital cadastrado com sucesso.")

            except ValueError as e:
                print(f"Erro: {e}")

        # ======================
        # LISTAR
        # ======================
        elif opcao == "3":
            produtos = repo_produtos.listar_produtos()
            if not produtos:
                print("Nenhum produto cadastrado.")
            for p in produtos:
                print(p)

        # ======================
        # EDITAR
        # ======================
        elif opcao == "4":
            try:
                sku = int(input("SKU do produto: "))
                nome = input("Novo nome (enter para manter): ")
                categoria = input("Nova categoria (enter para manter): ")
                preco = input("Novo preço (enter para manter): ")
                estoque = input("Novo estoque (enter para manter): ")
                ativo = input("Ativo? (s/n ou enter): ")

                repo_produtos.alterar_produto(
                    sku=sku,
                    nome_novo=nome or None,
                    categoria_nova=categoria or None,
                    preco_novo=float(preco) if preco else None,
                    estoque_novo=int(estoque) if estoque else None,
                    ativo_novo=True if ativo.lower() == "s" else False if ativo.lower() == "n" else None
                )

                repo_produtos.salvar_dados()
                print("Produto atualizado com sucesso.")

            except ValueError as e:
                print(f"Erro: {e}")

        # ======================
        # REMOVER
        # ======================
        elif opcao == "5":
            try:
                sku = int(input("SKU do produto: "))
                repo_produtos.remover_produto_por_sku(sku)
                repo_produtos.salvar_dados()
                print("Produto removido com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
