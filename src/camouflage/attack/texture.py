from __future__ import annotations

from typing import Literal

import torch

InitMode = Literal["uniform", "gray", "noise"]


def make_texture_parameters(
    size: tuple[int, int],
    init: InitMode = "uniform",
    device: torch.device | str | None = None,
) -> torch.nn.Parameter:
    """Create unconstrained RGB texture parameters with shape `[3, H, W]`."""
    height, width = size
    if init == "gray":
        values = torch.full((3, height, width), 0.5, device=device)
    elif init == "noise":
        values = torch.rand((3, height, width), device=device)
    elif init == "uniform":
        values = torch.empty((3, height, width), device=device).uniform_(0.35, 0.65)
    else:
        raise ValueError(f"Unsupported texture init: {init}")

    eps = torch.finfo(values.dtype).eps
    logits = torch.logit(values.clamp(eps, 1.0 - eps))
    return torch.nn.Parameter(logits)


def texture_from_parameters(parameters: torch.Tensor) -> torch.Tensor:
    """Map unconstrained texture parameters to printable RGB range `[0, 1]`."""
    return torch.sigmoid(parameters)
