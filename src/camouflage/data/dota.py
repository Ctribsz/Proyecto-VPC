from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from camouflage.data.obb import Polygon


@dataclass(frozen=True)
class DotaAnnotation:
    """Single DOTA label record with a quadrilateral object polygon."""

    image_id: str
    polygon: Polygon
    category: str
    difficult: int = 0


def parse_dota_label_file(label_path: str | Path) -> list[DotaAnnotation]:
    """Parse one DOTA label text file.

    Expected row format:
    x1 y1 x2 y2 x3 y3 x4 y4 category difficult
    """
    path = Path(label_path)
    annotations: list[DotaAnnotation] = []

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 9:
            raise ValueError(f"Invalid DOTA label at {path}:{line_number}: {raw_line!r}")

        coords = [float(value) for value in parts[:8]]
        polygon = tuple((coords[idx], coords[idx + 1]) for idx in range(0, 8, 2))
        difficult = int(parts[9]) if len(parts) > 9 else 0
        annotations.append(
            DotaAnnotation(
                image_id=path.stem,
                polygon=polygon,  # type: ignore[arg-type]
                category=parts[8],
                difficult=difficult,
            )
        )

    return annotations


def iter_dota_labels(labels_dir: str | Path) -> Iterable[Path]:
    """Yield DOTA label files in deterministic order."""
    yield from sorted(Path(labels_dir).glob("*.txt"))


def load_dota_annotations(labels_dir: str | Path) -> list[DotaAnnotation]:
    """Load all annotations from a DOTA labels directory."""
    annotations: list[DotaAnnotation] = []
    for label_file in iter_dota_labels(labels_dir):
        annotations.extend(parse_dota_label_file(label_file))
    return annotations
