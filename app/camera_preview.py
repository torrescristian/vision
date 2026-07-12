"""Runner de captura de webcam para el Hito A.1."""

from __future__ import annotations

import argparse
import os
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

EXIT_KEYS = (ord("q"), 27)


@dataclass(frozen=True, slots=True)
class CameraPreviewConfig:
    """Configuracion de runtime para el preview de camara."""

    camera_index: int = 0
    width: int = 1280
    height: int = 720
    window_name: str = "Vision Engine - Webcam"


def compute_fps(previous_tick: float, current_tick: float) -> float:
    """Calcula FPS instantaneo evitando division por cero."""
    delta = current_tick - previous_tick
    if delta <= 0:
        return 0.0
    return 1.0 / delta


def _load_cv2(cv2_module: Any | None) -> Any:
    """Permite inyectar cv2 en tests y usar import real en runtime."""
    if cv2_module is not None:
        return cv2_module

    import cv2 as imported_cv2

    return imported_cv2


def _open_capture(cv2: Any, config: CameraPreviewConfig) -> Any:
    """Abre la camara y aplica resolucion objetivo."""
    capture = cv2.VideoCapture(config.camera_index)
    if not capture.isOpened():
        raise RuntimeError(f"No se pudo abrir la webcam en indice {config.camera_index}")

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
    return capture


def _initialize_window(cv2: Any, window_name: str) -> None:
    """Inicializa la ventana de forma explicita para evitar glitches de UI en macOS."""
    window_flags = getattr(cv2, "WINDOW_NORMAL", 0)
    cv2.namedWindow(window_name, window_flags)

    # Similar a forzar un mount/render inicial en frontend: evita ventanas invisibles.
    if hasattr(cv2, "moveWindow"):
        cv2.moveWindow(window_name, 120, 120)
    if hasattr(cv2, "startWindowThread"):
        cv2.startWindowThread()


def _draw_overlay(cv2: Any, frame: Any, fps: float) -> None:
    """Dibuja metadata minima sobre el frame antes de renderizar."""
    cv2.putText(
        img=frame,
        text=f"FPS: {fps:.1f}",
        org=(12, 30),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.9,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA,
    )


def _print_startup_message(config: CameraPreviewConfig) -> None:
    print(
        f"[vision-camera] Camara {config.camera_index} iniciada en "
        f"{config.width}x{config.height}. Presiona q o ESC para salir.",
        file=sys.stderr,
    )


def _ensure_graphical_session() -> None:
    # Si existe SSH_CONNECTION, probablemente no hay contexto grafico local para abrir ventanas.
    if os.environ.get("SSH_CONNECTION"):
        raise RuntimeError(
            "No se detecta sesion grafica local (SSH_CONNECTION activo). "
            "Ejecuta vision-camera en una sesion local de macOS para ver la UI."
        )


def run_camera_preview(
    camera_index: int = 0,
    width: int = 1280,
    height: int = 720,
    window_name: str = "Vision Engine - Webcam",
    *,
    cv2_module: Any | None = None,
) -> None:
    """Muestra stream de webcam con FPS y permite salir con q o ESC."""
    config = CameraPreviewConfig(
        camera_index=camera_index,
        width=width,
        height=height,
        window_name=window_name,
    )
    cv2 = _load_cv2(cv2_module)
    capture = _open_capture(cv2, config)
    _initialize_window(cv2, config.window_name)
    _print_startup_message(config)

    last_tick = time.perf_counter()
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                raise RuntimeError("No se pudo leer un frame desde la webcam")

            current_tick = time.perf_counter()
            fps = compute_fps(last_tick, current_tick)
            last_tick = current_tick

            _draw_overlay(cv2, frame, fps)
            cv2.imshow(config.window_name, frame)

            key = cv2.waitKey(1) & 0xFF
            if key in EXIT_KEYS:
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Captura webcam con FPS en vivo")
    parser.add_argument("--camera-index", type=int, default=0, help="Indice de camara")
    parser.add_argument("--width", type=int, default=1280, help="Resolucion horizontal")
    parser.add_argument("--height", type=int, default=720, help="Resolucion vertical")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """CLI del preview de webcam."""
    _ensure_graphical_session()

    parser = _build_parser()
    args = parser.parse_args(argv)
    run_camera_preview(camera_index=args.camera_index, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
