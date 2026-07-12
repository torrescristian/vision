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

## Hito A.3 - Configuracion Centralizada

Archivo central: `config.py`

Variables de entorno soportadas:

- `VISION_CAMERA_INDEX`
- `VISION_CAMERA_WIDTH`
- `VISION_CAMERA_HEIGHT`
- `VISION_CAMERA_FPS`
- `VISION_YOLO_MODEL`
- `VISION_YOLO_CONFIDENCE`
- `VISION_YOLO_TRACKER`
- `VISION_YOLO_DRAW_SKELETON`

Ejemplo:

`VISION_YOLO_MODEL=yolo11n-pose.pt VISION_YOLO_CONFIDENCE=0.45 VISION_YOLO_TRACKER=bytetrack.yaml uv run vision-yolo`

## Hito A.4 - Integracion YOLO (person)

Ejecutar deteccion de personas en vivo:

`uv run vision-yolo --camera-index 0 --width 1280 --height 720 --model yolo11n-pose.pt --confidence 0.45 --tracker-config bytetrack.yaml`

Se muestran:

- Bounding boxes
- Track ID
- Keypoints
- Skeleton (opcional con `--draw-skeleton` / `--no-draw-skeleton`)
- Confidence
- FPS

## Modulos principales (actual)

- `detectors/yolo_pose_bytetrack.py`: adaptador de inferencia+tracking con Ultralytics.
- `models/tracked_person.py`: entidad de dominio trackeada.
- `app/pose_renderer.py`: render modular de bbox, keypoints, skeleton y overlays.
- `app/yolo_person_preview.py`: composition root del preview en vivo.
