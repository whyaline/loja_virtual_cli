from src.modelos.item_carrinho import ItemCarrinho
from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.repositorios.repositorio_cupons import RepositorioCupons
from src.modelos.frete import Frete
import src.sessao as Sessao


repo_produtos = RepositorioProdutos()
repo_produtos.carregar_dados()

repo_cupons = RepositorioCupons()
repo_cupons.carregar_dados()


def menu_carrinho():
    if Sessao.carrinho is None:
        print("Nenhum cliente selecionado.")
        return

    while True:
        print("\n=== MENU CARRINHO ===")
        print("1 - Adicionar item")
        print("2 - Remover item")
        print("3 - Listar carrinho")
        print("4 - Aplicar cupom")
        print("5 - Limpar carrinho")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        # -------------------------
        # ADICIONAR ITEM
        # -------------------------
        if opcao == "1":
            try:
                sku = int(input("SKU: "))
                qtde = int(input("Quantidade: "))

                produto = repo_produtos.buscar_produto_por_sku(sku)

                if produto is None or not produto.ativo:
                    print("Produto inválido.")
                    continue

                if qtde > produto.estoque:
                    print("Estoque insuficiente.")
                    continue

                item = ItemCarrinho(produto, qtde)
                Sessao.carrinho.adicionar_item(item)

                # qualquer alteração invalida frete e cupom
                Sessao.carrinho.frete = None
                Sessao.carrinho.cupom_preview = None
                Sessao.frete = None
                Sessao.cupom = None

                print("Item adicionado.")

            except ValueError:
                print("Dados inválidos.")

        # -------------------------
        # REMOVER ITEM
        # -------------------------
        elif opcao == "2":
            try:
                sku = int(input("SKU: "))
                Sessao.carrinho.remover_item_por_sku(sku)

                Sessao.carrinho.frete = None
                Sessao.carrinho.cupom_preview = None
                Sessao.frete = None
                Sessao.cupom = None

                print("Item removido.")

            except ValueError as e:
                print(e)

        # -------------------------
        # LISTAR CARRINHO
        # -------------------------
        elif opcao == "3":
            if len(Sessao.carrinho) == 0:
                print("Carrinho vazio.")
                continue

            # calcula frete automaticamente
            if Sessao.carrinho.frete is None:
                if Sessao.endereco_entrega is None:
                    print("Nenhum endereço de entrega selecionado.")
                else:
                    frete = Frete(Sessao.endereco_entrega)
                    Sessao.carrinho.aplicar_frete_preview(frete)
                    Sessao.frete = frete

            print(Sessao.carrinho)

        # -------------------------
        # APLICAR CUPOM
        # -------------------------
        elif opcao == "4":
            try:
                if len(Sessao.carrinho) == 0:
                    print("Carrinho vazio.")
                    continue

                codigo = input("Cupom: ").upper()
                cupom = repo_cupons.buscar_por_codigo(codigo)

                if cupom is None:
                    print("Cupom inválido.")
                    continue

                categorias = {item.produto.categoria for item in Sessao.carrinho.itens}
                for categoria in categorias:
                    cupom.validar_uso(categoria)

                Sessao.carrinho.aplicar_cupom_preview(cupom)
                Sessao.cupom = cupom

                print("Cupom aplicado.")

            except ValueError as e:
                print(e)

        # -------------------------
        # LIMPAR CARRINHO
        # -------------------------
        elif opcao == "5":
            Sessao.carrinho.limpar()
            Sessao.frete = None
            Sessao.cupom = None
            print("Carrinho limpo.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
