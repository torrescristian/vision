"""Modelos de dominio."""

from models.detections import BoundingBox, Detection, Person
from models.tracked_person import TrackedPerson

__all__ = ["BoundingBox", "Detection", "Person", "TrackedPerson"]
