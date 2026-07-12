"""Compatibilidad temporal: usar `models.yolo_class` en nuevos imports."""

from models.yolo_class import YoloClass, parse_yolo_class_token

__all__ = ["YoloClass", "parse_yolo_class_token"]
