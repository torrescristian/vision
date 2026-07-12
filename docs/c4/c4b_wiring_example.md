# C4b - Wiring End-to-End

Este documento conecta C3 y C4 en un solo recorrido: como se conectan objetos y como viaja un frame hasta pantalla.

## Wiring de objetos (runtime)

```mermaid
flowchart LR
    cfg[load_config]
    cv[load_cv2]
    cap[open_capture]
    det[YoloPersonDetector.from_model_path]
    loop[while True]
    draw[_draw_detection_box + _draw_global_overlay]
    out[cv2.imshow]

    cfg --> det
    cfg --> cap
    cv --> cap
    cap --> loop
    det --> loop
    loop --> draw --> out
```

## Secuencia de un frame

```mermaid
sequenceDiagram
    participant App as yolo_person_preview
    participant Cam as cv2.VideoCapture
    participant Det as YoloPersonDetector
    participant Y as Ultralytics YOLO

    App->>Cam: read()
    Cam-->>App: frame
    App->>Det: detect(frame)
    Det->>Y: model(frame)
    Y-->>Det: results.boxes
    Det-->>App: list[PersonDetection]
    App->>App: draw boxes + confidence + fps
    App->>App: imshow(window, frame)
```

## Donde mirar en codigo

1. Setup y loop principal: `app/yolo_person_preview.py`
2. Parseo/filtro YOLO: `detectors/yolo_person.py`
3. Configuracion de defaults/env: `config.py`

## Relacion con C4 principal

Si quieres detalle por metodos, continua en `c4_codigo.md`.
