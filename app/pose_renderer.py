"""Helpers de render para overlays de deteccion y pose."""

from __future__ import annotations

from typing import Any

from models.pose_keypoint import PoseKeypoint
from models.tracked_person import TrackedPerson

# Pares anatomicos del esqueleto COCO usando enum (sin numeros magicos).
COCO_SKELETON_EDGES: tuple[tuple[PoseKeypoint, PoseKeypoint], ...] = (
    (PoseKeypoint.NOSE, PoseKeypoint.LEFT_EYE),
    (PoseKeypoint.NOSE, PoseKeypoint.RIGHT_EYE),
    (PoseKeypoint.LEFT_EYE, PoseKeypoint.LEFT_EAR),
    (PoseKeypoint.RIGHT_EYE, PoseKeypoint.RIGHT_EAR),
    (PoseKeypoint.LEFT_SHOULDER, PoseKeypoint.RIGHT_SHOULDER),
    (PoseKeypoint.LEFT_SHOULDER, PoseKeypoint.LEFT_ELBOW),
    (PoseKeypoint.LEFT_ELBOW, PoseKeypoint.LEFT_WRIST),
    (PoseKeypoint.RIGHT_SHOULDER, PoseKeypoint.RIGHT_ELBOW),
    (PoseKeypoint.RIGHT_ELBOW, PoseKeypoint.RIGHT_WRIST),
    (PoseKeypoint.LEFT_SHOULDER, PoseKeypoint.LEFT_HIP),
    (PoseKeypoint.RIGHT_SHOULDER, PoseKeypoint.RIGHT_HIP),
    (PoseKeypoint.LEFT_HIP, PoseKeypoint.RIGHT_HIP),
    (PoseKeypoint.LEFT_HIP, PoseKeypoint.LEFT_KNEE),
    (PoseKeypoint.LEFT_KNEE, PoseKeypoint.LEFT_ANKLE),
    (PoseKeypoint.RIGHT_HIP, PoseKeypoint.RIGHT_KNEE),
    (PoseKeypoint.RIGHT_KNEE, PoseKeypoint.RIGHT_ANKLE),
)


def draw_detection_box(cv2: Any, frame: Any, tracked: TrackedPerson) -> None:
    detection = tracked.detection
    bbox = detection.bbox
    cv2.rectangle(
        img=frame,
        pt1=(bbox.x1, bbox.y1),
        pt2=(bbox.x2, bbox.y2),
        color=(255, 0, 0),
        thickness=2,
    )
    cv2.putText(
        img=frame,
        text=f"Person {tracked.track_id} {detection.confidence:.2f}",
        org=(bbox.x1, max(bbox.y1 - 8, 20)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.65,
        color=(0, 200, 255),
        thickness=2,
        lineType=cv2.LINE_AA,
    )


def draw_pose_keypoints(cv2: Any, frame: Any, tracked: TrackedPerson) -> None:
    for x_coord, y_coord in tracked.keypoints:
        cv2.circle(
            img=frame,
            center=(x_coord, y_coord),
            radius=3,
            color=(0, 255, 255),
            thickness=-1,
            lineType=cv2.LINE_AA,
        )


def draw_pose_skeleton(cv2: Any, frame: Any, tracked: TrackedPerson) -> None:
    points = tracked.keypoints
    for start_keypoint, end_keypoint in COCO_SKELETON_EDGES:
        start_point = _get_keypoint(points, start_keypoint)
        end_point = _get_keypoint(points, end_keypoint)
        if start_point is None or end_point is None:
            continue
        if not (_is_valid_keypoint(start_point) and _is_valid_keypoint(end_point)):
            continue
        cv2.line(
            img=frame,
            pt1=start_point,
            pt2=end_point,
            color=(255, 255, 0),
            thickness=2,
            lineType=cv2.LINE_AA,
        )


def draw_global_overlay(cv2: Any, frame: Any, fps: float, people_count: int) -> None:
    cv2.putText(
        img=frame,
        text=f"FPS: {fps:.1f}  Persons: {people_count}",
        org=(12, 30),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.85,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA,
    )


def _is_valid_keypoint(point: tuple[int, int]) -> bool:
    return point != (0, 0)


def _get_keypoint(
    points: tuple[tuple[int, int], ...],
    keypoint: PoseKeypoint,
) -> tuple[int, int] | None:
    keypoint_index = int(keypoint)
    if keypoint_index >= len(points):
        return None
    return points[keypoint_index]
