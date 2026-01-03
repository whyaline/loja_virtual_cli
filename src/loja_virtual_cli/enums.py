from enum import Enum

class StatusPedido(Enum):
    CRIADO = "CRIADO"
    PAGO = "PAGO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"
