import src.sessao as Sessao
from src.modelos.item_carrinho import ItemCarrinho
from src.modelos.frete import Frete
from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.repositorios.repositorio_cupons import RepositorioCupons
from src.cli.menu_pedido_cliente import criar_pedido

# =========================
# REPOSITÓRIOS
# =========================
repo_produtos = RepositorioProdutos()
repo_produtos.carregar_dados()

repo_cupons = RepositorioCupons()
repo_cupons.carregar_dados()


def menu_carrinho(repo_pedidos):
    if Sessao.carrinho is None:
        print("Nenhum cliente selecionado ou carrinho não iniciado.")
        return

    while True:
        print("\n=== MENU CARRINHO ===")
        print("1 - Adicionar item")
        print("2 - Remover item")
        print("3 - Listar carrinho")
        print("4 - Aplicar cupom")
        print("5 - Limpar carrinho")
        print("6 - Fechar pedido")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                sku = int(input("SKU: "))
                qtde = int(input("Quantidade: "))
            except ValueError:
                print("SKU ou quantidade inválidos.")
                continue

            produto = repo_produtos.buscar_produto_por_sku(sku)
            if not produto or not produto.ativo or qtde > produto.estoque:
                print("Produto inválido ou quantidade indisponível.")
                continue

            Sessao.carrinho.adicionar_item(ItemCarrinho(produto, qtde))
            Sessao.frete = None
            Sessao.cupom = None
            print("Item adicionado.")

        elif opcao == "2":
            try:
                sku = int(input("SKU: "))
                Sessao.carrinho.remover_item_por_sku(sku)
                Sessao.frete = None
                Sessao.cupom = None
                print("Item removido.")
            except ValueError:
                print("SKU inválido.")

        elif opcao == "3":
            if len(Sessao.carrinho) == 0:
                print("Carrinho vazio.")
                continue

            if Sessao.carrinho.frete is None and Sessao.endereco_entrega:
                frete = Frete(Sessao.endereco_entrega)
                frete.calcular_preview(Sessao.carrinho)
                Sessao.carrinho.aplicar_frete_preview(frete)

            print(Sessao.carrinho)

        elif opcao == "4":
            codigo = input("Cupom: ").upper()
            cupom = repo_cupons.buscar_por_codigo(codigo)
            if cupom:
                Sessao.carrinho.aplicar_cupom_preview(cupom)
                Sessao.cupom = cupom
                print("Cupom aplicado.")
            else:
                print("Cupom inválido.")

        elif opcao == "5":
            Sessao.carrinho.limpar()
            Sessao.frete = None
            Sessao.cupom = None
            print("Carrinho limpo.")

        elif opcao == "6":  # fechar pedido
            if not Sessao.carrinho or not Sessao.carrinho.itens:
                print("Carrinho vazio, impossível criar pedido.")
            else:
                criar_pedido(repo_pedidos)  # <-- passa repo_pedidos

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
