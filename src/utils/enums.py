from enum import Enum

class StatusPedido(Enum):
    CRIADO = "CRIADO"
    PAGO = "PAGO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"
    
class FormaPagamento(Enum):
    PIX = "PIX"
    CREDITO = "CREDITO"
    DEBITO = "DEBITO"
    BOLETO = "BOLETO"

class StatusPagamento(Enum):
    PENDENTE = "PENDENTE"
    CONFIRMADO = "CONFIRMADO"
    ESTORNADO = "ESTORNADO"
    CANCELADO = "CANCELADO"