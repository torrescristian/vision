"""Proveedor de frames de prueba para el Hito A.2."""

from collections.abc import Iterator

from services.pipeline.types import FramePacket


class MockFrameProvider:
    """Genera frames sinteticos para validar el pipeline sin webcam/RTSP."""

    def __init__(self, frame_count: int = 30, source: str = "mock://camera") -> None:
        self._frame_count = frame_count
        self._source = source
        self._is_open = False

    def open(self) -> None:
        self._is_open = True

    def close(self) -> None:
        self._is_open = False

    def __iter__(self) -> Iterator[FramePacket[str]]:
        if not self._is_open:
            raise RuntimeError("El provider debe abrirse antes de iterar frames")

        for index in range(self._frame_count):
            yield FramePacket(index=index, payload=f"frame-{index}", source=self._source)
