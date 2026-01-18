# main.py

from src.cli.menu_principal import menu_principal
from src.dados.seed import seed

if __name__ == "__main__":
    seed()
    menu_principal()
