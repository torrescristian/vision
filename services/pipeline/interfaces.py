"""Contratos del pipeline de frames."""

from typing import Generic, Iterator, Protocol, TypeVar

from services.pipeline.types import FramePacket

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class FrameProvider(Protocol, Generic[TIn]):
    """Expone una fuente iterable de frames (webcam, RTSP, mock)."""

    def open(self) -> None:
        """Inicializa recursos del proveedor."""
        ...

    def close(self) -> None:
        """Libera recursos del proveedor."""
        ...

    def __iter__(self) -> Iterator[FramePacket[TIn]]:
        """Itera frames crudos del origen."""
        ...


class FrameProcessor(Protocol, Generic[TIn, TOut]):
    """Transforma un frame de entrada en otro frame procesado."""

    def process(self, frame: FramePacket[TIn]) -> FramePacket[TOut]:
        """Procesa un frame crudo."""
        ...


class FrameRenderer(Protocol, Generic[TOut]):
    """Consume frames procesados para visualizacion/salida."""

    def render(self, frame: FramePacket[TOut]) -> None:
        """Renderiza un frame procesado."""
        ...

    def close(self) -> None:
        """Libera recursos del renderer."""
        ...
