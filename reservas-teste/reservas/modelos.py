from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reserva:
    sala: str
    inicio: datetime
    fim: datetime
    responsavel: str
    id: int | None = None
