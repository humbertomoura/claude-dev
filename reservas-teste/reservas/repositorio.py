import sqlite3
from datetime import datetime

from reservas.modelos import Reserva


class RepositorioSQLite:
    def __init__(self, caminho: str = ":memory:") -> None:
        self._con = sqlite3.connect(caminho)
        self._con.execute(
            "CREATE TABLE IF NOT EXISTS reservas ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "sala TEXT NOT NULL, inicio TEXT NOT NULL, fim TEXT NOT NULL, "
            "responsavel TEXT NOT NULL)"
        )

    def salvar(self, reserva: Reserva) -> Reserva:
        cur = self._con.execute(
            "INSERT INTO reservas (sala, inicio, fim, responsavel) VALUES (?, ?, ?, ?)",
            (reserva.sala, reserva.inicio.isoformat(), reserva.fim.isoformat(), reserva.responsavel),
        )
        self._con.commit()
        reserva.id = cur.lastrowid
        return reserva

    def listar_por_sala(self, sala: str) -> list[Reserva]:
        linhas = self._con.execute(
            "SELECT id, sala, inicio, fim, responsavel FROM reservas WHERE sala = ? ORDER BY inicio",
            (sala,),
        ).fetchall()
        return [
            Reserva(
                id=i,
                sala=s,
                inicio=datetime.fromisoformat(ini),
                fim=datetime.fromisoformat(fim),
                responsavel=r,
            )
            for i, s, ini, fim, r in linhas
        ]

    def remover(self, id: int) -> bool:
        cur = self._con.execute("DELETE FROM reservas WHERE id = ?", (id,))
        self._con.commit()
        return cur.rowcount > 0
