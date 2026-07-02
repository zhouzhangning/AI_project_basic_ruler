#!/usr/bin/env python
"""Report AI onboarding signals for a target project."""

from __future__ import annotations

import argparse
from pathlib import Path


ONBOARDING_FILES = [
    "AGENTS.md",
    "README-AI.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursorrules",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="?", default=".", help="Target project path")
    args = parser.parse_args()

    root = Path(args.project).resolve()
    print(f"Project: {root}")

    if not root.exists():
        print("ERROR: project path does not exist")
        return 2

    found = []
    missing = []
    for name in ONBOARDING_FILES:
        path = root / name
        if path.exists():
            found.append(name)
        else:
            missing.append(name)

    print("Found onboarding files:")
    for name in found:
        print(f"  - {name}")

    if missing:
        print("Missing optional onboarding files:")
        for name in missing:
            print(f"  - {name}")

    if (root / ".codegraph").exists():
        print("CodeGraph: .codegraph found; use CodeGraph before source grep/read.")
    else:
        print("CodeGraph: no .codegraph directory; skip CodeGraph unless user asks to initialize it.")

    print("Recommended first reads:")
    if "AGENTS.md" in found:
        print("  - AGENTS.md")
    if "README-AI.md" in found:
        print("  - README-AI.md")
    print("  - current task Spec or short plan")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
