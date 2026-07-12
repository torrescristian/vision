# Hito A.2 - Tests Manuales

## Objetivo

Validar el pipeline desacoplado `FrameProvider -> FrameProcessor -> Renderer`.

## Casos

1. Ejecutar corrida base del pipeline.

   Comando:

   uv run python main.py

   Resultado esperado:

   La consola muestra `pipeline A.2 OK` con cantidad de frames procesados.

2. Ejecutar tests automatizados del pipeline.

   Comando:

   uv run pytest

   Resultado esperado:

   Todos los tests pasan, incluyendo los de `tests/test_pipeline.py`.

3. Validar que arquitectura sigue desacoplada.

   Revision manual:

   - `FrameProvider`, `FrameProcessor` y `FrameRenderer` estan definidos como contratos.
   - `FramePipeline` no depende de OpenCV ni de una fuente concreta.
   - El proveedor puede reemplazarse por uno RTSP en futuros hitos.

## Criterio de salida

El hito se considera completo cuando los 3 casos anteriores pasan correctamente.
