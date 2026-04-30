from __future__ import annotations

import numpy as np


def confidence_drop(baseline: np.ndarray, attacked: np.ndarray) -> float:
    """Mean confidence reduction from baseline to attacked predictions."""
    if baseline.shape != attacked.shape:
        raise ValueError("baseline and attacked arrays must have the same shape")
    return float(np.mean(baseline - attacked))


def attack_success_rate(attacked_confidences: np.ndarray, threshold: float = 0.25) -> float:
    """Fraction of targets whose attacked confidence falls below threshold."""
    if attacked_confidences.size == 0:
        return 0.0
    return float(np.mean(attacked_confidences < threshold))


def box_iou_xyxy(box_a: np.ndarray, box_b: np.ndarray) -> float:
    """IoU for axis-aligned boxes in `[xmin, ymin, xmax, ymax]` format."""
    xa1, ya1, xa2, ya2 = box_a.astype(float)
    xb1, yb1, xb2, yb2 = box_b.astype(float)

    inter_w = max(0.0, min(xa2, xb2) - max(xa1, xb1))
    inter_h = max(0.0, min(ya2, yb2) - max(ya1, yb1))
    intersection = inter_w * inter_h
    area_a = max(0.0, xa2 - xa1) * max(0.0, ya2 - ya1)
    area_b = max(0.0, xb2 - xb1) * max(0.0, yb2 - yb1)
    union = area_a + area_b - intersection
    return 0.0 if union <= 0 else float(intersection / union)
