# Quickstart para Devs de TypeScript

Este documento explica el proyecto completo de forma simple, pensado para alguien que viene de JS/TS.

## 1. Mapa mental rapido: TS vs Python en este repo

- `package.json` -> `pyproject.toml`
- `npm run <cmd>` -> `uv run <cmd>`
- `interface` (TS) -> `Protocol` (Python)
- `type/DTO` -> `dataclass`
- Composition root (backend TS) -> `build_demo_pipeline()` en `main.py`

## 2. Que hace este proyecto hoy

1. Captura video de webcam.
2. Puede correr preview simple con FPS.
3. Puede correr YOLO y detectar personas.
4. Tiene pipeline desacoplado (provider -> processor -> renderer) listo para crecer.

## 3. Estructura explicada por carpetas

- `app/`: entrypoints ejecutables (preview de camara y preview YOLO).
- `config.py`: configuracion central por defaults + variables de entorno.
- `detectors/`: adaptadores de deteccion (YOLO).
- `models/`: enums y modelos de dominio/base.
- `services/pipeline/`: contratos y orquestacion desacoplada.
- `tests/`: pruebas unitarias de config, pipeline, detector y preview.
- `docs/`: roadmap, manuales por hito y C4.

## 4. Entrypoints que importan

En `pyproject.toml` hay tres scripts:

1. `vision-engine`: demo del pipeline desacoplado.
2. `vision-camera`: webcam + FPS.
3. `vision-yolo`: webcam + deteccion YOLO de personas.

## 5. Flujo de control (de frame a pantalla)

### A) Preview de camara

1. Se carga config (`load_config`).
2. Se abre camara (`open_capture`).
3. Loop: `read` -> `compute_fps` -> dibujar overlay -> `imshow`.
4. Cierre limpio de recursos (`release` + `destroyAllWindows`).

### B) Preview YOLO

1. Se carga modelo (`YoloPersonDetector.from_model_path`).
2. Loop: `read` -> `detect` -> dibujar boxes -> overlay global -> `imshow`.
3. El detector parsea salida cruda de Ultralytics y filtra clase persona.

## 6. Configuracion central (A.3)

`config.py` concentra defaults y lectura por env vars:

- `VISION_CAMERA_INDEX`
- `VISION_CAMERA_WIDTH`
- `VISION_CAMERA_HEIGHT`
- `VISION_CAMERA_FPS`
- `VISION_YOLO_MODEL`
- `VISION_YOLO_CONFIDENCE`

## 7. Comandos base

Instalacion:

```bash
uv venv
uv pip install --python .venv/bin/python -e ".[dev]"
```

Calidad:

```bash
uv run ruff check .
uv run pyright .
uv run pytest
```

Ejecucion:

```bash
uv run vision-camera
uv run vision-yolo --model yolov8n.pt --confidence 0.45
uv run vision-yolo --camera-index 0 --width 1280 --height 720 --model yolov8n.pt --confidence 0.45
```

## 8. Donde profundizar con zoom

Recorrido recomendado:

1. `docs/c4/c1_contexto.md`
2. `docs/c4/c2_contenedores.md`
3. `docs/c4/c3_componentes.md`
4. `docs/c4/c4b_wiring_example.md`
5. `docs/c4/c4_codigo.md`

## 9. Regla para no perderse

Cuando dudes, ubica primero:

1. Quien crea las dependencias (composition root).
2. Quien corre el loop principal.
3. Donde se abre/cierra recursos.
4. Donde se transforma data cruda a estructura propia.
