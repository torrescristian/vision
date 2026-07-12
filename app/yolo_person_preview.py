"""Preview en vivo con YOLO para deteccion de personas (Hito A.4)."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from app.camera_preview import (
    CameraPreviewConfig,
    compute_fps,
    ensure_graphical_session,
    initialize_window,
    load_cv2,
    open_capture,
    print_startup_message,
)
from config import load_config
from detectors.yolo_person import PersonDetection, YoloPersonDetector

EXIT_KEYS = (ord("q"), 27)


@dataclass(frozen=True, slots=True)
class YoloPreviewConfig:
    camera_index: int
    width: int
    height: int
    model_path: str
    confidence_threshold: float
    window_name: str = "Vision Engine - YOLO Person"


def _draw_detection_box(cv2: Any, frame: Any, detection: PersonDetection) -> None:
    cv2.rectangle(
        img=frame,
        pt1=(detection.x1, detection.y1),
        pt2=(detection.x2, detection.y2),
        color=(255, 0, 0),
        thickness=2,
    )
    cv2.putText(
        img=frame,
        text=f"person {detection.confidence:.2f}",
        org=(detection.x1, max(detection.y1 - 8, 20)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.65,
        color=(0, 200, 255),
        thickness=2,
        lineType=cv2.LINE_AA,
    )


def _draw_global_overlay(cv2: Any, frame: Any, fps: float, people_count: int) -> None:
    cv2.putText(
        img=frame,
        text=f"FPS: {fps:.1f}  Persons: {people_count}",
        org=(12, 30),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.85,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA,
    )


def run_yolo_person_preview(config: YoloPreviewConfig, *, cv2_module: Any | None = None) -> None:
    cv2 = load_cv2(cv2_module)
    detector = YoloPersonDetector.from_model_path(
        model_path=config.model_path,
        confidence_threshold=config.confidence_threshold,
    )

    camera_config = CameraPreviewConfig(
        camera_index=config.camera_index,
        width=config.width,
        height=config.height,
        window_name=config.window_name,
    )
    capture = open_capture(cv2, config=camera_config)
    initialize_window(cv2, config.window_name)
    print_startup_message(camera_config)

    import time

    last_tick = time.perf_counter()
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                raise RuntimeError("No se pudo leer un frame desde la webcam")

            detections = detector.detect(frame)

            for detection in detections:
                _draw_detection_box(cv2, frame, detection)

            current_tick = time.perf_counter()
            fps = compute_fps(last_tick, current_tick)
            last_tick = current_tick
            _draw_global_overlay(cv2, frame, fps=fps, people_count=len(detections))

            cv2.imshow(config.window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in EXIT_KEYS:
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()


def _build_parser() -> argparse.ArgumentParser:
    app_config = load_config()

    parser = argparse.ArgumentParser(description="Preview YOLO: deteccion de personas en vivo")
    parser.add_argument("--camera-index", type=int, default=app_config.camera.index)
    parser.add_argument("--width", type=int, default=app_config.camera.width)
    parser.add_argument("--height", type=int, default=app_config.camera.height)
    parser.add_argument("--model", type=str, default=app_config.yolo.model_path)
    parser.add_argument(
        "--confidence",
        type=float,
        default=app_config.yolo.person_confidence_threshold,
        help="Threshold minimo para aceptar detecciones de persona",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    ensure_graphical_session()

    parser = _build_parser()
    args = parser.parse_args(argv)
    run_yolo_person_preview(
        YoloPreviewConfig(
            camera_index=args.camera_index,
            width=args.width,
            height=args.height,
            model_path=args.model,
            confidence_threshold=args.confidence,
        )
    )


if __name__ == "__main__":
    main()
