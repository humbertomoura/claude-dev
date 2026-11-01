class ReservaInvalida(ValueError):
    """A reserva viola uma regra de negócio."""


class ConflitoDeHorario(ReservaInvalida):
    """Já existe uma reserva da mesma sala nesse horário."""
