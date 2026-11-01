# reservas-teste

Serviço de reservas de salas de reunião. Repositório de estudo do livro
*Claude Code para devs seniores*.

## Regras de negócio

- Uma reserva tem sala, início, fim e responsável.
- A duração máxima de uma reserva é de **4 horas**.
- As salas funcionam das 08:00 às 20:00.
- Não se reserva no passado.
- Duas reservas da mesma sala não podem se sobrepor. Uma reserva pode
  começar exatamente quando a anterior termina.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Estrutura

- `reservas/modelos.py`: a classe `Reserva`.
- `reservas/repositorio.py`: persistência em SQLite.
- `reservas/servico.py`: as regras de negócio.
- `reservas/erros.py`: exceções do domínio.
- `tests/`: testes unitários.
