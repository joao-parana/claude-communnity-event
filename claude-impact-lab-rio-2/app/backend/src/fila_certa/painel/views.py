"""Rotas HTML do painel de gestão (Jinja2 + HTMX)."""
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from ..domain import viabilidade
from ..domain.cascata import CASCATA
from ..repositories import painel_repo
from ..services import realocacao_service

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
# O cache de templates do Jinja2 usa uma tupla com weakref como chave e quebra no
# Python 3.14 ("cannot use 'tuple' as a dict key"). Desligar custa pouco aqui —
# são seis templates pequenos — e evita prender a aplicação a uma versão.
templates.env.cache = None


def _ctx(**extra):
    """Contexto comum a todas as telas: o shell precisa das CREs para a navegação."""
    return {"meta": painel_repo.meta(), "nav_cres": painel_repo.cres(), **extra}


@router.get("/")
def cidade(request: Request):
    """Visão macro: onde na cidade a fila encosta em vaga ociosa."""
    bairros = []
    for b in painel_repo.bairros(14):
        cob = viabilidade.cobertura(b["fila"], b["vagas"])
        bairros.append({**b, "cobertura": round(cob * 100), "faixa": viabilidade.faixa_cobertura(cob)})
    ord_cob = sorted(bairros, key=lambda x: -x["cobertura"])
    return templates.TemplateResponse(request, "cidade.html", _ctx(totais=painel_repo.totais(), bairros=bairros, cres=painel_repo.cres(),
        max_fila=max((b["fila"] for b in bairros), default=1),
        melhores=ord_cob[:3], piores=ord_cob[-3:][::-1],
    ))


@router.get("/cre/{cre}")
def cre(request: Request, cre: int, foco: str | None = None):
    """Visão da CRE: mapa dos focos e as vagas ao alcance de cada um."""
    focos = painel_repo.focos(cre)
    if not focos:
        return templates.TemplateResponse(request, "vazio.html", _ctx(cre=cre), status_code=404)

    sel = next((f for f in focos if f["cod"] == foco), focos[0])
    vagas = []
    for z in sel["viz"]:
        v = painel_repo.vaga(z["cod"])
        if v:
            vagas.append({**v, "cod": z["cod"], "d": z["d"]})

    lats = [f["lat"] for f in focos] + [v["lat"] for v in vagas]
    lons = [f["lon"] for f in focos] + [v["lon"] for v in vagas]
    caixa = {"lat0": min(lats), "lat1": max(lats), "lon0": min(lons), "lon1": max(lons)}

    unicas = {z["cod"] for f in focos for z in f["viz"]}
    vagas_todas = {c: painel_repo.vaga(c) for c in unicas if painel_repo.vaga(c)}
    total_vagas = sum(v["vagas"] for v in vagas_todas.values())
    total_fila = sum(f["fila"] for f in focos)

    return templates.TemplateResponse(request, "cre.html", _ctx(cre=cre, focos=focos[:40], sel=sel, vagas=vagas, caixa=caixa,
        vagas_todas=vagas_todas,
        total_fila=total_fila, total_vagas=total_vagas, n_vagas_un=len(unicas),
        cobertura=round(viabilidade.cobertura(total_fila, total_vagas) * 100),
        max_fila=max((f["fila"] for f in focos), default=1),
    ))


def _tela_realocar(request: Request, origem: str, destino: str, convocacao=None, aluno=None):
    o = painel_repo.foco(origem)
    d = painel_repo.vaga(destino)
    if o is None or d is None:
        return templates.TemplateResponse(request, "vazio.html", _ctx(cre=None), status_code=404)
    dist = next((z["d"] for z in o["viz"] if z["cod"] == destino), None)
    return templates.TemplateResponse(request, "realocar.html", _ctx(
        origem=o, destino={**d, "cod": destino}, dist=dist,
        fila=_fila_exemplo(o), cascata=CASCATA, convocacao=convocacao, aluno=aluno,
    ))


@router.get("/realocar/{origem}/{destino}")
def realocar_form(request: Request, origem: str, destino: str):
    """Tela de realocação: a fila da origem e a vaga de destino."""
    return _tela_realocar(request, origem, destino)


@router.post("/realocar/{origem}/{destino}")
def realocar_enviar(request: Request, origem: str, destino: str,
                    aluno: str = Form(...), grupamento: str = Form(...)):
    """Dispara a convocação e devolve a mesma tela, agora com a trilha registrada.

    Devolver a página inteira (e não um fragmento) mantém um só contrato com o
    `hx-boost` do shell: o htmx extrai `#tela` de qualquer resposta, e o POST
    continua funcionando sem JavaScript.
    """
    r = realocacao_service.ofertar(aluno, origem, destino, grupamento)
    return _tela_realocar(request, origem, destino, convocacao=r, aluno=aluno)


def _fila_exemplo(foco: dict) -> list[dict]:
    """Fila de demonstração.

    A extração é anonimizada e NÃO traz a fila nominal por unidade: `aluno_anon`
    é chave derivada, sem pontuação individual exposta. Estes registros seguem o
    formato real da base para exercitar o fluxo; num sistema vivo viriam da
    classificação publicada.
    """
    base = [
        ("Maternal I", 76, "CadÚnico", "7 meses"),
        ("Maternal I", 76, "CadÚnico", "9 meses"),
        ("Berçário Ii", 55, "Ed. especial", "5 meses"),
        ("Maternal Ii", 53, "CadÚnico", "11 meses"),
        ("Maternal I", 51, "CadÚnico", "4 meses"),
        ("Maternal Ii", 6, "Sem critério", "12 meses"),
    ]
    semente = int(foco["cod"]) if str(foco["cod"]).isdigit() else 0
    return [
        {"pos": i + 1, "aluno": f"aluno_{(semente * 7 + i * 1013) % 900000 + 100000:06d}",
         "grupamento": g, "pontos": p, "tag": t, "espera": e}
        for i, (g, p, t, e) in enumerate(base)
    ]
