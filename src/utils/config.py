import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # raiz do projeto
SETTINGS_PATH = BASE_DIR / "settings.json"

def carregar_settings():
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_tabela_frete():
    path = Path(__file__).resolve().parent.parent.parent / "settings.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)["frete"]

def default_coupon_validity_days():
    settings = carregar_settings()
    return settings["coupon"]["default_validity_days"]

def obter_top_n_produtos():
    settings = carregar_settings()
    return settings.get("relatorios", {}).get("top_n_produtos", 5)

def obter_janela_cancelamento_horas():
    settings = carregar_settings()
    return settings.get("pedido", {}).get("janela_cancelamento_horas", 24)
