"""Orquestador del pipeline desacoplado de frames."""

from typing import Generic, TypeVar

from services.pipeline.interfaces import FrameProcessor, FrameProvider, FrameRenderer

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class FramePipeline(Generic[TIn, TOut]):
    """Conecta provider, processor y renderer sin acoplar implementaciones."""

    def __init__(
        self,
        provider: FrameProvider[TIn],
        processor: FrameProcessor[TIn, TOut],
        renderer: FrameRenderer[TOut],
    ) -> None:
        self._provider = provider
        self._processor = processor
        self._renderer = renderer

    def _open_resources(self) -> None:
        """Abre recursos de entrada antes de arrancar el loop principal."""
        self._provider.open()

    def _close_resources(self) -> None:
        """Cierra recursos siempre, incluso si ocurre una excepcion."""
        self._provider.close()
        self._renderer.close()

    def _should_stop(self, processed: int, max_frames: int | None) -> bool:
        if max_frames is None:
            return False
        return processed >= max_frames

    def run(self, max_frames: int | None = None) -> int:
        """Ejecuta el pipeline y retorna la cantidad de frames procesados."""
        if max_frames is not None and max_frames <= 0:
            return 0

        processed = 0
        self._open_resources()
        try:
            # Este loop es el "event loop" del pipeline: lee, procesa y renderiza.
            for frame in self._provider:
                processed_frame = self._processor.process(frame)
                self._renderer.render(processed_frame)
                processed += 1
                if self._should_stop(processed, max_frames):
                    break
        finally:
            self._close_resources()

        return processed
