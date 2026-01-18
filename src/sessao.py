from src.modelos.carrinho import Carrinho

cliente_atual = None
carrinho = None
frete = None
cupom = None
endereco_entrega = None


def iniciar_carrinho(cliente):
    global cliente_atual, carrinho, frete, cupom, endereco_entrega

    cliente_atual = cliente
    carrinho = Carrinho()
    frete = None
    cupom = None

    endereco_entrega = cliente.enderecos[0] if cliente.enderecos else None
