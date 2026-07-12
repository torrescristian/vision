# C4 - Código (Funciones y Conexiones)

Este nivel responde: **¿Qué funciones/métodos coordinan el comportamiento real?**

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
    participant Detector as YoloPersonDetector
    participant Model as Ultralytics YOLO

    Preview->>Detector: from_model_path(model, threshold)
    loop por frame
        Preview->>Detector: detect(frame)
        Detector->>Model: infer(frame)
        Model-->>Detector: results.boxes
        Detector-->>Preview: list[PersonDetection]
        Preview->>Preview: draw bbox + confidence + FPS
    end
```

Funciones clave:

1. `run_yolo_person_preview()`
2. `_draw_detection_box()`
3. `_draw_global_overlay()`
4. `YoloPersonDetector.detect()`

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
2. Revisa `detectors/yolo_person.py` para mapeo YOLO -> dominio.
3. Revisa `config.py` para precedencia de configuración.

## Zoom atrás

Volver a [C3 - Componentes](c3_componentes.md) o [README C4](README.md).
