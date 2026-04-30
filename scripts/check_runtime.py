from __future__ import annotations

import importlib.metadata
import platform


def main() -> int:
    print(f"Python: {platform.python_version()}")

    try:
        import torch
    except ImportError:
        print("torch: not installed")
        return 1

    print(f"torch: {torch.__version__}")
    print(f"cuda available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        device_index = torch.cuda.current_device()
        print(f"cuda device: {torch.cuda.get_device_name(device_index)}")
        total_memory = torch.cuda.get_device_properties(device_index).total_memory / 1024**3
        print(f"cuda memory: {total_memory:.1f} GiB")
    else:
        print("cuda device: none")

    for package_name in ("ultralytics", "kornia", "albumentations", "camouflage"):
        try:
            version = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            version = "not installed"
        print(f"{package_name}: {version}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
