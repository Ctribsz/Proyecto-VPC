# Architecture

## Goal

Create a reproducible research pipeline for aerial object detection experiments with digital and physical evaluation stages.

## Main Components

- `camouflage.data`: DOTA labels, oriented boxes, and cached preprocessing.
- `camouflage.models`: victim detector wrappers and prediction normalization.
- `camouflage.attack`: texture parameters, overlays, EoT transforms, losses, and optimization loop.
- `camouflage.physical`: printable palette calibration and physical degradation proxies.
- `camouflage.eval`: metrics and evaluation runners for digital and physical experiments.
- `camouflage.utils`: shared IO, seeding, and visualization helpers.

## Data Flow

1. Parse DOTA labels and select target classes.
2. Generate or load cached OBB crops and masks.
3. Overlay the current texture on target objects.
4. Apply EoT transformations for robustness.
5. Query the victim model and compute losses.
6. Save textures, metrics, figures, and experiment metadata.

## Reproducibility

Record the config file, seed, package version, model weights, dataset split, and output paths for each run.
