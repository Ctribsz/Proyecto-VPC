from __future__ import annotations

import torch


def differentiable_jpeg_proxy(image: torch.Tensor, quality: int = 80) -> torch.Tensor:
    """Differentiable proxy for JPEG degradation.

    This placeholder models compression as small additive noise. Replace it with a
    DCT/quantization straight-through estimator when physical evaluation begins.
    """
    if not 1 <= quality <= 100:
        raise ValueError("quality must be between 1 and 100")

    noise_scale = (100 - quality) / 100.0 * 0.03
    return (image + torch.randn_like(image) * noise_scale).clamp(0.0, 1.0)
