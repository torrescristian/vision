"""Tracking de personas con YOLO Pose + ByteTrack."""

# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false, reportAttributeAccessIssue=false

from __future__ import annotations

from typing import Any, Callable, Iterable

from models.detections import BoundingBox, Detection, Person
from models.tracked_person import TrackedPerson
from models.yolo_class import YoloClass

TrackFn = Callable[[Any], Iterable[Any]]


def _first_number(value: Any) -> float:
    current = value
    while isinstance(current, (list, tuple)):
        if not current:
            return 0.0
        current = current[0]

    if hasattr(current, "item"):
        return float(current.item())

    return float(current)


def _xyxy_to_ints(raw_xyxy: Any) -> tuple[int, int, int, int]:
    current = raw_xyxy
    while isinstance(current, (list, tuple)) and current and isinstance(current[0], (list, tuple)):
        current = current[0]

    if hasattr(current, "tolist"):
        current = current.tolist()
        while current and isinstance(current[0], list):
            current = current[0]

    x1, y1, x2, y2 = current
    return int(x1), int(y1), int(x2), int(y2)


def _extract_keypoints_for_detection(result: Any, index: int) -> tuple[tuple[int, int], ...]:
    keypoints = getattr(result, "keypoints", None)
    if keypoints is None:
        return ()

    xy = getattr(keypoints, "xy", None)
    if xy is None:
        return ()

    if hasattr(xy, "tolist"):
        xy = xy.tolist()

    if not isinstance(xy, list) or index >= len(xy):
        return ()

    person_points = xy[index]
    if not isinstance(person_points, list):
        return ()

    output: list[tuple[int, int]] = []
    for point in person_points:
        if not isinstance(point, list) or len(point) < 2:
            continue
        x_coord = int(point[0])
        y_coord = int(point[1])
        output.append((x_coord, y_coord))

    return tuple(output)


class YoloPoseByteTrackDetector:
    """Encapsula model.track de Ultralytics con tracker ByteTrack."""

    def __init__(self, track: TrackFn, confidence_threshold: float) -> None:
        self._track = track
        self._confidence_threshold = confidence_threshold

    @classmethod
    def from_model_path(
        cls,
        model_path: str,
        confidence_threshold: float,
        tracker_config: str = "bytetrack.yaml",
    ) -> "YoloPoseByteTrackDetector":
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "Ultralytics no esta instalado. "
                "Ejecuta `uv pip install --python .venv/bin/python -e '.[dev]'`."
            ) from exc

        model = YOLO(model_path)

        def _track(frame: Any) -> Iterable[Any]:
            return model.track(
                frame,
                persist=True,
                tracker=tracker_config,
                conf=confidence_threshold,
                verbose=False,
            )

        return cls(track=_track, confidence_threshold=confidence_threshold)

    def detect(self, frame: Any) -> list[TrackedPerson]:
        tracked_people: list[TrackedPerson] = []
        results = self._track(frame)

        for result in results:
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue

            names = getattr(result, "names", {})
            for box_index, box in enumerate(boxes):
                class_id = int(_first_number(getattr(box, "cls", 0)))
                confidence = _first_number(getattr(box, "conf", 0.0))

                if class_id != YoloClass.PERSON or confidence < self._confidence_threshold:
                    continue

                track_id_raw = getattr(box, "id", None)
                if track_id_raw is None:
                    continue

                track_id = int(_first_number(track_id_raw))
                x1, y1, x2, y2 = _xyxy_to_ints(getattr(box, "xyxy"))
                class_name = str(names.get(class_id, "person"))
                keypoints = _extract_keypoints_for_detection(result, box_index)

                tracked_people.append(
                    TrackedPerson(
                        track_id=track_id,
                        detection=Detection(
                            subject=Person(label=class_name),
                            confidence=confidence,
                            bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                            source="yolo11-pose-bytetrack",
                        ),
                        keypoints=keypoints,
                    )
                )

        return tracked_people
