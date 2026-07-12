"""Tests para modelos de dominio de deteccion (Hito A.5)."""

from models.detections import BoundingBox, Detection, Person


def test_bounding_box_center_width_height() -> None:
    bbox = BoundingBox(x1=10, y1=20, x2=30, y2=40)

    assert bbox.width == 20
    assert bbox.height == 20
    assert bbox.center == (20.0, 30.0)


def test_detection_is_domain_model() -> None:
    detection = Detection(
        subject=Person(),
        confidence=0.9,
        bbox=BoundingBox(x1=1, y1=2, x2=3, y2=4),
    )

    assert detection.subject.label == "person"
    assert detection.source == "yolo"
