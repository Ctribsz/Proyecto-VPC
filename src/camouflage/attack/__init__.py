"""Digital attack components."""

from camouflage.attack.losses import detection_confidence_loss, total_variation_loss
from camouflage.attack.texture import make_texture_parameters, texture_from_parameters

__all__ = [
    "detection_confidence_loss",
    "make_texture_parameters",
    "texture_from_parameters",
    "total_variation_loss",
]
