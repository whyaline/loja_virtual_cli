# src/seed.py

from src.repositorios.repositorio_produtos import RepositorioProdutos
from src.repositorios.repositorio_clientes import RepositorioClientes
from src.repositorios.repositorio_cupons import RepositorioCupons

from src.modelos.produto import ProdutoFisico, ProdutoDigital
from src.modelos.cliente import Cliente
from src.modelos.cupom import Cupom


def seed():
    #seed_produtos()
    seed_clientes()
    #seed_cupons()


# ======================
# PRODUTOS
# ======================

def seed_produtos():
    repo = RepositorioProdutos()
    repo.carregar_dados()

    if repo.listar_produtos():
        return

    repo.adicionar_produto(
        ProdutoFisico(
            nome="Teclado Mecânico",
            categoria="ELETRONICOS",
            preco=250.0,
            estoque=10,
            ativo=True
        )
    )

    repo.adicionar_produto(
        ProdutoFisico(
            nome="Mouse Gamer",
            categoria="ELETRONICOS",
            preco=150.0,
            estoque=20,
            ativo=True,
            peso = 1.2
        )
    )

    repo.adicionar_produto(
        ProdutoDigital(
            nome="Curso Python",
            categoria="CURSOS",
            preco=99.9,
            ativo=True
        )
    )

    repo.salvar_dados()


# ======================
# CLIENTES
# ======================

def seed_clientes():
    repo = RepositorioClientes()
    repo.carregar_dados()

    if repo.listar_clientes():
        return

    repo.adicionar_cliente(
        Cliente(
            nome="João Silva",
            cpf="12345678901",
            email="joao@email.com"
        )
    )

    repo.adicionar_cliente(
        Cliente(
            nome="Maria Oliveira",
            cpf="98765432100",
            email="maria@email.com"
        )
    )

    repo.salvar_dados()


# ======================
# CUPONS
# ======================

def seed_cupons():
    repo = RepositorioCupons()
    repo.carregar_dados()

    if repo.buscar_por_codigo("DESC10") is None:
        repo.adicionar_cupom(
            Cupom(
                codigo="DESC10",
                tipo="PERCENTUAL",
                valor=10,
                uso_maximo=100
            )
        )

    if repo.buscar_por_codigo("ELETRON20") is None:
        repo.adicionar_cupom(
            Cupom(
                codigo="ELETRON20",
                tipo="VALOR",
                valor=20,
                uso_maximo=50,
                categorias_elegiveis=["ELETRONICOS"]
            )
        )

    repo.salvar_dados()
