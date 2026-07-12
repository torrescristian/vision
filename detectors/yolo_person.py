"""Detector YOLO especializado en la clase `person` (Hito A.4)."""

# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false, reportAttributeAccessIssue=false

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from models.YoloClass import YoloClass

InferFn = Callable[[Any], Iterable[Any]]


@dataclass(frozen=True, slots=True)
class PersonDetection:
    """Representa una deteccion de persona en un frame."""

    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float


def _first_number(value: Any) -> float:
    """Extrae un numero de estructuras como tensor/lista/escalares."""
    # Ultralytics puede devolver escalares, tensores o listas anidadas.
    # Esta funcion normaliza todo a float para simplificar el flujo posterior.
    current = value
    while isinstance(current, (list, tuple)):
        if not current:
            return 0.0
        current = current[0]

    if hasattr(current, "item"):
        return float(current.item())

    return float(current)


def _xyxy_to_ints(raw_xyxy: Any) -> tuple[int, int, int, int]:
    """Normaliza coordenadas `xyxy` a enteros."""
    # El objetivo es tener siempre (x1, y1, x2, y2) como ints para dibujar
    # en OpenCV sin condicionales extra por tipo.
    current = raw_xyxy
    while isinstance(current, (list, tuple)) and current and isinstance(current[0], (list, tuple)):
        current = current[0]

    if hasattr(current, "tolist"):
        current = current.tolist()
        while current and isinstance(current[0], list):
            current = current[0]

    x1, y1, x2, y2 = current
    return int(x1), int(y1), int(x2), int(y2)


class YoloPersonDetector:
    """Encapsula inferencia YOLO y expone solo detecciones de personas."""

    def __init__(self, infer: InferFn, confidence_threshold: float) -> None:
        self._infer = infer
        self._confidence_threshold = confidence_threshold

    @classmethod
    def from_model_path(cls, model_path: str, confidence_threshold: float) -> "YoloPersonDetector":
        """Crea detector desde un path de modelo YOLO usando Ultralytics."""
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError(
                "Ultralytics no esta instalado. "
                "Ejecuta `uv pip install --python .venv/bin/python -e '.[dev]'`."
            ) from exc

        model = YOLO(model_path)

        def _infer(frame: Any) -> Iterable[Any]:
            return model(frame, verbose=False)

        return cls(infer=_infer, confidence_threshold=confidence_threshold)

    def detect(self, frame: Any) -> list[PersonDetection]:
        """Ejecuta inferencia y retorna solo detecciones clase person (id 0)."""
        detections: list[PersonDetection] = []
        results = self._infer(frame)

        for result in results:
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue

            for box in boxes:
                class_id = int(_first_number(getattr(box, "cls", 0)))
                confidence = _first_number(getattr(box, "conf", 0.0))

                # YOLO devuelve todas las clases detectadas.
                # Aqui filtramos solo persona y por confianza minima.
                if class_id != YoloClass.PERSON or confidence < self._confidence_threshold:
                    continue

                x1, y1, x2, y2 = _xyxy_to_ints(getattr(box, "xyxy"))
                detections.append(
                    PersonDetection(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        confidence=confidence,
                    )
                )

        return detections
