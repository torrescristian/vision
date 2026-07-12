# Vision Engine

Base del proyecto para deteccion de caidas usando vision por computadora.

## Requisitos

- Python 3.12+
- uv

## Setup

1. Crear entorno virtual:

   uv venv

2. Instalar dependencias (app + dev):

   uv pip install --python .venv/bin/python -e ".[dev]"

## Comandos utiles

- Lint: `uv run ruff check .`
- Typecheck: `uv run pyright .`
- Tests: `uv run pytest`

## Hito A.1 - Captura de Camara

Ejecutar preview de webcam con FPS:

`uv run vision-camera --camera-index 0 --width 1280 --height 720`

Salir con `q` o `ESC`.
