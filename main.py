import sys
from src.cli.dispatcher import dispatch
from src.dados.seed import executar_seed

def main():
    executar_seed()
    dispatch(sys.argv)

if __name__ == "__main__":
    main()
