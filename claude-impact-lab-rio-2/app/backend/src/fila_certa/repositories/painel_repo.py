"""Leitura do dataset pré-agregado.

O painel não lê as bases cruas: elas somam 190 MB e demoram a agregar.
`scripts/build_dataset.py` roda offline e produz o JSON que este módulo carrega
uma vez, no boot. Trocar por consultas ao vivo é trocar a implementação daqui.
"""
import json
from functools import lru_cache

from ..config import DATASET


@lru_cache(maxsize=1)
def dados() -> dict:
    with DATASET.open(encoding="utf-8") as fh:
        return json.load(fh)


def totais() -> dict:
    return dados()["totais"]


def meta() -> dict:
    return dados()["meta"]


def bairros(limite: int = 14) -> list[dict]:
    return dados()["bairros"][:limite]


def cres() -> list[dict]:
    return dados()["cres"]


def focos(cre: int | None = None) -> list[dict]:
    fs = dados()["focos"]
    if cre is not None:
        fs = [f for f in fs if f["cre"] == cre]
    return sorted(fs, key=lambda f: -f["fila"])


def foco(cod: str) -> dict | None:
    return next((f for f in dados()["focos"] if f["cod"] == cod), None)


def vaga(cod: str) -> dict | None:
    return dados()["vagas"].get(cod)
