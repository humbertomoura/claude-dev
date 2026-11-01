from datetime import datetime

import pytest

from reservas.erros import ConflitoDeHorario, ReservaInvalida
from reservas.repositorio import RepositorioSQLite
from reservas.servico import ServicoReservas

HOJE = datetime(2026, 11, 2, 7, 0)


def em(dia: int, hora: int, minuto: int = 0) -> datetime:
    return datetime(2026, 11, dia, hora, minuto)


@pytest.fixture
def servico() -> ServicoReservas:
    return ServicoReservas(RepositorioSQLite(), agora=lambda: HOJE)


def test_reserva_simples_recebe_id(servico):
    r = servico.reservar("A1", em(3, 9), em(3, 10), "ana")
    assert r.id is not None


def test_rejeita_fim_antes_do_inicio(servico):
    with pytest.raises(ReservaInvalida):
        servico.reservar("A1", em(3, 10), em(3, 9), "ana")


def test_aceita_tres_horas(servico):
    servico.reservar("A1", em(3, 9), em(3, 12), "ana")


def test_rejeita_mais_de_tres_horas(servico):
    with pytest.raises(ReservaInvalida):
        servico.reservar("A1", em(3, 9), em(3, 12, 1), "ana")


def test_rejeita_antes_da_abertura(servico):
    with pytest.raises(ReservaInvalida):
        servico.reservar("A1", em(3, 7), em(3, 8), "ana")


def test_rejeita_depois_do_fechamento(servico):
    with pytest.raises(ReservaInvalida):
        servico.reservar("A1", em(3, 19), em(3, 21), "ana")


def test_rejeita_reserva_no_passado(servico):
    with pytest.raises(ReservaInvalida):
        servico.reservar("A1", em(1, 9), em(1, 10), "ana")


def test_rejeita_sobreposicao_na_mesma_sala(servico):
    servico.reservar("A1", em(3, 10), em(3, 12), "ana")
    with pytest.raises(ConflitoDeHorario):
        servico.reservar("A1", em(3, 11), em(3, 13), "bia")


def test_aceita_mesmo_horario_em_salas_diferentes(servico):
    servico.reservar("A1", em(3, 10), em(3, 12), "ana")
    servico.reservar("B2", em(3, 10), em(3, 12), "bia")


def test_aceita_mesmo_horario_em_dias_diferentes(servico):
    servico.reservar("A1", em(3, 10), em(3, 12), "ana")
    servico.reservar("A1", em(4, 10), em(4, 12), "bia")


def test_cancelar_libera_o_horario(servico):
    r = servico.reservar("A1", em(3, 10), em(3, 12), "ana")
    servico.cancelar(r.id)
    servico.reservar("A1", em(3, 10), em(3, 12), "bia")


def test_cancelar_reserva_inexistente_falha(servico):
    with pytest.raises(ReservaInvalida):
        servico.cancelar(999)
