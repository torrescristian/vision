"""Pruebas basicas del entrypoint."""

from main import main


def test_main_runs_without_error() -> None:
    """Verifica que el entrypoint se ejecute sin excepciones."""
    main()
