# Hito A.1 - Tests Manuales

## Objetivo

Validar captura de webcam en tiempo real con salida limpia y FPS visible.

## Precondiciones

- Estar en la raiz del proyecto.
- Tener dependencias instaladas con `uv pip install --python .venv/bin/python -e ".[dev]"`.

## Casos

1. Ejecutar preview de webcam.

   Comando:

   `uv run vision-camera --camera-index 0 --width 1280 --height 720`

   Resultado esperado:

   Se abre una ventana con video en tiempo real.

2. Verificar FPS en pantalla.

   Resultado esperado:

   Se muestra un texto `FPS: <valor>` actualizado en cada frame.

3. Verificar salida limpia.

   Accion:

   Presionar `q` o `ESC`.

   Resultado esperado:

   La ventana se cierra y el proceso termina sin traceback.

4. Verificar calidad base del codigo.

   Comandos:

   - `uv run ruff check .`
   - `uv run pyright .`
   - `uv run pytest`

   Resultado esperado:

   Todo en verde.

## Criterio de salida

El hito A.1 se considera completo cuando los 4 casos pasan.
