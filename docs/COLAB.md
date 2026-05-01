# Google Colab Setup

This project is better suited to Colab or another CUDA machine than to a weak local GPU. The default config already targets `cuda`; this guide adds the Colab-specific paths and setup commands.

## Runtime

In Colab, use:

```text
Runtime > Change runtime type > Hardware accelerator > GPU
```

Then verify the GPU:

```bash
!nvidia-smi
```

## Install

Clone the repo and install it in editable mode:

```bash
!git clone git@github.com:Ctribsz/Proyecto-VPC.git
%cd Proyecto-VPC
!pip install -r requirements.txt
```

If SSH is not configured in Colab, use HTTPS instead:

```bash
!git clone https://github.com/Ctribsz/Proyecto-VPC.git
%cd Proyecto-VPC
!pip install -r requirements.txt
```

## Drive Storage

Mount Google Drive for datasets and generated outputs:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Create the expected folders:

```bash
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/data/raw/dota_v1/zips
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/data/raw/dota_v1/images
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/data/raw/dota_v1/labels
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/data/processed
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/data/calibration
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/results/digital
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/patches
!mkdir -p /content/drive/MyDrive/Proyecto-VPC/figures
```

The initial committed dataset artifact is the DOTA v1.0 label archive at:

```text
data/raw/dota_v1/labelTxt-v1.0-20260501T040720Z-3-001.zip
```

The corresponding DOTA image archives are intentionally stored outside Git because they are several GB. Upload them to Drive under:

```text
/content/drive/MyDrive/Proyecto-VPC/data/raw/dota_v1/zips/
```

After extraction, keep the dataset under:

```text
/content/drive/MyDrive/Proyecto-VPC/data/raw/dota_v1/images/
/content/drive/MyDrive/Proyecto-VPC/data/raw/dota_v1/labels/
```

## Verify Environment

Run the runtime check:

```bash
!python scripts/check_runtime.py
```

Validate the Colab config:

```bash
!python scripts/train_attack.py --config src/camouflage/config/colab.yaml
!python scripts/eval_digital.py --config src/camouflage/config/colab.yaml
!python scripts/eval_physical.py --config src/camouflage/config/colab.yaml
```

## Current Limitation

The repository is currently a scaffold. `AttackTrainer.run()` still raises `NotImplementedError`, so full adversarial training will not run until the DOTA loader, YOLO victim model, overlay, EOT transforms, and losses are connected in the trainer.

What Colab can do now:

- Install the package and dependencies.
- Verify CUDA/GPU availability.
- Download YOLO OBB weights through Ultralytics when inference code is used.
- Validate configs and script entrypoints.
- Store DOTA v1 image archives, extracted data, and outputs on Google Drive.

What still needs implementation:

- Real training loop in `src/camouflage/attack/trainer.py`.
- Dataset batching from DOTA samples.
- Differentiable connection between overlay, EOT, victim detections, and losses.
- Saving trained textures and experiment metrics.
