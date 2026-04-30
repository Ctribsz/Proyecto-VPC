from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin
from typing import Sequence

Point = tuple[float, float]
Polygon = tuple[Point, Point, Point, Point]


@dataclass(frozen=True)
class OrientedBBox:
    """Oriented rectangle represented by center, size, and angle in degrees."""

    cx: float
    cy: float
    width: float
    height: float
    angle_deg: float

    def corners(self) -> Polygon:
        theta = radians(self.angle_deg)
        dx = self.width / 2.0
        dy = self.height / 2.0
        local = ((-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy))
        c = cos(theta)
        s = sin(theta)
        return tuple((self.cx + x * c - y * s, self.cy + x * s + y * c) for x, y in local)  # type: ignore[return-value]


def polygon_area(points: Sequence[Point]) -> float:
    """Return the absolute area of a polygon using the shoelace formula."""
    if len(points) < 3:
        return 0.0

    area = 0.0
    for idx, (x1, y1) in enumerate(points):
        x2, y2 = points[(idx + 1) % len(points)]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def axis_aligned_bbox(points: Sequence[Point]) -> tuple[float, float, float, float]:
    """Convert a polygon to an axis-aligned box `(xmin, ymin, xmax, ymax)`."""
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def flatten_polygon(points: Sequence[Point]) -> tuple[float, ...]:
    """Flatten polygon points into DOTA-style coordinate order."""
    return tuple(coord for point in points for coord in point)
