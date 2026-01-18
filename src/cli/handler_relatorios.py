# src/cli/handler_relatorios.py
from src.repositorios.repositorio_pedidos import RepositorioPedidos
from src.relatorios.relatorio_faturamento import gerar_relatorio_faturamento

repo_pedidos = RepositorioPedidos()

def handle_relatorios(args):
    if not args:
        print("Comando de relatório não especificado")
        return

    comando = args[0].lower()

    pedidos = repo_pedidos.listar_pedidos()

    if comando == "faturamento":
        total = sum(p.total for p in pedidos if p.status != "CANCELADO")
        print(f"Total faturado: R$ {total:.2f}")

    elif comando == "top":
        top_n = int(args[1]) if len(args) > 1 else 5
        top_produtos, ticket_medio = gerar_relatorio_faturamento(pedidos, top_n)
        print("Top produtos:")
        for nome, qtd in top_produtos:
            print(f"{nome}: {qtd}")
        print(f"Ticket médio: R$ {ticket_medio:.2f}")

    elif comando == "categoria":
        print("Relatório por categoria: (em implementação futura)")

    elif comando == "uf":
        print("Relatório por UF: (em implementação futura)")

    else:
        print(f"Comando de relatório '{comando}' não reconhecido")
