import json
from pathlib import Path

BASE_DIR = Path("data")
BASE_DIR.mkdir(exist_ok=True)

ARQUIVOS = {
    "produtos": BASE_DIR / "produtos.json",
    "clientes": BASE_DIR / "clientes.json",
    "pedidos": BASE_DIR / "pedidos.json",
    "cupons": BASE_DIR / "cupons.json",
}

def salvar_lista(nome, lista_dict):
    caminho = ARQUIVOS[nome]
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(lista_dict, f, indent=2, ensure_ascii=False)


def carregar_lista(nome):
    caminho = ARQUIVOS[nome]
    if not caminho.exists():
        return []

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
