"""Orquestra a oferta de uma vaga ociosa a uma criança da fila."""
from datetime import date, timedelta

from ..domain.cascata import CASCATA, PRAZO_DIAS_UTEIS
from ..repositories import painel_repo, tentativas_repo


def _prazo(dias_uteis: int = PRAZO_DIAS_UTEIS) -> date:
    d = date.today()
    restantes = dias_uteis
    while restantes:
        d += timedelta(days=1)
        if d.weekday() < 5:
            restantes -= 1
    return d


def ofertar(aluno: str, origem_cod: str, destino_cod: str, grupamento: str) -> dict:
    """Cria a convocação e dispara o primeiro degrau da cascata.

    Só o push é enviado de fato; os demais canais ficam registrados como
    pendentes até que haja credencial de provedor. O registro é o entregável:
    é ele que distingue falha de contato de recusa real.
    """
    destino = painel_repo.vaga(destino_cod)
    if destino is None:
        raise ValueError(f"unidade de destino desconhecida: {destino_cod}")

    prazo = _prazo()
    conv_id = tentativas_repo.criar_convocacao(
        aluno=aluno, origem=origem_cod, destino=destino_cod,
        grupamento=grupamento, prazo=prazo.isoformat(),
    )
    for degrau in CASCATA:
        entrega = "enviado" if degrau.ao_vivo else "pendente"
        tentativas_repo.registrar_tentativa(conv_id, degrau.canal, entrega)

    return {
        "id": conv_id,
        "destino": destino,
        "prazo": prazo.isoformat(),
        "degraus": [d.canal for d in CASCATA],
    }
