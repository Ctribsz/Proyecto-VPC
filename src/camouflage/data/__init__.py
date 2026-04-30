"""Dataset loading and oriented bounding box utilities."""

from camouflage.data.dota import DotaAnnotation, parse_dota_label_file
from camouflage.data.obb import OrientedBBox, axis_aligned_bbox, polygon_area

__all__ = [
    "DotaAnnotation",
    "OrientedBBox",
    "axis_aligned_bbox",
    "parse_dota_label_file",
    "polygon_area",
]
