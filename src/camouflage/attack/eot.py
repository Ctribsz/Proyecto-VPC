from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class EOTConfig:
    brightness: tuple[float, float] = (0.75, 1.25)
    contrast: tuple[float, float] = (0.80, 1.20)
    noise_std: tuple[float, float] = (0.0, 0.02)


def sample_uniform(
    shape: tuple[int, ...],
    value_range: tuple[float, float],
    device: torch.device,
) -> torch.Tensor:
    low, high = value_range
    return torch.empty(shape, device=device).uniform_(low, high)


def apply_color_eot(batch: torch.Tensor, config: EOTConfig | None = None) -> torch.Tensor:
    """Apply differentiable color perturbations for expectation over transformation."""
    if batch.ndim != 4:
        raise ValueError("batch must have shape [B,C,H,W]")

    cfg = config or EOTConfig()
    bsz = batch.shape[0]
    brightness = sample_uniform((bsz, 1, 1, 1), cfg.brightness, batch.device)
    contrast = sample_uniform((bsz, 1, 1, 1), cfg.contrast, batch.device)
    noise_std = sample_uniform((bsz, 1, 1, 1), cfg.noise_std, batch.device)

    mean = batch.mean(dim=(-2, -1), keepdim=True)
    transformed = (batch - mean) * contrast + mean
    transformed = transformed * brightness
    transformed = transformed + torch.randn_like(transformed) * noise_std
    return transformed.clamp(0.0, 1.0)
