from __future__ import annotations

import torch
import torch.nn.functional as F


def resize_texture(texture: torch.Tensor, size: tuple[int, int]) -> torch.Tensor:
    """Resize `[C,H,W]` or `[B,C,H,W]` texture tensors with bilinear sampling."""
    batched = texture.ndim == 4
    work = texture if batched else texture.unsqueeze(0)
    resized = F.interpolate(work, size=size, mode="bilinear", align_corners=False)
    return resized if batched else resized.squeeze(0)


def overlay_texture(
    image: torch.Tensor,
    texture: torch.Tensor,
    mask: torch.Tensor,
    alpha: float = 1.0,
) -> torch.Tensor:
    """Alpha-blend a texture into an image using a differentiable mask.

    Tensors are expected in channel-first format and normalized to `[0, 1]`.
    """
    if image.ndim not in {3, 4}:
        raise ValueError("image must have shape [C,H,W] or [B,C,H,W]")

    batched = image.ndim == 4
    work_image = image if batched else image.unsqueeze(0)
    work_texture = texture if texture.ndim == 4 else texture.unsqueeze(0)

    if work_texture.shape[-2:] != work_image.shape[-2:]:
        work_texture = resize_texture(work_texture, work_image.shape[-2:])

    if mask.ndim == 2:
        work_mask = mask.unsqueeze(0).unsqueeze(0)
    elif mask.ndim == 3:
        work_mask = mask.unsqueeze(1) if batched else mask.unsqueeze(0)
    elif mask.ndim == 4:
        work_mask = mask
    else:
        raise ValueError("mask must have shape [H,W], [C,H,W], or [B,C,H,W]")

    work_mask = work_mask.to(dtype=work_image.dtype, device=work_image.device).clamp(0.0, 1.0)
    blend = (work_mask * alpha).clamp(0.0, 1.0)
    patched = work_image * (1.0 - blend) + work_texture.to(work_image.device) * blend
    return patched if batched else patched.squeeze(0)
