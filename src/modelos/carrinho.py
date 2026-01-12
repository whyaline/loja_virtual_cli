from src.modelos.item_carrinho import ItemCarrinho
from src.modelos.cupom import Cupom


class Carrinho:
    def __init__(self):
        self.itens = []
        self.cupom_preview = None

    def adicionar_item(self, item_novo: ItemCarrinho): #se já existir o produto apenas aumenta sua qtde
        for item in self.itens:
            if item == item_novo:
                item.adicionar_qtde(item_novo.qtde) 
                return

        self.itens.append(item_novo)

    def remover_item_por_sku(self, sku): # se qtde do item <= 0 -> retira do  carrinho
        item = self.buscar_item_por_sku(sku)

        if item is None:
            raise ValueError("Produto não encontrado!")

        self.itens.remove(item)

    def buscar_item_por_sku(self, sku):
        for item in self.itens:
            if item.produto.sku == sku:
                return item
        return None

    def listar_itens(self):
        if not self.itens:
            return "Carrinho vazio."

        linhas = []
        for item in self.itens:
            linhas.append(f"SKU: {item.produto.sku} - {item.produto.nome} - Qtde: {item.qtde} - Subtotal: {item.calcular_subtotal():.2f}")

        linhas.append(f"Total do carrinho: R$ {self.calcular_subtotal():.2f}")
        return "\n".join(linhas)

    def calcular_subtotal(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def aplicar_cupom_preview(self, cupom: Cupom, categoria):
        cupom.validar_uso(categoria)
        self.cupom_preview = cupom

    def calcular_total_preview(self, frete):
        subtotal = self.calcular_subtotal()
        desconto = 0

        if self.cupom_preview:
            # calcula apenas o subtotal elegível ao cupom
            if self.cupom_preview.categorias_elegiveis:
                subtotal_elegivel = sum(
                    item.calcular_subtotal()
                    for item in self.itens
                    if item.produto.categoria.upper() in self.cupom_preview.categorias_elegiveis
                )
            else:
                subtotal_elegivel = subtotal

            desconto = self.cupom_preview.calcular_desconto(subtotal_elegivel)

        total = subtotal - desconto + (frete.valor if frete else 0)
        return total


    def limpar(self):
        self.itens.clear()

    #métodos especiais
    def __str__(self):
        return self.listar_itens()

    def __repr__(self):
        return f"Carrinho(itens={self.itens!r})"

    def __len__(self):
        return len(self.itens)