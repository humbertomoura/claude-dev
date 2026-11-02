# reservas-teste

Serviço de reservas de salas, em Python 3 sem framework (SQLite e pytest).

## Comandos
- Testes: `python -m pytest -q` (use o python do .venv; o pytest solto falha fora dele).

## Estrutura
- `reservas/servico.py`: regras de negócio (ServicoReservas).
- `reservas/repositorio.py`: acesso ao SQLite.
- `reservas/erros.py`: ReservaInvalida e ConflitoDeHorario.
- `tests/`: testes com pytest.

## Convenções
- Os testes fixam a data. Use o relógio injetado (parâmetro `agora` do serviço), nunca `datetime.now()`.
- Teste novo usa a fixture `servico` e o helper `em` de tests/test_servico.py.
- Mensagens de erro em português.
- Toda regra de negócio nova ou alterada entra na lista "Regras de negócio" do README.md, na mesma tarefa.

## Proibições
- Não altere testes existentes sem pedir.
- Não faça commit: deixe o diff para revisão.