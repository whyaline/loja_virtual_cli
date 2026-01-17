from datetime import date, timedelta, datetime
from src.utils.enums import StatusPedido, StatusPagamento, FormaPagamento
import json
import random
import string

from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.repositorios.repositorio_pedidos import RepositorioPedidos
from src.modelos.produto import ProdutoFisico, ProdutoDigital
from src.modelos.item_pedido import ItemPedido
from src.modelos.cupom import Cupom
from src.modelos.endereco import Endereco
from src.modelos.cliente import Cliente
from src.modelos.carrinho import Carrinho
from src.modelos.frete import Frete
from src.modelos.item_carrinho import ItemCarrinho
from src.modelos.pagamento import Pagamento
from src.modelos.pedido import Pedido




def separador(titulo):
    print("\n" + "=" * 10, titulo, "=" * 10)


def run_all_tests():
    print("\n--- EXECUTANDO TODOS OS TESTES EM UMA ÚNICA CÉLULA ---")

    # ==================== SETTINGS INITIALIZATION ====================
    print("\n===== INICIALIZANDO CONFIGURAÇÕES (SETTINGS) =====")
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
        global tabela_frete, default_coupon_validity_days
        tabela_frete = {
            faixa["uf"]: {
                "valor": faixa["valor"],
                "prazo": faixa["prazo"]
            }
            for faixa in settings["frete"]["faixas_cep"]
        }
        tabela_frete["default"] = settings["frete"]["default"]
        default_coupon_validity_days = settings["coupon"]["default_validity_days"]
        print("Configurações de frete e cupom carregadas.")
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return # Stop if settings can't be loaded

    # ==================== CLASSE VALIDAÇÕES ====================
    print("\n===== TESTANDO VALIDAÇÕES =====")
    print("Validações (validar_string, validar_numero) são testadas indiretamente pelas classes que as utilizam.")

    # ==================== CLASSE ENDERECO ====================
    print("\n===== TESTANDO CLASSE ENDERECO =====")
    # Endereço é testado implicitamente em Cliente e Frete.
    print("Classe Endereco testada indiretamente pelos testes de Cliente e Frete.")

    # ==================== CLASSE PRODUTO (e subclasses) ====================
    print("\n===== TESTANDO CLASSE PRODUTO (e suas subclasses) =====")

    # Testar RepositorioProdutos (inclui Produto, ProdutoFisico, ProdutoDigital)
    print("=== CRIAÇÃO DO REPOSITÓRIO ===")
    try:
        repo = RepositorioProdutos()
        print("Repositório criado com sucesso")
    except Exception as e:
        print("Erro ao criar repositório:", e)

    print("\n=== CRIAÇÃO DE PRODUTOS ===")
    try:
        p1 = ProdutoFisico("Notebook", "Eletrônicos", 3500.00, 10, True, 2.5)
        p2 = ProdutoFisico("Mouse", "Acessórios", 80.00, 20, True, 0.2)
        p3 = ProdutoDigital("Curso Python", "Educação", 199.90, 0, True)
        print("Produtos criados com sucesso")
    except Exception as e:
        print("Erro ao criar produtos:", e)

    print("\n=== ADIÇÃO AO REPOSITÓRIO (SKU AUTOMÁTICO) ===")
    try:
        repo.adicionar_produto(p1)
        repo.adicionar_produto(p2)
        repo.adicionar_produto(p3)

        print("Produtos adicionados")
        print("SKU p1:", p1.sku)
        print("SKU p2:", p2.sku)
        print("SKU p3:", p3.sku)
    except Exception as e:
        print("Erro ao adicionar produtos:", e)

    print("\n=== LISTAGEM DE PRODUTOS ===")
    try:
        for produto in repo.listar_produtos():
            print(produto)
    except Exception as e:
        print("Erro ao listar produtos:", e)

    print("\n=== TESTE DE BUSCA POR SKU ===")
    try:
        produto = repo.buscar_produto_por_sku(2)
        print("Produto encontrado:", produto)
    except Exception as e:
        print("Erro na busca:", e)

    print("\n=== TESTE DE ALTERAÇÃO DE PRODUTO ===")
    try:
        repo.alterar_produto(
            sku=2,
            preco_novo=90.00,
            estoque_novo=15,
            ativo_novo=False
        )
        print("Produto alterado:", repo.buscar_produto_por_sku(2))
    except Exception as e:
        print("Erro ao alterar produto:", e)

    print("\n=== LISTAGEM SOMENTE ATIVOS ===")
    try:
        for produto in repo.listar_produtos(somente_ativos=True):
            print(produto)
    except Exception as e:
        print("Erro ao listar ativos:", e)

    print("\n=== TESTE DE __eq__ (SKU) ===")
    try:
        print("p1 == p2 ?", p1 == p2)
        print("p1 == p1 ?", p1 == p1)
    except Exception as e:
        print("Erro no __eq__:", e)

    print("\n=== TESTE DE ORDENAÇÃO (por preço) ===")
    try:
        produtos_ordenados = sorted(repo.listar_produtos())
        for prod_sorted in produtos_ordenados:
            print(f"{prod_sorted.nome} - R$ {prod_sorted.preco}")
    except Exception as e:
        print("Erro na ordenação:", e)

    print("\n=== TESTE DE FRETE ===")
    try:
        print("Notebook tem frete?", p1.tem_frete())
        print("Curso Python tem frete?", p3.tem_frete())
    except Exception as e:
        print("Erro no teste de frete:", e)

    print("\n=== TESTE DE ESTOQUE ===")
    try:
        print("Estoque inicial p2:", p2.estoque)
        p2.remover_estoque(5)
        print("Após remover:", p2.estoque)
        p2.adicionar_estoque(10)
        print("Após adicionar:", p2.estoque)
    except Exception as e:
        print("Erro no controle de estoque:", e)

    print("\n=== TESTE DE ERRO: ESTOQUE INSUFICIENTE ===")
    try:
        p2.remover_estoque(100)
    except Exception as e:
        print("Erro esperado:", e)

    print("\n=== TESTE DE PRODUTO INATIVO ===")
    try:
        p2.adicionar_estoque(5)
    except Exception as e:
        print("Erro esperado:", e)

    print("\n=== TESTE DE REMOÇÃO ===")
    try:
        repo.remover_produto_por_sku(1)
        print("Produto removido. Produtos restantes:")
        for prod_rem in repo.listar_produtos():
            print(prod_rem)
    except Exception as e:
        print("Erro ao remover produto:", e)
    print("=== FIM DOS TESTES DE PRODUTO ===")

    # ==================== CLASSE CLIENTE ====================
    print("\n===== TESTANDO CLASSE CLIENTE =====")
    print("Classe Cliente testada indiretamente pelos testes de Pedido.")

    # ==================== CLASSE ITEMCARRINHO & ITEMPEDIDO ====================
    print("\n===== TESTANDO CLASSE ITEMCARRINHO & ITEMPEDIDO =====")
    print("=== TESTE ITEM PEDIDO ===")
    repo_produtos_item_test = RepositorioProdutos()
    produto_ex = ProdutoFisico("Mouse", "ELETRONICOS", 200.0, 10, True, 0.5)
    repo_produtos_item_test.adicionar_produto(produto_ex)
    try:
        item = ItemPedido(produto_ex, 3)
        print(item)
        print("Subtotal calculado:", item.subtotal)
    except Exception as e:
        print("Erro ao criar ItemPedido válido:", e)
    try:
        ItemPedido(produto_ex, 0)
    except ValueError as e:
        print("Erro esperado:", e)
    print()

    # ==================== CLASSE CUPOM ====================
    print("\n===== TESTANDO CLASSE CUPOM =====")
    separador("CRIAÇÃO VÁLIDA")
    try:
        cupom_valido = Cupom(
            codigo="DESC10",
            tipo="percentual",
            valor=10,
            data_validade=date.today() + timedelta(days=10),
            uso_maximo=5,
            usos_feitos=0,
            categorias_elegiveis=["ELETRONICOS"]
        )
        print("Cupom criado com sucesso:", cupom_valido)
        assert cupom_valido.data_validade == date.today() + timedelta(days=10)
    except Exception as e:
        print("Erro na criação válida:", e)

    separador("CRIAÇÃO COM VALIDADE PADRÃO")
    try:
        cupom_default = Cupom(
            codigo="DEFAULT30",
            tipo="VALOR",
            valor=25,
            uso_maximo=10,
            usos_feitos=0
        )
        expected_date = date.today() + timedelta(days=default_coupon_validity_days)
        print(f"Cupom com validade padrão criado: {cupom_default.data_validade}")
        print(f"Data esperada: {expected_date}")
        assert cupom_default.data_validade == expected_date
        print("Validade padrão definida corretamente.")
    except Exception as e:
        print("Erro na criação com validade padrão:", e)

    separador("TIPO INVÁLIDO")
    try:
        Cupom(
            codigo="ERRO1",
            tipo="OUTRO",
            valor=10,
            data_validade=date.today() + timedelta(days=1),
            uso_maximo=1,
            usos_feitos=0
        )
        print("❌ Teste tipo inválido - FALHA (Não levantou exceção)")
    except ValueError as e:
        print("Erro esperado:", e)

    separador("VALIDAÇÃO DE USO")
    try:
        cupom_validacao = Cupom(
            codigo="VALOR50",
            tipo="VALOR",
            valor=50,
            data_validade=date.today() + timedelta(days=5),
            uso_maximo=1,
            usos_feitos=0,
            categorias_elegiveis=["LIVROS"]
        )
        cupom_validacao.validar_uso("LIVROS")
        print("Validação OK")
    except Exception as e:
        print("Erro na validação de uso (esperado OK):", e)
    try:
        cupom_validacao.validar_uso("ELETRONICOS")
        print("❌ Teste validação de uso - FALHA (Não levantou exceção para categoria inválida)")
    except ValueError as e:
        print("Erro esperado:", e)

    separador("CÁLCULO DE DESCONTO")
    try:
        cupom_valor = Cupom("FIXO30", "VALOR", 30, date.today() + timedelta(days=1), 5, 0)
        cupom_percentual = Cupom("PERC10", "PERCENTUAL", 10, date.today() + timedelta(days=1), 5, 0)
        print("Desconto valor fixo:", cupom_valor.calcular_desconto(100))
        print("Desconto percentual:", cupom_percentual.calcular_desconto(200))
    except Exception as e:
        print("Erro no cálculo de desconto:", e)

    separador("REGISTRO DE USO")
    try:
        cupom_unico = Cupom("UNICO", "VALOR", 20, date.today() + timedelta(days=1), uso_maximo=1, usos_feitos=0)
        cupom_unico.registrar_uso()
        print("Usos feitos:", cupom_unico.usos_feitos)
    except Exception as e:
        print("Erro no primeiro registro de uso:", e)
    try:
        cupom_unico.registrar_uso()
        print("❌ Teste registro de uso - FALHA (Não levantou exceção para limite excedido)")
    except ValueError as e:
        print("Erro esperado:", e)

    separador("PERSISTÊNCIA")
    try:
        cupom_persist = Cupom("SAVE10", "PERCENTUAL", 10, date.today() + timedelta(days=10), 3, 1, ["MODA"])
        dados = cupom_persist.to_dict()
        print("Dict gerado:", dados)
        cupom_recuperado = Cupom.from_dict(dados)
        print("Cupom recuperado:", cupom_recuperado)
        print("Objetos equivalentes?", cupom_persist == cupom_recuperado)
        assert cupom_persist.data_validade == cupom_recuperado.data_validade
        cupom_default_persist = Cupom("SAVEDEFAULT", "VALOR", 5, uso_maximo=2, usos_feitos=0)
        dados_default = cupom_default_persist.to_dict()
        print("Dict gerado para default:", dados_default)
        cupom_recuperado_default = Cupom.from_dict(dados_default)
        print("Cupom recuperado default:", cupom_recuperado_default)
        assert cupom_default_persist.data_validade == cupom_recuperado_default.data_validade
    except Exception as e:
        print("Erro na persistência de cupom:", e)

    separador("EQ / HASH")
    try:
        c1 = Cupom("HASH1", "VALOR", 10, date.today() + timedelta(days=1), 5, 0)
        c2 = Cupom("HASH1", "VALOR", 20, date.today() + timedelta(days=5), 10, 2)
        conjunto = {c1, c2}
        print("Quantidade no set (esperado 1):", len(conjunto))
    except Exception as e:
        print("Erro em EQ/HASH:", e)
    print("=== FIM DOS TESTES DE CUPOM ===")

    # ==================== CLASSE CARRINHO ====================
    print("\n===== TESTANDO CLASSE CARRINHO =====")
    print("Classe Carrinho testada indiretamente pelos testes de Pedido e Frete.")

    # ==================== CLASSE FRETE ====================
    print("\n===== TESTANDO CLASSE FRETE =====")
    print("\n=== TESTE DA CLASSE FRETE ===")
    endereco_frete_ba = Endereco("Salvador", "BA", "40000000")
    endereco_frete_sp = Endereco("São Paulo", "SP", "01000000")
    produto_fisico_frete = ProdutoFisico("Ventilador", "ELETRODOMESTICOS", 150.0, 5, True, 3.0)
    produto_fisico_frete._definir_sku(101)
    produto_digital_frete = ProdutoDigital("Ebook Marketing", "LIVROS", 50.0, 999, True)
    produto_digital_frete._definir_sku(102)
    carrinho_frete_misto = Carrinho()
    carrinho_frete_misto.adicionar_item(ItemCarrinho(produto_fisico_frete, 1))
    carrinho_frete_misto.adicionar_item(ItemCarrinho(produto_digital_frete, 1))
    carrinho_frete_apenas_digital = Carrinho()
    carrinho_frete_apenas_digital.adicionar_item(ItemCarrinho(produto_digital_frete, 2))
    print("Endereços e Produtos de teste criados.")

    print("\n--- Teste 1: Frete para BA com produto físico e digital ---")
    frete_ba = Frete(endereco_frete_ba)
    try:
        resultado_ba = frete_ba.calcular_preview(carrinho_frete_misto, tabela_frete)
        print(f"Endereço: {endereco_frete_ba.cidade}-{endereco_frete_ba.uf}, CEP: {endereco_frete_ba.cep}")
        print(f"Carrinho: {carrinho_frete_misto}")
        print(f"Frete calculado para BA: Valor R$ {resultado_ba['valor']:.2f}, Prazo {resultado_ba['prazo']} dias")
        assert resultado_ba['valor'] == 18
        assert resultado_ba['prazo'] == 5
        print("✅ Teste BA (regra específica) - SUCESSO")
    except Exception as e:
        print(f"❌ Teste BA (regra específica) - ERRO: {e}")

    print("\n--- Teste 2: Frete para SP com produto físico e digital ---")
    frete_sp = Frete(endereco_frete_sp)
    try:
        resultado_sp = frete_sp.calcular_preview(carrinho_frete_misto, tabela_frete)
        print(f"Endereço: {endereco_frete_sp.cidade}-{endereco_frete_sp.uf}, CEP: {endereco_frete_sp.cep}")
        print(f"Carrinho: {carrinho_frete_misto}")
        print(f"Frete calculado para SP: Valor R$ {resultado_sp['valor']:.2f}, Prazo {resultado_sp['prazo']} dias")
        assert resultado_sp['valor'] == 30
        assert resultado_sp['prazo'] == 10
        print("✅ Teste SP (regra default) - SUCESSO")
    except Exception as e:
        print(f"❌ Teste SP (regra default) - ERRO: {e}")

    print("\n--- Teste 3: Frete para carrinho apenas com produtos digitais ---")
    frete_digital = Frete(endereco_frete_ba)
    try:
        resultado_digital = frete_digital.calcular_preview(carrinho_frete_apenas_digital, tabela_frete)
        print(f"Carrinho: {carrinho_frete_apenas_digital}")
        print(f"Frete calculado (apenas digital): Valor R$ {resultado_digital['valor']:.2f}, Prazo {resultado_digital['prazo']} dias")
        assert resultado_digital['valor'] == 0
        assert resultado_digital['prazo'] == 0
        print("✅ Teste produtos digitais - SUCESSO")
    except Exception as e:
        print(f"❌ Teste produtos digitais - ERRO: {e}")

    print("\n--- Teste 4: Inicialização com Endereco inválido ---")
    try:
        Frete("Não é um Endereco")
        print("❌ Teste inicialização inválida - FALHA (Não levantou exceção)")
    except TypeError as e:
        print(f"✅ Teste inicialização inválida - SUCESSO (Erro esperado: {e})")
    print("=== FIM DOS TESTES DA CLASSE FRETE ===")

    # ==================== CLASSE PAGAMENTO ====================
    print("\n===== TESTANDO CLASSE PAGAMENTO =====")
    print("\n=== TESTE DA CLASSE PAGAMENTO ===")
    class MockProduto:
        def __init__(self, sku, nome, preco):
            self.sku = sku
            self.nome = nome
            self.preco = preco
    class MockItemPedido:
        def __init__(self, produto, quantidade):
            self.produto = produto
            self.sku = produto.sku
            self.nome = produto.nome
            self.preco_unitario = produto.preco
            self.quantidade = quantidade
        @property
        def subtotal(self):
            return self.preco_unitario * self.quantidade

    class MockPedido(Pedido):
        def __init__(self, id, total):
            self._id = id
            self._total = total
            self.pagamentos = []
            self.status = StatusPedido.CRIADO
            self.cliente = None
            self.endereco = None
            self.itens = []
            self.frete_valor = 0
            self.desconto = 0
            self.data_criacao = datetime.now()
            self.codigo_rastreio = None
            self.data_entrega = None

        @property
        def id(self):
            return self._id
        @property
        def total(self):
            return self._total
        def registrar_pagamento(self, pagamento):
            self.pagamentos.append(pagamento)
            total_pago = sum(p.valor for p in self.pagamentos if p.status == StatusPagamento.CONFIRMADO)
            if total_pago >= self.total and self.status == StatusPedido.CRIADO:
                self.status = StatusPedido.PAGO

    produto_mock = MockProduto(1, "Produto Teste", 100.0)
    item_mock_pagamento = MockItemPedido(produto_mock, 1)
    pedido_mock_pagamento = MockPedido(id=1, total=100.0)
    print("Pedido mock criado com total de R$ 100.00")

    print("\n--- Teste 1: Inicialização válida ---")
    try:
        pagamento = Pagamento(pedido=pedido_mock_pagamento, valor=100.0, forma=FormaPagamento.PIX)
        print(f"Pagamento inicializado: Valor {pagamento.valor:.2f}, Forma {pagamento.forma.value}, Status {pagamento.status.value}")
        assert pagamento.valor == 100.0
        assert pagamento.forma == FormaPagamento.PIX
        assert pagamento.status == StatusPagamento.PENDENTE
        print("✅ Teste de inicialização válida - SUCESSO")
    except Exception as e:
        print(f"❌ Teste de inicialização válida - ERRO: {e}")

    print("\n--- Teste 2: Inicialização com valor inválido ---")
    try:
        Pagamento(pedido=pedido_mock_pagamento, valor=0, forma=FormaPagamento.CREDITO)
        print("❌ Teste de valor inválido - FALHA (Não levantou exceção)")
    except ValueError as e:
        print(f"✅ Teste de valor inválido - SUCESSO (Erro esperado: {e})")

    print("\n--- Teste 3: Processar pagamento ---")
    pagamento_processar = Pagamento(pedido=pedido_mock_pagamento, valor=50.0, forma=FormaPagamento.DEBITO)
    try:
        pagamento_processar.processar()
        assert pagamento_processar.status == StatusPagamento.CONFIRMADO
        print("✅ Teste de processamento - SUCESSO")
    except Exception as e:
        print(f"❌ Teste de processamento - ERRO: {e}")

    print("\n--- Teste 4: Estornar pagamento ---")
    pagamento_estornar = Pagamento(pedido=pedido_mock_pagamento, valor=75.0, forma=FormaPagamento.CREDITO)
    pagamento_estornar.processar()
    try:
        pagamento_estornar.estornar()
        assert pagamento_estornar.status == StatusPagamento.ESTORNADO
        print("✅ Teste de estorno - SUCESSO")
    except Exception as e:
        print(f"❌ Teste de estorno - ERRO: {e}")

    print("\n--- Teste 5: Cancelar pagamento (apenas PENDENTE) ---")
    pagamento_cancelar = Pagamento(pedido=pedido_mock_pagamento, valor=25.0, forma=FormaPagamento.BOLETO)
    try:
        pagamento_cancelar.cancelar_pagamento()
        assert pagamento_cancelar.status == StatusPagamento.CANCELADO
        print("✅ Teste de cancelamento - SUCESSO")
    except Exception as e:
        print(f"❌ Teste de cancelamento - ERRO: {e}")

    print("\n--- Teste 6: Estorno de pagamento já estornado ---")
    try:
        pagamento_estornar.estornar()
        print("❌ Teste de estorno repetido - FALHA (Não levantou exceção)")
    except ValueError as e:
        print(f"✅ Teste de estorno repetido - SUCESSO (Erro esperado: {e})")

    print("\n--- Teste 7: Cancelamento de pagamento já confirmado ---")
    try:
        pagamento_processar.cancelar_pagamento()
        print("❌ Teste de cancelamento de confirmado - FALHA (Não levantou exceção)")
    except ValueError as e:
        print(f"✅ Teste de cancelamento de confirmado - SUCESSO (Erro esperado: {e})")

    print("\n--- Teste 8: Persistência (to_dict e from_dict) ---")
    pagamento_persist = Pagamento(pedido=pedido_mock_pagamento, valor=150.0, forma=FormaPagamento.PIX, data=datetime(2023, 1, 1, 10, 30))
    pagamento_persist.processar()
    data_dict = pagamento_persist.to_dict()
    print("Dict gerado:", data_dict)
    pagamento_recuperado = Pagamento.from_dict(data_dict, pedido_mock_pagamento)
    print(f"Pagamento recuperado: Valor {pagamento_recuperado.valor:.2f}, Forma {pagamento_recuperado.forma.value}, Status {pagamento_recuperado.status.value}, Data {pagamento_recuperado.data}")
    assert pagamento_recuperado.valor == pagamento_persist.valor
    assert pagamento_recuperado.forma == pagamento_persist.forma
    assert pagamento_recuperado.status == pagamento_persist.status
    assert pagamento_recuperado.data == pagamento_persist.data
    assert pagamento_recuperado.pedido == pedido_mock_pagamento
    print("✅ Teste de persistência - SUCESSO")
    print("=== FIM DOS TESTES DA CLASSE PAGAMENTO ===")

    # ==================== CLASSE PEDIDO E SEUS FLUXOS ====================
    print("\n===== TESTANDO CLASSE PEDIDO E SEUS FLUXOS =====")
    print("=== TESTE PEDIDO E PAGAMENTO ===")
    repo_produtos_pedido = RepositorioProdutos()
    notebook_pedido = ProdutoFisico("Notebook", "ELETRONICOS", 5000.0, 5, True, 2.5)
    mouse_pedido = ProdutoFisico("Mouse", "ELETRONICOS", 200.0, 10, True, 0.5)
    repo_produtos_pedido.adicionar_produto(notebook_pedido)
    repo_produtos_pedido.adicionar_produto(mouse_pedido)
    carrinho_teste_pedido = Carrinho()
    carrinho_teste_pedido.adicionar_item(ItemCarrinho(notebook_pedido, 1))
    carrinho_teste_pedido.adicionar_item(ItemCarrinho(mouse_pedido, 2))
    cliente_teste_pedido = Cliente("Cliente Teste", 11122233344, "cliente.teste@email.com")
    cliente_teste_pedido._definir_id(100)
    endereco_teste_pedido = Endereco("Salvador", "BA", "40000000")
    cliente_teste_pedido.adicionar_endereco(endereco_teste_pedido)
    repo_pedidos_teste_pedido = RepositorioPedidos()
    pedido_fluxo = Pedido(cliente=cliente_teste_pedido, endereco=endereco_teste_pedido, carrinho=carrinho_teste_pedido, frete_valor=50, desconto=100)
    repo_pedidos_teste_pedido.adicionar_pedido(pedido_fluxo)
    print("Itens no pedido:")
    for i in pedido_fluxo.itens:
        print(i)
    print(f"Total produtos: R$ {pedido_fluxo.total_produtos:.2f}")
    print(f"Total com frete e desconto: R$ {pedido_fluxo.total:.2f}")
    pagamento1_fluxo = Pagamento(pedido=pedido_fluxo, valor=2000, forma=FormaPagamento.PIX)
    pagamento1_fluxo.processar()
    pedido_fluxo.registrar_pagamento(pagamento1_fluxo)
    print("Status após pagamento parcial:", pedido_fluxo.status)
    pagamento2_fluxo = Pagamento(pedido=pedido_fluxo, valor=pedido_fluxo.total - 2000, forma=FormaPagamento.CREDITO)
    pagamento2_fluxo.processar()
    pedido_fluxo.registrar_pagamento(pagamento2_fluxo)
    print("Status após pagamento total:", pedido_fluxo.status)
    pedido_fluxo.enviar()
    print("Status após envio:", pedido_fluxo.status)
    pedido_fluxo.entregar()
    print("Status após entrega:", pedido_fluxo.status)
    try:
        pedido_fluxo.cancelar()
    except ValueError as e:
        print("Erro esperado ao cancelar pedido entregue:", e)
    print()

    print("=== TESTE CANCELAMENTO E ESTORNO ===")
    repo_produtos_cancel = RepositorioProdutos()
    produto1_cancel = ProdutoFisico("Teclado", "ELETRONICOS", 300.0, 5, True, 1.0)
    repo_produtos_cancel.adicionar_produto(produto1_cancel)
    carrinho_cancel = Carrinho()
    carrinho_cancel.adicionar_item(ItemCarrinho(produto1_cancel, 2))
    cliente_cancel = Cliente("Cliente Cancelamento", 44455566677, "cancelamento@email.com")
    cliente_cancel._definir_id(101)
    endereco_cancel = Endereco("São Paulo", "SP", "01000000")
    cliente_cancel.adicionar_endereco(endereco_cancel)
    repo_pedidos_cancel = RepositorioPedidos()
    pedido_cancel = Pedido(cliente=cliente_cancel, endereco=endereco_cancel, carrinho=carrinho_cancel, frete_valor=20)
    repo_pedidos_cancel.adicionar_pedido(pedido_cancel)
    print("Estoque antes do pagamento:", produto1_cancel.estoque)
    pagamento_cancel = Pagamento(pedido=pedido_cancel, valor=pedido_cancel.total, forma=FormaPagamento.PIX)
    pagamento_cancel.processar()
    pedido_cancel.registrar_pagamento(pagamento_cancel)
    print("Status após pagamento:", pedido_cancel.status)
    pedido_cancel.cancelar()
    print("Status após cancelamento:", pedido_cancel.status)
    print("Estoque após cancelamento:", produto1_cancel.estoque)
    print("Pagamento estornado?", pagamento_cancel.status == StatusPagamento.ESTORNADO)
    try:
        pagamento_cancel.estornar()
    except ValueError as e:
        print("Erro esperado ao estornar novamente:", e)
    print()

    print("=== TESTE DE EXPEDIÇÃO DO PEDIDO ===")
    repo_produtos_exp = RepositorioProdutos()
    produto_exp1 = ProdutoFisico("Ventilador", "ELETRODOMESTICOS", 150.0, 5, True, 3.0)
    produto_exp2 = ProdutoDigital("Ebook Marketing", "LIVROS", 50.0, 999, True)
    repo_produtos_exp.adicionar_produto(produto_exp1)
    repo_produtos_exp.adicionar_produto(produto_exp2)
    cliente_exp = Cliente("Cliente Expedição", 11111111111, "expedicao@email.com")
    cliente_exp._definir_id(200)
    endereco_exp = Endereco("Rio de Janeiro", "RJ", "20000000")
    cliente_exp.adicionar_endereco(endereco_exp)
    carrinho_exp = Carrinho()
    carrinho_exp.adicionar_item(ItemCarrinho(produto_exp1, 1))
    carrinho_exp.adicionar_item(ItemCarrinho(produto_exp2, 1))
    repo_pedidos_exp = RepositorioPedidos()
    pedido_exp = Pedido(cliente=cliente_exp, endereco=endereco_exp, carrinho=carrinho_exp, frete_valor=25)
    repo_pedidos_exp.adicionar_pedido(pedido_exp)
    print("\nPedido criado:")
    print(pedido_exp.resumo())
    pagamento_exp = Pagamento(pedido=pedido_exp, valor=pedido_exp.total, forma=FormaPagamento.PIX)
    pagamento_exp.processar()
    pedido_exp.registrar_pagamento(pagamento_exp)
    print("\nPedido após pagamento:")
    print(pedido_exp.resumo())
    pedido_exp.enviar()
    print("\nPedido após envio:")
    print(pedido_exp.resumo())
    assert pedido_exp.status == StatusPedido.ENVIADO
    assert pedido_exp.codigo_rastreio is not None and len(pedido_exp.codigo_rastreio) == 13
    print(f"Código de rastreio gerado: {pedido_exp.codigo_rastreio}")
    data_entrega_manual = datetime.now() + timedelta(days=2)
    pedido_exp.entregar(data_entrega=data_entrega_manual)
    print("\nPedido após entrega:")
    print(pedido_exp.resumo())
    assert pedido_exp.status == StatusPedido.ENTREGUE
    assert pedido_exp.data_entrega == data_entrega_manual
    print(f"Data de entrega registrada: {pedido_exp.data_entrega}")
    print("✅ TESTE DE EXPEDIÇÃO CONCLUÍDO COM SUCESSO")
    print("=== FIM DOS TESTES DE PEDIDO E FLUXOS ===")

    print("\n--- TODOS OS TESTES FORAM EXECUTADOS --- ✅")

run_all_tests()