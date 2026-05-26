# Experiments

Use this file as the experiment log. Keep entries short and link to configs, notebooks, results, and figures.

## Template

```text
Date:
Owner:
Notebook or script:
Config:
Dataset split:
Victim model:
Patch artifact:
Metrics:
Notes:
```

## Initial Plan

1. Baseline YOLOv8 detections on selected DOTA classes.
2. Overlay sanity check on OBB crops.
3. Digital optimization without EoT.
4. Digital optimization with EoT.
5. Physical calibration and controlled capture.

## 2026-05-25 - YOLOv8-OBB clean baseline

Date: 2026-05-25
Owner: Proyecto VPC
Notebook or script: `experiments/Proyecto_VPC_Colab.ipynb`, `scripts/run_yolo_baseline.py`
Config: `src/camouflage/config/colab.yaml`
Dataset split: DOTA v1.0 images from Google Drive
Victim model: `yolov8n-obb.pt`
Patch artifact: none
Metrics: clean detections exported to `results/digital/baseline_yolo_obb/predictions.json`
Notes: Baseline confirmed that YOLOv8-OBB detects DOTA objects before any camouflage or adversarial texture is applied.

## 2026-05-25 - Fixed texture sanity checks

Date: 2026-05-25
Owner: Proyecto VPC
Notebook or script: Colab exploratory cells
Config: manual texture settings
Dataset split: selected DOTA v1.0 images
Victim model: `yolov8n-obb.pt`
Patch artifact: fixed checkerboard, random noise, camouflage-like, diagonal stripe, and gray textures
Metrics: detections before/after texture placement on selected object regions
Notes: Fixed textures validated the object-local overlay and evaluation pipeline, but they are not a true adversarial attack because the texture is not optimized against the detector.

## 2026-05-25 - Differentiable adversarial texture, one object

Date: 2026-05-25
Owner: Proyecto VPC
Notebook or script: `experiments/Ataque_Adversarial.ipynb`
Config: Adam optimizer, learning rate 0.10, 500 iterations, no EoT, no TV regularization
Dataset split: selected DOTA v1.0 image/object
Victim model: `yolov8n-obb.pt`
Patch artifact: `results/digital/adversarial_gradient/texture_one_object.png`
Metrics: local detections inside target bbox changed from 3 `large vehicle` detections to 0 detections
Notes: The texture is represented by `theta.requires_grad=True`, mapped through sigmoid, applied with differentiable torch/kornia operations, and optimized against the maximum target-class confidence inside the object region.

## 2026-05-25 - Preliminary multi-object transfer

Date: 2026-05-25
Owner: Proyecto VPC
Notebook or script: `experiments/Ataque_Adversarial.ipynb`
Config: universal texture evaluation on multiple object regions
Dataset split: 20 selected DOTA vehicle objects, mostly from one image
Victim model: `yolov8n-obb.pt`
Patch artifact: adversarial texture from gradient optimization
Metrics: 19/20 local successes; one failure still reduced confidence from about 0.82 to about 0.38
Notes: This supports intra-image transfer, but should not yet be reported as universal multi-image robustness. Next evaluation should cap objects per image, for example `MAX_OBJECTS_PER_IMAGE = 8`, and report image-level success rates.
