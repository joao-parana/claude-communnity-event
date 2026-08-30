"""Configuração por ambiente. Nada de credencial em código."""
import os
from pathlib import Path

RAIZ = Path(__file__).parent
DATASET = Path(os.getenv("FILA_CERTA_DATASET", RAIZ / "data" / "painel.json"))
DB_PATH = Path(os.getenv("FILA_CERTA_DB_PATH", "/tmp/fila_certa.db"))
TITULO = "Inscrição Creche — Painel de Descompasso"
