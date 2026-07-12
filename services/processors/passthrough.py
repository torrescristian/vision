"""Procesador base para A.2."""

from services.pipeline.types import FramePacket


class PassthroughFrameProcessor:
    """Procesador no-op para validar wiring del pipeline."""

    def process(self, frame: FramePacket[str]) -> FramePacket[str]:
        return frame
