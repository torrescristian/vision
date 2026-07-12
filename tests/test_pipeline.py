"""Tests del pipeline desacoplado de frames."""

from services.pipeline import FramePipeline
from services.processors.passthrough import PassthroughFrameProcessor
from services.providers.mock_provider import MockFrameProvider
from services.renderers.console import ConsoleFrameRenderer


def test_pipeline_processes_all_frames() -> None:
    """El pipeline procesa todos los frames disponibles del provider."""
    provider = MockFrameProvider(frame_count=3)
    processor = PassthroughFrameProcessor()
    renderer = ConsoleFrameRenderer()

    pipeline: FramePipeline[str, str] = FramePipeline(provider, processor, renderer)
    processed = pipeline.run()

    assert processed == 3
    assert renderer.rendered_count == 3
    assert renderer.last_frame_index == 2


def test_pipeline_respects_max_frames() -> None:
    """El pipeline corta en el limite pedido por configuracion."""
    provider = MockFrameProvider(frame_count=10)
    processor = PassthroughFrameProcessor()
    renderer = ConsoleFrameRenderer()

    pipeline: FramePipeline[str, str] = FramePipeline(provider, processor, renderer)
    processed = pipeline.run(max_frames=4)

    assert processed == 4
    assert renderer.rendered_count == 4
    assert renderer.last_frame_index == 3
