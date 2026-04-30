"""Evaluation helpers."""

from importlib import import_module

_EXPORT_MODULES = {
    "attack_success_rate": "camouflage.eval.metrics",
    "box_iou_xyxy": "camouflage.eval.metrics",
    "confidence_drop": "camouflage.eval.metrics",
}

__all__ = ["attack_success_rate", "box_iou_xyxy", "confidence_drop"]


def __getattr__(name: str):
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(module_name), name)
    globals()[name] = value
    return value
