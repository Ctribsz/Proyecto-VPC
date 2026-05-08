from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from camouflage.config import load_config

IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


@dataclass(frozen=True)
class BaselinePaths:
    image_dir: Path
    label_dir: Path
    zip_dir: Path
    output_dir: Path


def ensure_dir(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def write_json(payload: Any, path: str | Path, indent: int = 2) -> None:
    import json

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=indent) + "\n", encoding="utf-8")


def find_files(root: Path, extensions: set[str]) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in extensions
    )


def resolve_paths(config: dict[str, Any], args: argparse.Namespace) -> BaselinePaths:
    paths_cfg = config.get("paths", {})
    baseline_cfg = config.get("baseline", {})
    dota_root = Path(paths_cfg.get("dota_root", "data/raw/dota_v1"))
    results_root = Path(paths_cfg.get("results_root", "results"))

    return BaselinePaths(
        image_dir=Path(args.image_dir or baseline_cfg.get("image_dir") or dota_root / "images"),
        label_dir=Path(args.label_dir or baseline_cfg.get("label_dir") or dota_root / "labels"),
        zip_dir=Path(args.zip_dir or baseline_cfg.get("zip_dir") or dota_root / "zips"),
        output_dir=Path(
            args.output_dir
            or baseline_cfg.get("output_dir")
            or results_root / "digital" / "baseline_yolo_obb"
        ),
    )


def select_images(images: list[Path], max_images: int) -> list[Path]:
    if max_images <= 0:
        return images
    return images[:max_images]


def normalize_yolo_device(device: Any) -> Any:
    if device is None:
        return None

    device_name = str(device).strip().lower()
    if device_name in {"cuda", "cuda:0"}:
        return "0"
    return device


def print_dataset_summary(paths: BaselinePaths, images: list[Path], selected: list[Path]) -> None:
    labels = find_files(paths.label_dir, {".txt"})
    archives = find_files(paths.zip_dir, {".zip"})

    print(f"Image dir: {paths.image_dir}")
    print(f"Label dir: {paths.label_dir}")
    print(f"Zip dir: {paths.zip_dir}")
    print(f"Output dir: {paths.output_dir}")
    print(f"Images found: {len(images)}")
    print(f"Labels found: {len(labels)}")
    print(f"Zip archives found: {len(archives)}")
    print(f"Images selected for baseline: {len(selected)}")

    for image_path in selected[:5]:
        print(f"Sample image: {image_path}")


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []

    detach = getattr(value, "detach", None)
    if callable(detach):
        value = detach()

    cpu = getattr(value, "cpu", None)
    if callable(cpu):
        value = cpu()

    tolist = getattr(value, "tolist", None)
    if callable(tolist):
        result = tolist()
        return result if isinstance(result, list) else [result]

    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, list):
        return value
    return [value]


def item_at(values: list[Any], index: int) -> Any | None:
    return values[index] if index < len(values) else None


def class_name(names: Any, class_id: int) -> str:
    if isinstance(names, dict):
        return str(names.get(class_id) or names.get(str(class_id)) or class_id)
    if isinstance(names, list) and 0 <= class_id < len(names):
        return str(names[class_id])
    return str(class_id)


def extract_obb_detections(result: Any) -> list[dict[str, Any]]:
    names = getattr(result, "names", {}) or {}
    obb = getattr(result, "obb", None)
    if obb is None:
        return []

    classes = to_list(getattr(obb, "cls", None))
    confidences = to_list(getattr(obb, "conf", None))
    polygons = to_list(getattr(obb, "xyxyxyxy", None))
    xywhr = to_list(getattr(obb, "xywhr", None))

    detections: list[dict[str, Any]] = []
    for index, raw_class_id in enumerate(classes):
        class_id = int(float(raw_class_id))
        confidence = item_at(confidences, index)
        detections.append(
            {
                "type": "obb",
                "class_id": class_id,
                "class_name": class_name(names, class_id),
                "confidence": None if confidence is None else float(confidence),
                "polygon": item_at(polygons, index),
                "xywhr": item_at(xywhr, index),
            }
        )
    return detections


