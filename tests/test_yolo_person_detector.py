"""Tests para filtro de personas del detector YOLO."""

from dataclasses import dataclass

from detectors.yolo_person import YoloPersonDetector


@dataclass
class _FakeBox:
    cls: list[float]
    conf: list[float]
    xyxy: list[list[float]]


@dataclass
class _FakeResult:
    boxes: list[_FakeBox]


def test_detector_filters_only_person_class_and_threshold() -> None:
    frame = "frame"
    results = [
        _FakeResult(
            boxes=[
                _FakeBox(cls=[0.0], conf=[0.91], xyxy=[[10.0, 20.0, 30.0, 40.0]]),
                _FakeBox(cls=[2.0], conf=[0.99], xyxy=[[1.0, 2.0, 3.0, 4.0]]),
                _FakeBox(cls=[0.0], conf=[0.20], xyxy=[[5.0, 6.0, 7.0, 8.0]]),
            ]
        )
    ]

    detector = YoloPersonDetector(infer=lambda _: results, confidence_threshold=0.5)
    detections = detector.detect(frame)

    assert len(detections) == 1
    first = detections[0]
    assert (first.x1, first.y1, first.x2, first.y2) == (10, 20, 30, 40)
    assert first.confidence == 0.91


def test_detector_supports_empty_results() -> None:
    detector = YoloPersonDetector(infer=lambda _: [], confidence_threshold=0.5)
    detections = detector.detect("frame")
    assert detections == []
