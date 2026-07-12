"""Modelos de dominio para detecciones (Hito A.5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """Caja delimitadora independiente del proveedor de visión."""

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return max(0, self.x2 - self.x1)

    @property
    def height(self) -> int:
        return max(0, self.y2 - self.y1)

    @property
    def center(self) -> tuple[float, float]:
        center_x = (self.x1 + self.x2) / 2.0
        center_y = (self.y1 + self.y2) / 2.0
        return center_x, center_y


@dataclass(frozen=True, slots=True)
class Person:
    """Entidad de persona en dominio (sin acoplar a YOLO)."""

    label: str = "person"


@dataclass(frozen=True, slots=True)
class Detection:
    """Detección de dominio desacoplada del formato de Ultralytics."""

    subject: Person
    confidence: float
    bbox: BoundingBox
    source: str = "yolo"
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
