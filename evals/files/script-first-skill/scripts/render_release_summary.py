#!/usr/bin/env python3
"""Eval fixture helper that renders a release summary from stable inputs."""

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    output = root / "dist" / "release-summary.md"
    output.parent.mkdir(exist_ok=True)
    output.write_text("# Release Summary\n\nRendered by script.\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
