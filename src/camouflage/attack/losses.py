from __future__ import annotations

import torch


def detection_confidence_loss(confidences: torch.Tensor) -> torch.Tensor:
    """Loss for reducing detector confidence on selected targets."""
    if confidences.numel() == 0:
        return torch.zeros((), device=confidences.device, dtype=confidences.dtype)
    return confidences.mean()


def total_variation_loss(texture: torch.Tensor) -> torch.Tensor:
    """Penalize high-frequency texture changes."""
    horizontal = torch.abs(texture[..., :, 1:] - texture[..., :, :-1]).mean()
    vertical = torch.abs(texture[..., 1:, :] - texture[..., :-1, :]).mean()
    return horizontal + vertical


def non_printability_score(texture: torch.Tensor, printable_colors: torch.Tensor) -> torch.Tensor:
    """Distance from each texture pixel to the nearest printable RGB color."""
    if texture.ndim == 3:
        work_texture = texture.unsqueeze(0)
    elif texture.ndim == 4:
        work_texture = texture
    else:
        raise ValueError("texture must have shape [C,H,W] or [B,C,H,W]")

    if printable_colors.ndim != 2 or printable_colors.shape[1] != 3:
        raise ValueError("printable_colors must have shape [N,3]")

    palette = printable_colors.to(device=work_texture.device, dtype=work_texture.dtype)
    diff = work_texture.unsqueeze(-1) - palette.T.view(1, 3, 1, 1, -1)
    distances = torch.linalg.vector_norm(diff, dim=1)
    return distances.min(dim=-1).values.mean()


def naturalness_loss(
    texture: torch.Tensor,
    target_mean: tuple[float, float, float] = (0.45, 0.45, 0.40),
    target_std: tuple[float, float, float] = (0.20, 0.20, 0.18),
) -> torch.Tensor:
    """Simple color-statistics regularizer for natural-looking patches."""
    work = texture if texture.ndim == 4 else texture.unsqueeze(0)
    mean = work.mean(dim=(-2, -1))
    std = work.std(dim=(-2, -1))
    ref_mean = torch.tensor(target_mean, device=work.device, dtype=work.dtype)
    ref_std = torch.tensor(target_std, device=work.device, dtype=work.dtype)
    return (mean - ref_mean).pow(2).mean() + (std - ref_std).pow(2).mean()
