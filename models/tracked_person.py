"""Entidad de dominio para persona trackeada."""

from __future__ import annotations

from dataclasses import dataclass

from models.detections import Detection


@dataclass(frozen=True, slots=True)
class TrackedPerson:
    """Deteccion enriquecida con identidad persistente y keypoints opcionales."""

    track_id: int
    detection: Detection
    keypoints: tuple[tuple[int, int], ...] = ()
