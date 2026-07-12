# Vision Engine

Base del proyecto para deteccion de caidas usando vision por computadora.

## Requisitos

- Python 3.12+
- uv

## Setup

1. Crear entorno virtual:

   uv venv

2. Activar entorno:

   source .venv/bin/activate

3. Instalar dependencias de desarrollo:

   uv pip install -e ".[dev]"

4. Ejecutar validaciones:

   ruff check .
   pyright .
   pytest
