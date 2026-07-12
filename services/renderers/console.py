"""Renderer de consola para validar salida del pipeline."""

from services.pipeline.types import FramePacket


class ConsoleFrameRenderer:
    """Renderer minimalista que acumula estadisticas en memoria."""

    def __init__(self) -> None:
        self.rendered_count = 0
        self.last_frame_index: int | None = None

    def render(self, frame: FramePacket[str]) -> None:
        self.rendered_count += 1
        self.last_frame_index = frame.index

    def close(self) -> None:
        return None
