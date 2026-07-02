#!/usr/bin/env python
"""Lightweight validation for engineering-standard adoption in a project."""

from __future__ import annotations

import argparse
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="?", default=".", help="Target project path")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    agents = root / "AGENTS.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not agents.exists():
        errors.append("Missing AGENTS.md")
    else:
        text = read_text(agents)
        if "engineering-standard" not in text:
            warnings.append("AGENTS.md does not mention engineering-standard")
        if "dce-generation" in text and "engineering-standard" not in text:
            errors.append("Project-specific skill is declared without engineering-standard")

    if (root / "skills" / "engineering-standard").exists():
        warnings.append("Project contains a local copy of engineering-standard; ensure it is synced from the infrastructure repository.")

    if errors:
        print("ERRORS:")
        for item in errors:
            print(f"  - {item}")
    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"  - {item}")
    if not errors and not warnings:
        print("Project rule validation passed.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
