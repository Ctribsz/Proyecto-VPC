# Agent Guide

Guidelines for AI or human collaborators working in this repository.

## Rules

- Preserve the `src/` package layout.
- Keep raw data and generated results out of git.
- Prefer small, reviewable changes.
- Add tests or notebook evidence for behavior changes.
- Document experiment prompts and decisions under `docs/prompts/` when required.

## Common Tasks

- Config changes: edit `src/camouflage/config/default.yaml` or add a run-specific YAML file.
- New metric: add it to `src/camouflage/eval/metrics.py` and document it in `docs/EXPERIMENTS.md`.
- New transform: add it to `src/camouflage/attack/eot.py` and keep it differentiable when used during optimization.
- New artifact type: update `.gitignore` if it is generated or too large for git.
