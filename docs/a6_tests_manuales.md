# Hito A.6 - Tests Manuales

## Objetivo

Validar tracking de personas con IDs persistentes entre frames usando YOLO11 Pose + ByteTrack.

## Casos

1. Validar track IDs en inferencia con ByteTrack.

   Comando:

   `uv run pytest -q tests/test_yolo_pose_bytetrack.py::test_pose_bytetrack_detector_returns_tracked_persons`

   Resultado esperado:

   El detector retorna `track_id` y filtra correctamente clase `person`.

2. Ignorar detecciones sin ID de tracking.

   Comando:

   `uv run pytest -q tests/test_yolo_pose_bytetrack.py::test_pose_bytetrack_detector_ignores_boxes_without_track_id`

   Resultado esperado:

   Se descartan cajas sin `box.id` generado por ByteTrack.

3. Validación visual en preview YOLO.

   Comando:

   `uv run vision-yolo --model yolo11n-pose.pt --tracker-config bytetrack.yaml --confidence 0.45`

   Resultado esperado:

   Se ve overlay `Person <id> <confidence>` usando IDs del tracker ByteTrack.

## Criterio de salida

El hito A.6 se considera completo cuando los 3 casos pasan.
