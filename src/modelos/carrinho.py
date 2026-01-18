from src.modelos.item_carrinho import ItemCarrinho
from src.modelos.cupom import Cupom


class Carrinho:
    def __init__(self):
        self.itens = []
        self.cupom_preview = None
        self.frete = None  # instância de Frete já calculada

    # =========================
    # ITENS
    # =========================
    def adicionar_item(self, item_novo: ItemCarrinho):
        for item in self.itens:
            if item.produto.sku == item_novo.produto.sku:
                item.adicionar_qtde(item_novo.qtde)
                return
        self.itens.append(item_novo)

    def remover_item_por_sku(self, sku):
        item = self.buscar_item_por_sku(sku)
        if item is None:
            raise ValueError("Produto não encontrado no carrinho.")
        self.itens.remove(item)

    def buscar_item_por_sku(self, sku):
        for item in self.itens:
            if item.produto.sku == sku:
                return item
        return None

    def esta_vazio(self):
        return len(self.itens) == 0

    # =========================
    # CUPOM
    # =========================
    def aplicar_cupom_preview(self, cupom: Cupom):
        self.cupom_preview = cupom

    def calcular_desconto_preview(self):
        if not self.cupom_preview:
            return 0

        subtotal = self.calcular_subtotal()

        if self.cupom_preview.categorias_elegiveis:
            subtotal_elegivel = sum(
                item.calcular_subtotal()
                for item in self.itens
                if item.produto.categoria.upper()
                in self.cupom_preview.categorias_elegiveis
            )
        else:
            subtotal_elegivel = subtotal

        return self.cupom_preview.calcular_desconto(subtotal_elegivel)

    # =========================
    # FRETE
    # =========================
    def aplicar_frete_preview(self, frete):
        frete.calcular_preview(self)
        self.frete = frete

    @property
    def valor_frete(self):
        return self.frete.valor if self.frete else 0

    @property
    def prazo_frete(self):
        return self.frete.prazo if self.frete else 0

    # =========================
    # TOTAIS
    # =========================
    def calcular_subtotal(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def calcular_total_preview(self):
        subtotal = self.calcular_subtotal()
        desconto = self.calcular_desconto_preview()
        return subtotal - desconto + self.valor_frete

    # =========================
    # UTILIDADES
    # =========================
    def limpar(self):
        self.itens.clear()
        self.cupom_preview = None
        self.frete = None

    def listar_itens(self):
        if not self.itens:
            return "Carrinho vazio."

        linhas = ["=== CARRINHO ==="]

        for item in self.itens:
            linhas.append(
                f"SKU: {item.produto.sku} | "
                f"{item.produto.nome} | "
                f"Qtde: {item.qtde} | "
                f"Subtotal: R$ {item.calcular_subtotal():.2f}"
            )

        subtotal = self.calcular_subtotal()
        linhas.append(f"\nSubtotal: R$ {subtotal:.2f}")

        desconto = self.calcular_desconto_preview()
        if desconto > 0:
            linhas.append(f"Desconto: -R$ {desconto:.2f}")

        if self.frete:
            linhas.append(f"Frete: R$ {self.frete.valor:.2f} (Prazo: {self.frete.prazo} dias)")

        total = self.calcular_total_preview()
        linhas.append(f"\nTotal: R$ {total:.2f}")

        return "\n".join(linhas)

    # =========================
    # MÉTODOS ESPECIAIS
    # =========================
    def __str__(self):
        return self.listar_itens()

    def __len__(self):
        return len(self.itens)

    def __repr__(self):
        return f"Carrinho(itens={self.itens!r})"
