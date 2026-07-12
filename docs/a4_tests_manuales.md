# Hito A.4 - Tests Manuales

## Objetivo

Validar deteccion de personas con YOLO sobre webcam en tiempo real.

## Casos

1. Ejecutar preview YOLO.

   Comando:

   `uv run vision-yolo --camera-index 0 --width 1280 --height 720 --model yolov8n.pt --confidence 0.45`

   Resultado esperado:

   Se abre ventana de video con inferencia activa.

2. Verificar filtro `person`.

   Accion:

   Mostrar una persona frente a la camara.

   Resultado esperado:

   Aparece bounding box con label `person` y confidence.

3. Verificar overlay global.

   Resultado esperado:

   Se muestra `FPS` y contador `Persons`.

4. Verificar salida limpia.

   Accion:

   Presionar `q` o `ESC`.

   Resultado esperado:

   La ventana se cierra sin traceback.

## Criterio de salida

El hito A.4 se considera completo cuando los 4 casos pasan.
