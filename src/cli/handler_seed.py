# src/cli/handler_seed.py
from src.dados.seed import seed

def handle_seed():
    seed()
    print("Dados iniciais carregados com sucesso!")
