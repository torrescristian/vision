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
from app.pose_renderer import (
    draw_detection_box,
    draw_global_overlay,
    draw_pose_keypoints,
    draw_pose_skeleton,
)
from config import load_config
from detectors.yolo_pose_bytetrack import YoloPoseByteTrackDetector

EXIT_KEYS = (ord("q"), 27)


@dataclass(frozen=True, slots=True)
class YoloPreviewConfig:
    camera_index: int
    width: int
    height: int
    model_path: str
    confidence_threshold: float
    tracker_config: str = "bytetrack.yaml"
    draw_skeleton: bool = True
    window_name: str = "Vision Engine - YOLO Person"


def run_yolo_person_preview(config: YoloPreviewConfig, *, cv2_module: Any | None = None) -> None:
    # Fase 1: wiring de dependencias e inicializacion de recursos.
    cv2 = load_cv2(cv2_module)
    detector = YoloPoseByteTrackDetector.from_model_path(
        model_path=config.model_path,
        confidence_threshold=config.confidence_threshold,
        tracker_config=config.tracker_config,
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
        # Fase 2: loop principal de runtime (capture -> detect -> draw -> show).
        while True:
            ok, frame = capture.read()
            if not ok:
                raise RuntimeError("No se pudo leer un frame desde la webcam")

            tracked_people = detector.detect(frame)

            for tracked in tracked_people:
                draw_detection_box(cv2, frame, tracked)
                draw_pose_keypoints(cv2, frame, tracked)
                if config.draw_skeleton:
                    draw_pose_skeleton(cv2, frame, tracked)

            current_tick = time.perf_counter()
            fps = compute_fps(last_tick, current_tick)
            last_tick = current_tick
            draw_global_overlay(cv2, frame, fps=fps, people_count=len(tracked_people))

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
    parser.add_argument(
        "--tracker-config",
        type=str,
        default=app_config.yolo.tracker_config,
        help="Archivo de tracker Ultralytics (ej: bytetrack.yaml)",
    )
    parser.add_argument(
        "--draw-skeleton",
        action=argparse.BooleanOptionalAction,
        default=app_config.yolo.draw_skeleton,
        help="Dibuja lineas del esqueleto COCO encima de los keypoints",
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
            tracker_config=args.tracker_config,
            draw_skeleton=args.draw_skeleton,
        )
    )


if __name__ == "__main__":
    main()
