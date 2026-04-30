# Physical Protocol

## Scope

Physical experiments should be conducted only in authorized, controlled environments where all capture conditions and objects are permitted by the project supervisor.

## Calibration

1. Print the 16x16 color palette.
2. Photograph it under the planned lighting conditions.
3. Store calibration images in `data/calibration/`.
4. Use `camouflage.physical.calibration.build_printable_palette` to estimate printable colors.

## Capture Log

Record the following for every physical run:

- Camera model and lens.
- Height or distance from target.
- Lighting and weather.
- Print material and printer settings.
- Target dimensions and placement.
- Raw image path and processed output path.

## Outputs

Store physical metrics under `results/physical/` and selected figures under `figures/`.
