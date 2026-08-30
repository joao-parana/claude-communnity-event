"""Fila Certa — painel de gestão da Inscrição Creche (SME-Rio).

Um processo serve as três coisas: o painel HTML dos gestores, a API JSON e
(quando existir) os estáticos do PWA do responsável. O registro de tentativas é
compartilhado — o painel escreve, o app lê.
"""
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.v1 import gestao
from .config import TITULO
from .painel import views
from .repositories import tentativas_repo

app = FastAPI(title=TITULO, docs_url="/api/docs", redoc_url=None)


@app.on_event("startup")
def iniciar() -> None:
    tentativas_repo.iniciar()


app.include_router(gestao.router)
app.include_router(views.router)

_static = Path(__file__).parent / "painel" / "static"
if _static.is_dir():
    app.mount("/static", StaticFiles(directory=str(_static)), name="static")

# O PWA entra aqui quando for construído (vite build -> app/frontend/dist).
_pwa = os.getenv("FILA_CERTA_STATIC_DIR")
if _pwa and Path(_pwa).is_dir():
    app.mount("/app", StaticFiles(directory=_pwa, html=True), name="pwa")
