"""Tests para detector YOLO Pose + ByteTrack."""

from dataclasses import dataclass

from detectors.yolo_pose_bytetrack import YoloPoseByteTrackDetector


@dataclass
class _FakeBox:
    cls: list[float]
    conf: list[float]
    xyxy: list[list[float]]
    id: list[float] | None


@dataclass
class _FakeResult:
    boxes: list[_FakeBox]
    names: dict[int, str]
    keypoints: object | None = None


@dataclass
class _FakeKeypoints:
    xy: list[list[list[float]]]


def test_pose_bytetrack_detector_returns_tracked_persons() -> None:
    frame = "frame"
    results = [
        _FakeResult(
            boxes=[
                _FakeBox(
                    cls=[0.0],
                    conf=[0.88],
                    xyxy=[[10.0, 20.0, 30.0, 40.0]],
                    id=[7.0],
                ),
                _FakeBox(
                    cls=[2.0],
                    conf=[0.95],
                    xyxy=[[100.0, 120.0, 180.0, 200.0]],
                    id=[11.0],
                ),
            ],
            names={0: "person", 2: "car"},
        )
    ]

    detector = YoloPoseByteTrackDetector(track=lambda _: results, confidence_threshold=0.5)
    tracked = detector.detect(frame)

    assert len(tracked) == 1
    first = tracked[0]
    assert first.track_id == 7
    assert first.detection.subject.label == "person"
    assert first.detection.confidence == 0.88
    assert (first.detection.bbox.x1, first.detection.bbox.y1) == (10, 20)


def test_pose_bytetrack_detector_ignores_boxes_without_track_id() -> None:
    results = [
        _FakeResult(
            boxes=[
                _FakeBox(
                    cls=[0.0],
                    conf=[0.88],
                    xyxy=[[10.0, 20.0, 30.0, 40.0]],
                    id=None,
                )
            ],
            names={0: "person"},
        )
    ]

    detector = YoloPoseByteTrackDetector(track=lambda _: results, confidence_threshold=0.5)
    tracked = detector.detect("frame")
    assert tracked == []


def test_pose_bytetrack_detector_includes_keypoints() -> None:
    results = [
        _FakeResult(
            boxes=[
                _FakeBox(
                    cls=[0.0],
                    conf=[0.91],
                    xyxy=[[5.0, 10.0, 40.0, 60.0]],
                    id=[3.0],
                )
            ],
            names={0: "person"},
            keypoints=_FakeKeypoints(
                xy=[
                    [
                        [12.4, 22.7],
                        [16.1, 30.9],
                    ]
                ]
            ),
        )
    ]

    detector = YoloPoseByteTrackDetector(track=lambda _: results, confidence_threshold=0.5)
    tracked = detector.detect("frame")

    assert len(tracked) == 1
    assert tracked[0].keypoints == ((12, 22), (16, 30))
