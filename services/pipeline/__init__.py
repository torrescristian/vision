"""API publica del pipeline de frames."""

from services.pipeline.engine import FramePipeline
from services.pipeline.interfaces import FrameProcessor, FrameProvider, FrameRenderer
from services.pipeline.types import FramePacket

__all__ = ["FramePacket", "FramePipeline", "FrameProvider", "FrameProcessor", "FrameRenderer"]
