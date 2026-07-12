# Hito A.3 - Tests Manuales

## Objetivo

Validar que la configuracion centralizada en `config.py` controla camara y YOLO.

## Casos

1. Verificar valores por defecto.

   Comando:

   `uv run python -c "from config import load_config; print(load_config())"`

   Resultado esperado:

   Se imprime `camera` y `yolo` con valores default.

2. Verificar override por variables de entorno.

   Comando:

   `VISION_CAMERA_WIDTH=960 VISION_CAMERA_HEIGHT=540 uv run python -c "from config import load_config; c=load_config(); print(c.camera.width, c.camera.height)"`

   Resultado esperado:

   Imprime `960 540`.

3. Verificar que runner de camara usa config central.

   Comando:

   `VISION_CAMERA_WIDTH=960 VISION_CAMERA_HEIGHT=540 uv run vision-camera`

   Resultado esperado:

   Inicia captura en 960x540 (log inicial del runner).

## Criterio de salida

El hito A.3 se considera completo cuando los 3 casos pasan.
