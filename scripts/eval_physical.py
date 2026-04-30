from __future__ import annotations

import sys

from camouflage.eval.runner import main


if __name__ == "__main__":
    raise SystemExit(main(["--mode", "physical", *sys.argv[1:]]))
