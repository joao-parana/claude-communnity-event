"""Regras de compatibilidade entre uma criança na fila e uma vaga ociosa."""

# Ordem etária dos grupamentos da educação infantil.
GRUPAMENTOS = ("Berçário I", "Berçário Ii", "Maternal I", "Maternal Ii")


def compativel(grupamento: str, grupos_da_vaga: dict[str, int]) -> bool:
    """A vaga só serve se houver saldo no grupamento da idade da criança."""
    return grupos_da_vaga.get(grupamento, 0) > 0


def cobertura(fila: int, vagas: int) -> float:
    """Fração da fila que caberia nas vagas ao alcance. 0..1+"""
    return 0.0 if fila <= 0 else vagas / fila


def faixa_cobertura(c: float) -> str:
    """Classe de leitura: onde realocar resolve, onde falta oferta."""
    if c >= 0.5:
        return "alta"
    if c >= 0.25:
        return "media"
    return "baixa"
