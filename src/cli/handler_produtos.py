# src/cli/handler_produtos.py
from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.modelos.produto import ProdutoFisico, ProdutoDigital

repo_produtos = RepositorioProdutos()
repo_produtos.carregar_dados()

def handle_produtos(args):
    if not args:
        print("Comando do produto não especificado")
        return

    comando = args[0].lower()

    if comando == "cadastrar":
        tipo = input("Tipo (fisico/digital): ").lower()
        nome = input("Nome: ")
        categoria = input("Categoria: ")
        preco = float(input("Preço: "))
        estoque = int(input("Estoque: ")) if tipo == "fisico" else 0

        if tipo == "fisico":
            produto = ProdutoFisico(nome, categoria, preco, estoque)
        else:
            produto = ProdutoDigital(nome, categoria, preco)

        repo_produtos.adicionar_produto(produto)
        repo_produtos.salvar_dados()
        print(f"Produto {nome} cadastrado!")

    elif comando == "listar":
        somente_ativos = "--ativos" in args
        for p in repo_produtos.listar_produtos(somente_ativos):
            print(p)

    elif comando == "editar":
        sku = int(input("SKU do produto: "))
        nome = input("Novo nome (Enter para manter): ")
        categoria = input("Nova categoria (Enter para manter): ")
        preco = input("Novo preço (Enter para manter): ")
        estoque = input("Novo estoque (Enter para manter): ")
        ativo = input("Ativo? (s/n Enter para manter): ")

        repo_produtos.alterar_produto(
            sku,
            nome or None,
            categoria or None,
            float(preco) if preco else None,
            int(estoque) if estoque else None,
            True if ativo.lower() == "s" else False if ativo.lower() == "n" else None
        )
        repo_produtos.salvar_dados()
        print(f"Produto {sku} editado!")

    elif comando == "remover":
        sku = int(input("SKU do produto: "))
        repo_produtos.remover_produto_por_sku(sku)
        repo_produtos.salvar_dados()
        print(f"Produto {sku} removido!")

    else:
        print(f"Comando '{comando}' não reconhecido para produto")
