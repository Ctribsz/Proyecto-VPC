from __future__ import annotations

import argparse
from typing import Any

from camouflage.config import load_config


class EvaluationRunner:
    """Runs digital or physical evaluation using generated predictions."""

    def __init__(self, config: dict[str, Any], mode: str = "digital") -> None:
        self.config = config
        self.mode = mode

    def run(self) -> None:
        raise NotImplementedError("Connect prediction loading and metric aggregation here.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate camouflage experiments.")
    parser.add_argument("--config", default=None, help="Path to a YAML config file.")
    parser.add_argument("--mode", choices=["digital", "physical"], default="digital")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute evaluation. Without this flag the command only validates the config.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    if not args.run:
        print(f"Loaded config for {args.mode} evaluation: {config['project']['name']}")
        print("Evaluation skeleton is ready. Pass --run after implementing EvaluationRunner.run().")
        return 0

    EvaluationRunner(config, mode=args.mode).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
