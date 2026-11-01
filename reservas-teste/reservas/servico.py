from datetime import datetime, time, timedelta
from typing import Callable

from reservas.erros import ConflitoDeHorario, ReservaInvalida
from reservas.modelos import Reserva
from reservas.repositorio import RepositorioSQLite

DURACAO_MAXIMA = timedelta(hours=3)
ABERTURA = time(8, 0)
FECHAMENTO = time(20, 0)


class ServicoReservas:
    def __init__(self, repositorio: RepositorioSQLite, agora: Callable[[], datetime]) -> None:
        self._repo = repositorio
        self._agora = agora

    def reservar(self, sala: str, inicio: datetime, fim: datetime, responsavel: str) -> Reserva:
        if fim <= inicio:
            raise ReservaInvalida("O fim deve ser depois do início")
        if fim - inicio > DURACAO_MAXIMA:
            raise ReservaInvalida("A reserva excede a duração máxima")
        if inicio.time() < ABERTURA or fim.time() > FECHAMENTO or inicio.date() != fim.date():
            raise ReservaInvalida("Fora do horário de funcionamento")
        if inicio < self._agora():
            raise ReservaInvalida("Não é possível reservar no passado")
        for existente in self._repo.listar_por_sala(sala):
            if inicio <= existente.fim and fim >= existente.inicio:
                raise ConflitoDeHorario(f"A sala {sala} já está reservada nesse horário")
        return self._repo.salvar(Reserva(sala, inicio, fim, responsavel))

    def cancelar(self, id: int) -> None:
        if not self._repo.remover(id):
            raise ReservaInvalida(f"Reserva {id} não encontrada")

    def reservas_da_sala(self, sala: str) -> list[Reserva]:
        return self._repo.listar_por_sala(sala)
