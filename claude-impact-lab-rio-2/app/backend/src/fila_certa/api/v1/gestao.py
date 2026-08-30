"""API JSON — mesma fonte do painel, para o PWA do responsável consumir."""
from fastapi import APIRouter, HTTPException

from ...repositories import painel_repo, tentativas_repo

router = APIRouter(prefix="/api/v1", tags=["gestao"])


@router.get("/totais")
def totais():
    return {**painel_repo.totais(), "meta": painel_repo.meta()}


@router.get("/cres")
def cres():
    return painel_repo.cres()


@router.get("/bairros")
def bairros(limite: int = 40):
    return painel_repo.bairros(limite)


@router.get("/focos")
def focos(cre: int | None = None):
    return painel_repo.focos(cre)


@router.get("/focos/{cod}")
def foco(cod: str):
    f = painel_repo.foco(cod)
    if f is None:
        raise HTTPException(404, "foco não encontrado")
    vagas = [{**(painel_repo.vaga(z["cod"]) or {}), "cod": z["cod"], "d": z["d"]} for z in f["viz"]]
    return {**f, "vagas": vagas}


@router.get("/convocacoes")
def convocacoes(limite: int = 20):
    return tentativas_repo.convocacoes(limite)
