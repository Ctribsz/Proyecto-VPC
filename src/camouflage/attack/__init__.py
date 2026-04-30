"""Digital attack components."""

from importlib import import_module

_EXPORT_MODULES = {
    "detection_confidence_loss": "camouflage.attack.losses",
    "make_texture_parameters": "camouflage.attack.texture",
    "texture_from_parameters": "camouflage.attack.texture",
    "total_variation_loss": "camouflage.attack.losses",
}

__all__ = [
    "detection_confidence_loss",
    "make_texture_parameters",
    "texture_from_parameters",
    "total_variation_loss",
]


def __getattr__(name: str):
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(module_name), name)
    globals()[name] = value
    return value
