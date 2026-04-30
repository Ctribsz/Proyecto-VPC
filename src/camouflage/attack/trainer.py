from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

from camouflage.config import load_config


@dataclass
class AttackTrainer:
    """Coordinates data loading, texture optimization, and artifact writing."""

    config: dict[str, Any]

    def run(self) -> None:
        raise NotImplementedError(
            "Connect the DOTA loader, victim model, overlay, EOT, and losses before running training."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train an adversarial camouflage texture.")
    parser.add_argument("--config", default=None, help="Path to a YAML config file.")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute training. Without this flag the command only validates the config.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    if not args.run:
        print(f"Loaded config for project: {config['project']['name']}")
        print("Training skeleton is ready. Pass --run after implementing AttackTrainer.run().")
        return 0

    AttackTrainer(config).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
