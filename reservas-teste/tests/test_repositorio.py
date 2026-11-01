from datetime import datetime

from reservas.modelos import Reserva
from reservas.repositorio import RepositorioSQLite


def test_salva_e_lista_por_sala():
    repo = RepositorioSQLite()
    repo.salvar(Reserva("A1", datetime(2026, 11, 3, 9), datetime(2026, 11, 3, 10), "ana"))
    repo.salvar(Reserva("B2", datetime(2026, 11, 3, 9), datetime(2026, 11, 3, 10), "bia"))
    assert [r.responsavel for r in repo.listar_por_sala("A1")] == ["ana"]


def test_remover_devolve_false_quando_nao_existe():
    assert RepositorioSQLite().remover(1) is False
