"""Clases YOLO conocidas con nombres legibles (evita valores magicos)."""

from __future__ import annotations

from enum import IntEnum


class YoloClass(IntEnum):
    """Subset de clases COCO comunes para configuracion amigable."""

    PERSON = 0
    BICYCLE = 1
    CAR = 2
    MOTORCYCLE = 3
    AIRPLANE = 4
    BUS = 5
    TRAIN = 6
    TRUCK = 7
    BOAT = 8
    TRAFFIC_LIGHT = 9
    FIRE_HYDRANT = 10
    STOP_SIGN = 11
    PARKING_METER = 12
    BENCH = 13
    BIRD = 14
    CAT = 15
    DOG = 16
    HORSE = 17
    SHEEP = 18
    COW = 19
    CHAIR = 56
    COUCH = 57
    POTTED_PLANT = 58
    BED = 59
    DINING_TABLE = 60
    LAPTOP = 63
    MOUSE = 64
    KEYBOARD = 66
    CELL_PHONE = 67
    BOOK = 73


def parse_yolo_class_token(token: str) -> int:
    """Parsea clase por nombre (person, car) o id numerico (0,2)."""
    normalized = token.strip().lower().replace("-", "_").replace(" ", "_")
    if not normalized:
        raise ValueError("Clase YOLO vacia no es valida")

    if normalized.isdigit():
        return int(normalized)

    enum_key = normalized.upper()
    try:
        return int(YoloClass[enum_key])
    except KeyError as exc:
        supported = ", ".join(member.name.lower() for member in YoloClass)
        raise ValueError(
            f"Clase '{token}' no reconocida. Usa id numerico o uno de: {supported}"
        ) from exc
