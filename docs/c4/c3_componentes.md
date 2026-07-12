# C3 - Componentes

Este nivel responde: **¿Qué módulos/clases componen cada contenedor y cómo se conectan?**

## C3.1 Pipeline

```mermaid
flowchart LR
    fp[FrameProvider Protocol]
    pr[FrameProcessor Protocol]
    rr[FrameRenderer Protocol]
    eng[FramePipeline]
    packet[FramePacket]

    fp --> eng
    eng --> pr
    pr --> eng
    eng --> rr
    packet --> fp
    packet --> pr
    packet --> rr
```

Componentes clave:

1. `FrameProvider`: fuente de frames (mock/webcam/RTSP futuro).
2. `FrameProcessor`: transforma frame de entrada en salida.
3. `FrameRenderer`: presenta o persiste resultados.
4. `FramePipeline`: orquesta el ciclo de ejecución.

## C3.2 Detección YOLO

```mermaid
flowchart TB
    preview[yolo_person_preview.py]
    detector[YoloPersonDetector]
    yolo[Ultralytics YOLO]
    person[PersonDetection]

    preview --> detector
    detector --> yolo
    detector --> person
    person --> preview
```

Componentes clave:

1. `YoloPersonDetector.from_model_path()`: carga pesos/modelo.
2. `YoloPersonDetector.detect()`: filtra clase `person` + threshold.
3. `PersonDetection`: bounding box + confidence.

## C3.3 Configuración

```mermaid
flowchart LR
    env[Variables de Entorno]
    cfg[load_config]
    cam[CameraConfig]
    yolo[YoloConfig]
    app[Entrypoints App]

    env --> cfg
    cfg --> cam
    cfg --> yolo
    cam --> app
    yolo --> app
```

## Zoom siguiente

Ir a [C4 - Código](c4_codigo.md).
