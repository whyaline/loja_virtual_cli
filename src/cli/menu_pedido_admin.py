from src.modelos.endereco import Endereco

# =========================
# MENU ADMIN
# =========================
def menu_pedido_admin(repo_pedidos):
    while True:
        print("\n=== GERENCIAR PEDIDOS ===")
        print("1 - Listar todos os pedidos")
        print("2 - Ver resumo do pedido")
        print("3 - Enviar pedido")
        print("4 - Entregar pedido")
        print("5 - Cancelar pedido")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_todos(repo_pedidos)
        elif opcao == "2":
            resumo(repo_pedidos)
        elif opcao == "3":
            enviar(repo_pedidos)
        elif opcao == "4":
            entregar(repo_pedidos)
        elif opcao == "5":
            cancelar(repo_pedidos)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# =========================
# FUNÇÕES AUXILIARES
# =========================
def listar_todos(repo_pedidos):
    pedidos = repo_pedidos.listar_pedidos()
    if not pedidos:
        print("Nenhum pedido cadastrado.")
        return

    print("\nTodos os pedidos:")
    for p in pedidos:
        print(
            f"ID: {p.id} | "
            f"Cliente: {p.cliente.nome if p.cliente else 'N/D'} | "
            f"Status: {p.status.value} | "
            f"Total: R$ {p.total:.2f}"
        )


def resumo(repo_pedidos):
    try:
        pedido_id = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
    if not pedido:
        print("Pedido não encontrado.")
        return

    print(pedido.resumo())


def enviar(repo_pedidos):
    try:
        pedido_id = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
    if not pedido:
        print("Pedido não encontrado.")
        return

    try:
        pedido.enviar()
        repo_pedidos.salvar_dados()
        print(f"Pedido {pedido.id} enviado. Código de rastreio: {pedido.codigo_rastreio}")
    except ValueError as e:
        print(f"Erro: {e}")


def entregar(repo_pedidos):
    try:
        pedido_id = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
    if not pedido:
        print("Pedido não encontrado.")
        return

    try:
        pedido.entregar()
        repo_pedidos.salvar_dados()
        print(f"Pedido {pedido.id} entregue.")
    except ValueError as e:
        print(f"Erro: {e}")


def cancelar(repo_pedidos):
    try:
        pedido_id = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    pedido = repo_pedidos.buscar_pedido_por_id(pedido_id)
    if not pedido:
        print("Pedido não encontrado.")
        return

    try:
        pedido.cancelar()
        repo_pedidos.salvar_dados()
        print(f"Pedido {pedido.id} cancelado com sucesso.")
    except ValueError as e:
        print(f"Erro: {e}")
