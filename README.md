# Adversarial Camouflage Aerial

Starter repository for a computer vision research project on adversarial camouflage for aerial object detection. The codebase uses a `src/` Python package layout and is organized around DOTA-style oriented bounding boxes, a YOLOv8 victim model wrapper, digital/physical evaluation, and experiment documentation.

This repository is intended for authorized, reproducible research in controlled settings.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For a runtime-only install without notebook and lint tooling, use `pip install -e .` instead.

Validate the package import:

```bash
python -c "import camouflage; print(camouflage.__version__)"
```

Run the current CLI dry runs:

```bash
python scripts/train_attack.py --config src/camouflage/config/default.yaml
python scripts/eval_digital.py --config src/camouflage/config/default.yaml
python scripts/eval_physical.py --config src/camouflage/config/default.yaml
```

## Layout

```text
src/camouflage/      Importable Python package
experiments/         Numbered notebooks
scripts/             CLI entrypoints
data/                Local datasets and caches, ignored by git
patches/             Generated textures selected for versioning
results/             Generated evaluation outputs, ignored by git
figures/             Paper and report figures
docs/                Architecture, experiment log, physical protocol
paper/               LaTeX manuscript skeleton
```

## Data

Place DOTA-v2.0 files under `data/raw/dota_v2/`. Keep raw data, caches, and generated results out of git. The `.gitkeep` files only preserve the directory structure.

## Configuration

The default configuration lives at `src/camouflage/config/default.yaml`. Use `.env` for local paths or credentials; start from `.env.example` and never commit real secrets.

## Development Notes

- Keep experiments reproducible by recording config files, git commit hashes, and random seeds.
- Store prompts or agent interaction logs under `docs/prompts/` if required by the course.
- Keep generated heavy artifacts in `data/`, `results/`, or external storage.
