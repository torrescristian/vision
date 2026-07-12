# C4 - Código (Funciones y Conexiones)

Este nivel responde: **¿Qué funciones/métodos coordinan el comportamiento real?**

Si necesitas ver primero el cableado completo de objetos y flujo de frame, revisa antes `c4b_wiring_example.md`.

## C4.1 Flujo de ejecución del pipeline

```mermaid
sequenceDiagram
    participant Main as main.py
    participant Pipe as FramePipeline
    participant Prov as FrameProvider
    participant Proc as FrameProcessor
    participant Rend as FrameRenderer

    Main->>Pipe: run(max_frames)
    Pipe->>Prov: open()
    loop por cada frame
        Prov-->>Pipe: FramePacket
        Pipe->>Proc: process(frame)
        Proc-->>Pipe: processed_frame
        Pipe->>Rend: render(processed_frame)
    end
    Pipe->>Prov: close()
    Pipe->>Rend: close()
```

Métodos clave:

1. `FramePipeline.run()`
2. `FramePipeline._open_resources()`
3. `FramePipeline._close_resources()`
4. `FramePipeline._should_stop()`

## C4.2 Flujo de detección YOLO

```mermaid
sequenceDiagram
    participant Preview as yolo_person_preview
    participant Detector as YoloPoseByteTrackDetector
    participant Model as Ultralytics YOLO.track
    participant Render as pose_renderer

    Preview->>Detector: from_model_path(model, threshold, tracker)
    loop por frame
        Preview->>Detector: detect(frame)
        Detector->>Model: track(frame, persist=True)
        Model-->>Detector: results.boxes + results.keypoints + track_id
        Detector-->>Preview: list[TrackedPerson]
        Preview->>Render: draw_detection_box / draw_pose_keypoints
        Preview->>Render: draw_pose_skeleton (opcional)
        Preview->>Render: draw_global_overlay
    end
```

Funciones clave:

1. `run_yolo_person_preview()`
2. `YoloPoseByteTrackDetector.detect()`
3. `draw_pose_keypoints()`
4. `draw_pose_skeleton()`
5. `draw_global_overlay()`

## C4.3 Flujo de configuración

```mermaid
flowchart TB
    start[Proceso inicia]
    env[Lee variables de entorno]
    parse[Parsers _env_int/_env_float/_env_str]
    load[load_config]
    out[AppConfig listo]
    use[Entrypoints consumen config]

    start --> env --> parse --> load --> out --> use
```

## Detalles on demand

Si quieres profundizar en código:

1. Revisa `services/pipeline/engine.py` para ciclo de vida del pipeline.
2. Revisa `detectors/yolo_pose_bytetrack.py` para mapeo YOLO/ByteTrack -> dominio.
3. Revisa `config.py` para precedencia de configuración.

## Zoom atrás

Volver a [C3 - Componentes](c3_componentes.md) o [README C4](README.md).
