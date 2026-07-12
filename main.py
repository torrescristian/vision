"""Punto de entrada principal del proyecto."""

from dataclasses import dataclass

from services.pipeline import FramePipeline
from services.processors.passthrough import PassthroughFrameProcessor
from services.providers.mock_provider import MockFrameProvider
from services.renderers.console import ConsoleFrameRenderer


@dataclass(frozen=True, slots=True)
class DemoPipelineConfig:
    """Config del demo para mantener parametros juntos y faciles de extender."""

    frame_count: int = 5


def build_demo_pipeline(config: DemoPipelineConfig) -> FramePipeline[str, str]:
    """Arma el pipeline de demo (equivalente a un composition root en JS)."""
    provider = MockFrameProvider(frame_count=config.frame_count)
    processor = PassthroughFrameProcessor()
    renderer = ConsoleFrameRenderer()

    return FramePipeline(provider=provider, processor=processor, renderer=renderer)


def run_demo_pipeline(config: DemoPipelineConfig) -> int:
    """Ejecuta el pipeline de demo y retorna cantidad de frames procesados."""
    pipeline = build_demo_pipeline(config)
    return pipeline.run()


def main() -> None:
    """Ejecuta una corrida de ejemplo del pipeline desacoplado."""
    processed = run_demo_pipeline(DemoPipelineConfig())

    print(f"Vision Engine inicializado - pipeline A.2 OK ({processed} frames)")


if __name__ == "__main__":
    main()