def extract_box_detections(result: Any) -> list[dict[str, Any]]:
    names = getattr(result, "names", {}) or {}
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return []

    classes = to_list(getattr(boxes, "cls", None))
    confidences = to_list(getattr(boxes, "conf", None))
    xyxy = to_list(getattr(boxes, "xyxy", None))

    detections: list[dict[str, Any]] = []
    for index, raw_class_id in enumerate(classes):
        class_id = int(float(raw_class_id))
        confidence = item_at(confidences, index)
        detections.append(
            {
                "type": "xyxy",
                "class_id": class_id,
                "class_name": class_name(names, class_id),
                "confidence": None if confidence is None else float(confidence),
                "xyxy": item_at(xyxy, index),
            }
        )
    return detections


def extract_detections(result: Any) -> list[dict[str, Any]]:
    obb_detections = extract_obb_detections(result)
    return obb_detections if obb_detections else extract_box_detections(result)


def run_baseline(
    config: dict[str, Any],
    paths: BaselinePaths,
    image_paths: list[Path],
    args: argparse.Namespace,
) -> int:
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise ImportError("Install ultralytics before running the YOLO baseline.") from exc

    model_cfg = config.get("model", {})
    data_cfg = config.get("data", {})
    project_cfg = config.get("project", {})
    baseline_cfg = config.get("baseline", {})

    weights = args.weights or model_cfg.get("weights", "yolov8n-obb.pt")
    task = model_cfg.get("task", "obb")
    conf = args.conf if args.conf is not None else model_cfg.get("conf_threshold", 0.25)
    iou = args.iou if args.iou is not None else model_cfg.get("iou_threshold", 0.7)
    device = normalize_yolo_device(args.device or project_cfg.get("device"))
    image_size = args.imgsz or baseline_cfg.get("image_size") or data_cfg.get("image_size", 1024)

    ensure_dir(paths.output_dir)
    plots_dir = ensure_dir(paths.output_dir / "plots")

    print(f"Loading YOLO model: {weights}")
    model = YOLO(weights, task=task)

    records: list[dict[str, Any]] = []
    for image_path in image_paths:
        print(f"Running baseline: {image_path}")
        results = model.predict(
            source=str(image_path),
            conf=conf,
            iou=iou,
            device=device,
            imgsz=image_size,
            verbose=False,
        )
        if not results:
            continue

        result = results[0]
        plot_path = plots_dir / f"{image_path.stem}_baseline.jpg"
        if not args.no_save_plots:
            result.save(filename=str(plot_path))

        detections = extract_detections(result)
        records.append(
            {
                "image_path": str(image_path),
                "plot_path": None if args.no_save_plots else str(plot_path),
                "detections": detections,
            }
        )

    payload = {
        "model": str(weights),
        "task": str(task),
        "confidence_threshold": float(conf),
        "iou_threshold": float(iou),
        "device": None if device is None else str(device),
        "image_size": int(image_size),
        "image_dir": str(paths.image_dir),
        "output_dir": str(paths.output_dir),
        "images_evaluated": len(records),
        "detections_total": sum(len(record["detections"]) for record in records),
        "records": records,
    }
    predictions_path = paths.output_dir / "predictions.json"
    write_json(payload, predictions_path)
    print(f"Saved predictions: {predictions_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a YOLOv8 OBB baseline on clean images.")
    parser.add_argument("--config", default="src/camouflage/config/colab.yaml")
    parser.add_argument("--image-dir", default=None)
    parser.add_argument("--label-dir", default=None)
    parser.add_argument("--zip-dir", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--weights", default=None)
    parser.add_argument("--device", default=None)
    parser.add_argument("--imgsz", type=int, default=None)
    parser.add_argument("--conf", type=float, default=None)
    parser.add_argument("--iou", type=float, default=None)
    parser.add_argument("--max-images", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-save-plots", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    baseline_cfg = config.get("baseline", {})
    max_images = args.max_images
    if max_images is None:
        max_images = int(baseline_cfg.get("max_images", 20))

    paths = resolve_paths(config, args)
    images = find_files(paths.image_dir, IMAGE_EXTENSIONS)
    selected = select_images(images, max_images)
    print_dataset_summary(paths, images, selected)

    if args.dry_run:
        return 0

    if not selected:
        print("No images found. Upload and extract DOTA images before running the baseline.")
        return 1

    return run_baseline(config, paths, selected, args)


if __name__ == "__main__":
    raise SystemExit(main())
