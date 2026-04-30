from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def build_printable_palette(image_path: str | Path, grid_size: tuple[int, int] = (16, 16)) -> np.ndarray:
    """Average a photographed calibration grid into printable RGB colors in `[0, 1]`."""
    image = Image.open(image_path).convert("RGB")
    array = np.asarray(image, dtype=np.float32) / 255.0
    rows, cols = grid_size
    cell_h = array.shape[0] // rows
    cell_w = array.shape[1] // cols
    colors: list[np.ndarray] = []

    for row in range(rows):
        for col in range(cols):
            patch = array[row * cell_h : (row + 1) * cell_h, col * cell_w : (col + 1) * cell_w]
            colors.append(patch.reshape(-1, 3).mean(axis=0))

    return np.stack(colors, axis=0)
