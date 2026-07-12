"""Tests para configuracion centralizada (Hito A.3)."""

from pytest import MonkeyPatch

from config import load_config


def test_load_config_uses_defaults_when_env_is_missing(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("VISION_CAMERA_INDEX", raising=False)
    monkeypatch.delenv("VISION_CAMERA_WIDTH", raising=False)
    monkeypatch.delenv("VISION_CAMERA_HEIGHT", raising=False)
    monkeypatch.delenv("VISION_CAMERA_FPS", raising=False)
    monkeypatch.delenv("VISION_YOLO_MODEL", raising=False)
    monkeypatch.delenv("VISION_YOLO_CONFIDENCE", raising=False)
    monkeypatch.delenv("VISION_YOLO_TRACKER", raising=False)
    monkeypatch.delenv("VISION_YOLO_DRAW_SKELETON", raising=False)

    cfg = load_config()

    assert cfg.camera.index == 0
    assert cfg.camera.width == 1280
    assert cfg.camera.height == 720
    assert cfg.camera.target_fps == 30
    assert cfg.yolo.model_path == "yolo11n-pose.pt"
    assert cfg.yolo.person_confidence_threshold == 0.45
    assert cfg.yolo.tracker_config == "bytetrack.yaml"
    assert cfg.yolo.draw_skeleton is True


def test_load_config_reads_env_overrides(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("VISION_CAMERA_INDEX", "2")
    monkeypatch.setenv("VISION_CAMERA_WIDTH", "1920")
    monkeypatch.setenv("VISION_CAMERA_HEIGHT", "1080")
    monkeypatch.setenv("VISION_CAMERA_FPS", "25")
    monkeypatch.setenv("VISION_YOLO_MODEL", "yolo11s-pose.pt")
    monkeypatch.setenv("VISION_YOLO_CONFIDENCE", "0.6")
    monkeypatch.setenv("VISION_YOLO_TRACKER", "bytetrack.yaml")
    monkeypatch.setenv("VISION_YOLO_DRAW_SKELETON", "false")

    cfg = load_config()

    assert cfg.camera.index == 2
    assert cfg.camera.width == 1920
    assert cfg.camera.height == 1080
    assert cfg.camera.target_fps == 25
    assert cfg.yolo.model_path == "yolo11s-pose.pt"
    assert cfg.yolo.person_confidence_threshold == 0.6
    assert cfg.yolo.tracker_config == "bytetrack.yaml"
    assert cfg.yolo.draw_skeleton is False
