import src.sessao as Sessao
from src.modelos.pedido import Pedido
from src.modelos.pagamento import Pagamento
from src.utils.enums import FormaPagamento, StatusPagamento
from datetime import datetime


def menu_pedido_cliente(repo_pedidos):
    """
    Menu de pedidos para o cliente.
    Recebe o mesmo repositório de pedidos usado pelo admin.
    """
    if not Sessao.cliente_atual:
        print("Nenhum cliente selecionado.")
        return

    while True:
        print("\n=== MEUS PEDIDOS ===")
        print("1 - Criar pedido")
        print("2 - Listar meus pedidos")
        print("3 - Ver resumo do pedido")
        print("4 - Pagar pedido")
        print("5 - Cancelar pedido")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_pedido(repo_pedidos)
        elif opcao == "2":
            listar_meus_pedidos(repo_pedidos)
        elif opcao == "3":
            resumo_pedido(repo_pedidos)
        elif opcao == "4":
            pagar_pedido(repo_pedidos)
        elif opcao == "5":
            cancelar_pedido(repo_pedidos)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# =========================
# FUNÇÕES AUXILIARES
# =========================
def criar_pedido(repo_pedidos):
    if not Sessao.carrinho or not Sessao.carrinho.itens:
        print("Carrinho vazio.")
        return

    if not Sessao.endereco_entrega:
        print("Endereço de entrega não selecionado.")
        return

    carrinho = Sessao.carrinho
    desconto = carrinho.calcular_desconto_preview()
    frete_valor = carrinho.valor_frete

    try:
        pedido = Pedido(
            cliente=Sessao.cliente_atual,
            endereco=Sessao.endereco_entrega,
            carrinho=carrinho,
            frete_valor=frete_valor,
            desconto=desconto
        )

        repo_pedidos.adicionar_pedido(pedido)
        repo_pedidos.salvar_dados()

        # Limpa carrinho
        Sessao.carrinho.limpar()
        Sessao.carrinho = None
        Sessao.cupom = None
        Sessao.frete = None

        print(f"Pedido criado com sucesso. ID: {pedido.id}")

    except ValueError as e:
        print(f"Erro ao criar pedido: {e}")


def listar_meus_pedidos(repo_pedidos):
    pedidos = [p for p in repo_pedidos.listar_pedidos() if p.cliente.id == Sessao.cliente_atual.id]

    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    print("\nMeus pedidos:")
    for p in pedidos:
        total_pago = sum(pg.valor for pg in p.pagamentos if pg.status == StatusPagamento.CONFIRMADO)
        saldo_devedor = max(p.total - total_pago, 0)
        status = p.status.value
        if saldo_devedor > 0 and total_pago > 0:
            status += " (Pagamento parcial)"
        print(f"ID: {p.id} | Status: {status} | Total: R$ {p.total:.2f}")


def resumo_pedido(repo_pedidos):
    try:
        id_pedido = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(id_pedido)
    if not pedido or pedido.cliente.id != Sessao.cliente_atual.id:
        print("Pedido não encontrado.")
        return

    print("\n" + pedido.resumo())

    if pedido.pagamentos:
        print("\nPagamentos:")
        for pg in pedido.pagamentos:
            print(f"  Valor: R$ {pg.valor:.2f} | Forma: {pg.forma.value} | Status: {pg.status.value}")
    else:
        print("\nNenhum pagamento registrado.")


def pagar_pedido(repo_pedidos):
    try:
        id_pedido = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(id_pedido)
    if not pedido or pedido.cliente.id != Sessao.cliente_atual.id:
        print("Pedido não encontrado.")
        return

    total_pago = sum(p.valor for p in pedido.pagamentos if p.status == StatusPagamento.CONFIRMADO)
    saldo_devedor = pedido.total - total_pago

    if saldo_devedor <= 0:
        print("Pedido já totalmente pago.")
        return

    try:
        valor = float(input(f"Valor do pagamento (Saldo restante: R$ {saldo_devedor:.2f}): "))
    except ValueError:
        print("Valor inválido.")
        return

    if valor <= 0:
        print("O valor do pagamento deve ser positivo.")
        return
    if valor > saldo_devedor:
        print(f"O valor não pode ser maior que o saldo devedor ({saldo_devedor:.2f}).")
        return

    # Seleção da forma de pagamento
    print("Formas de pagamento disponíveis:")
    for i, forma in enumerate(FormaPagamento, start=1):
        print(f"{i} - {forma.value}")

    try:
        opc = int(input("Escolha a forma de pagamento: "))
        forma_selecionada = list(FormaPagamento)[opc - 1]
    except (ValueError, IndexError):
        print("Forma de pagamento inválida.")
        return

    pagamento = Pagamento(pedido=pedido, valor=valor, forma=forma_selecionada)
    sucesso = pagamento.processar()

    if sucesso:
        pedido.registrar_pagamento(pagamento)
        repo_pedidos.salvar_dados()
        print(f"Pagamento de R$ {valor:.2f} registrado com sucesso para o pedido {pedido.id}.")


def cancelar_pedido(repo_pedidos):
    try:
        id_pedido = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(id_pedido)
    if not pedido or pedido.cliente.id != Sessao.cliente_atual.id:
        print("Pedido não encontrado.")
        return

    try:
        pedido.cancelar()
        repo_pedidos.salvar_dados()
        print("Pedido cancelado com sucesso.")
    except ValueError as e:
        print(f"Erro: {e}")
