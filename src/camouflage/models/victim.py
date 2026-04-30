from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VictimConfig:
    weights: str = "yolov8n-obb.pt"
    task: str = "obb"
    conf_threshold: float = 0.25
    iou_threshold: float = 0.7
    device: str | None = None


class VictimDetector:
    """Thin wrapper around Ultralytics YOLO models.

    The wrapper keeps model-specific details isolated from training and eval code.
    """

    def __init__(self, config: VictimConfig | None = None, **kwargs: Any) -> None:
        self.config = config or VictimConfig(**kwargs)
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise ImportError("Install ultralytics to use VictimDetector.") from exc

        self.model = YOLO(self.config.weights, task=self.config.task)

    def predict(self, image: Any, **kwargs: Any) -> Any:
        """Run inference and return raw Ultralytics results."""
        return self.model.predict(
            image,
            conf=self.config.conf_threshold,
            iou=self.config.iou_threshold,
            device=self.config.device,
            **kwargs,
        )
