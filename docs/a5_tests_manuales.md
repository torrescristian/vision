# Hito A.5 - Tests Manuales

## Objetivo

Validar que existe un modelo de detección de dominio desacoplado de Ultralytics.

## Casos

1. Verificar modelos de dominio.

   Comando:

   `uv run pytest -q tests/test_detection_models.py`

   Resultado esperado:

   Tests verdes para `BoundingBox`, `Detection` y `Person`.

2. Verificar desacople del detector.

   Comando:

   `uv run pytest -q tests/test_yolo_person_detector.py`

   Resultado esperado:

   El detector retorna `Detection` de dominio, no estructuras crudas de Ultralytics.

## Criterio de salida

El hito A.5 se considera completo cuando ambos casos pasan.
