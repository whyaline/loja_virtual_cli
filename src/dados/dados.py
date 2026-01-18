from pathlib import Path
import json

ARQUIVOS = {
    "clientes": Path("data/clientes.json"),
    "produtos": Path("data/produtos.json"),
    "pedidos": Path("data/pedidos.json"),
    "cupons": Path("data/cupons.json")
}

def salvar_lista(nome, lista_dict):
    caminho = ARQUIVOS[nome]
    caminho.parent.mkdir(exist_ok=True)  # garante que a pasta existe
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(lista_dict, f, indent=2, ensure_ascii=False)

def carregar_lista(nome):
    caminho = ARQUIVOS[nome]
    if not caminho.exists() or caminho.stat().st_size == 0:
        # arquivo não existe ou está vazio → retorna estrutura vazia
        if nome == "clientes":
            return {"proximo_id": 1, "clientes": []}
        elif nome == "produtos":
            return {"proximo_sku": 1, "produtos": []}
        elif nome == "pedidos":
            return {"proximo_id": 1, "pedidos": []}
        elif nome == "cupons":
            return []
        else:
            return {}
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Aviso: arquivo {caminho} está corrompido ou vazio. Retornando repositório vazio.")
        return {}
