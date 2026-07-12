"""Configuracion centralizada del proyecto (Hito A.3)."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CameraConfig:
    """Configuracion de captura de video."""

    index: int = 0
    width: int = 1280
    height: int = 720
    target_fps: int = 30


@dataclass(frozen=True, slots=True)
class YoloConfig:
    """Configuracion del modelo YOLO."""

    model_path: str = "yolov8n.pt"
    person_confidence_threshold: float = 0.45


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Configuracion principal de la app."""

    camera: CameraConfig
    yolo: YoloConfig


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    return float(value)


def _env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value


def load_config() -> AppConfig:
    """Carga la configuracion, permitiendo override por variables de entorno."""
    return AppConfig(
        camera=CameraConfig(
            index=_env_int("VISION_CAMERA_INDEX", 0),
            width=_env_int("VISION_CAMERA_WIDTH", 1280),
            height=_env_int("VISION_CAMERA_HEIGHT", 720),
            target_fps=_env_int("VISION_CAMERA_FPS", 30),
        ),
        yolo=YoloConfig(
            model_path=_env_str("VISION_YOLO_MODEL", "yolov8n.pt"),
            person_confidence_threshold=_env_float("VISION_YOLO_CONFIDENCE", 0.45),
        ),
    )
