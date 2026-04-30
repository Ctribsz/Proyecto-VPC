#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-data/raw/dota_v2}"

mkdir -p "${TARGET_DIR}"

cat <<'MSG'
DOTA-v2.0 download is not automated in this starter script because access and mirrors can change.

Manual steps:
1. Download DOTA-v2.0 images and labels from the official project page.
2. Extract them under data/raw/dota_v2/.
3. Keep the resulting raw data out of git.

Expected target directory:
MSG
printf '%s\n' "${TARGET_DIR}"
