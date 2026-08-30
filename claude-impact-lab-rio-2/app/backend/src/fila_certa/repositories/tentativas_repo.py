"""Registro de tentativas de contato — a tabela que hoje não existe.

Canal, horário, entrega e resposta por convocação. É o que permite distinguir
falha de contato de recusa real, e o que prova o cumprimento do prazo de 3 dias
perante os órgãos que auditam a fila.
"""
import sqlite3
from datetime import datetime, timezone

from ..config import DB_PATH

ESQUEMA = """
CREATE TABLE IF NOT EXISTS convocacao (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  aluno_anon    TEXT    NOT NULL,
  origem_cod    TEXT    NOT NULL,
  destino_cod   TEXT    NOT NULL,
  grupamento    TEXT,
  criada_em     TEXT    NOT NULL,
  prazo_ate     TEXT    NOT NULL,
  situacao      TEXT    NOT NULL DEFAULT 'aguardando'
);
CREATE TABLE IF NOT EXISTS tentativa (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  convocacao_id INTEGER NOT NULL REFERENCES convocacao(id),
  canal         TEXT    NOT NULL,
  enviada_em    TEXT    NOT NULL,
  entrega       TEXT    NOT NULL,
  respondida_em TEXT
);
CREATE INDEX IF NOT EXISTS ix_tentativa_conv ON tentativa(convocacao_id);
"""


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def iniciar() -> None:
    with _conn() as c:
        c.executescript(ESQUEMA)


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def criar_convocacao(aluno: str, origem: str, destino: str, grupamento: str, prazo: str) -> int:
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO convocacao (aluno_anon, origem_cod, destino_cod, grupamento, criada_em, prazo_ate)"
            " VALUES (?,?,?,?,?,?)",
            (aluno, origem, destino, grupamento, _agora(), prazo),
        )
        return int(cur.lastrowid)


def registrar_tentativa(convocacao_id: int, canal: str, entrega: str) -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO tentativa (convocacao_id, canal, enviada_em, entrega) VALUES (?,?,?,?)",
            (convocacao_id, canal, _agora(), entrega),
        )


def convocacoes(limite: int = 20) -> list[dict]:
    with _conn() as c:
        linhas = c.execute(
            "SELECT c.*, ("
            "  SELECT group_concat(t.canal || '|' || t.entrega, ';')"
            "  FROM tentativa t WHERE t.convocacao_id = c.id ORDER BY t.id"
            ") AS trilha FROM convocacao c ORDER BY c.id DESC LIMIT ?",
            (limite,),
        ).fetchall()
    return [dict(l) for l in linhas]
