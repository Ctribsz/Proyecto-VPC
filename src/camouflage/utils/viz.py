from __future__ import annotations

from typing import Sequence

import numpy as np

from camouflage.data.obb import Point


def draw_polygon(
    image: np.ndarray,
    polygon: Sequence[Point],
    color: tuple[int, int, int] = (255, 0, 0),
    thickness: int = 2,
) -> np.ndarray:
    """Draw a quadrilateral on an image using OpenCV."""
    try:
        import cv2
    except ImportError as exc:
        raise ImportError("Install opencv-python to use draw_polygon.") from exc

    output = image.copy()
    points = np.asarray(polygon, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(output, [points], isClosed=True, color=color, thickness=thickness)
    return output
