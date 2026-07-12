"""Tipos de dominio para el pipeline de frames."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar

TFramePayload = TypeVar("TFramePayload")


@dataclass(slots=True)
class FramePacket(Generic[TFramePayload]):
    """Representa un frame con metadata agnostica al proveedor de video."""

    index: int
    payload: TFramePayload
    source: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
