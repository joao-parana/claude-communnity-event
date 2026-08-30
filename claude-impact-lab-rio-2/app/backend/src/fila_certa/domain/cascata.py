"""Política de escalonamento da convocação.

A regra oficial da SME: quando a vaga abre, a escola faz no mínimo 1 tentativa
por dia, durante 3 dias consecutivos, em horários diferentes, por telefone,
e-mail, WhatsApp ou SMS. A cascata não substitui isso — automatiza, escalona e
registra, parando assim que a família responde.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Degrau:
    canal: str
    rotulo: str
    quando: str
    ao_vivo: bool  # se pode ser realmente enviado sem credencial de terceiro


CASCATA: tuple[Degrau, ...] = (
    Degrau("push", "Push no app", "imediato", True),
    Degrau("whatsapp", "WhatsApp", "em 4 h sem leitura", False),
    Degrau("sms", "SMS", "dia 2", False),
    Degrau("ligacao", "Ligação da unidade", "dia 3", False),
)

PRAZO_DIAS_UTEIS = 3


def degraus_ate(indice: int) -> tuple[Degrau, ...]:
    """Degraus já disparados quando a cascata parou em `indice`."""
    return CASCATA[: indice + 1]
