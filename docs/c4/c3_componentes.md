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
    detector[YoloPoseByteTrackDetector]
    yolo[Ultralytics YOLO track]
    tracked[TrackedPerson]
    render[pose_renderer.py]

    preview --> detector
    detector --> yolo
    detector --> tracked
    tracked --> render
    render --> preview
```

Componentes clave:

1. `YoloPoseByteTrackDetector.from_model_path()`: carga modelo y tracker config.
2. `YoloPoseByteTrackDetector.detect()`: filtra `person` y mapea a `TrackedPerson`.
3. `TrackedPerson`: `track_id` + `Detection` + `keypoints` opcionales.
4. `pose_renderer.py`: dibuja bbox, keypoints, skeleton y overlays globales.

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
