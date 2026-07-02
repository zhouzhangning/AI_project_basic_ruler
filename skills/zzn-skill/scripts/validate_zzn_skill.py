#!/usr/bin/env python
"""Validate zzn-skill structure and memory hygiene."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATUSES = {"候选", "高频候选", "已升级", "废弃"}
MAX_SKILL_LINES = 180
MAX_PROFILE_LINES = 220


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def count_lines(path: Path) -> int:
    return len(read_text(path).splitlines())


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        ROOT / "SKILL.md",
        ROOT / "agents" / "openai.yaml",
        ROOT / "references" / "profile.md",
        ROOT / "references" / "experience-candidates.md",
        ROOT / "references" / "evolution-rules.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        text = read_text(skill)
        if "name: zzn-skill" not in text:
            errors.append("SKILL.md frontmatter must contain name: zzn-skill")
        if "engineering-standard" not in text:
            errors.append("SKILL.md must dispatch project work to engineering-standard")
        if count_lines(skill) > MAX_SKILL_LINES:
            warnings.append(f"SKILL.md has more than {MAX_SKILL_LINES} lines")

    profile = ROOT / "references" / "profile.md"
    if profile.is_file():
        profile_text = read_text(profile)
        for required_phrase in ["PowerShell", "engineering-standard", "DCE", "Get-Content -Encoding UTF8"]:
            if required_phrase not in profile_text:
                warnings.append(f"profile.md may be missing: {required_phrase}")
        if count_lines(profile) > MAX_PROFILE_LINES:
            warnings.append(f"profile.md has more than {MAX_PROFILE_LINES} lines")
        secret_words = ["API Key", "password", "token", "密钥"]
        if any(word.lower() in profile_text.lower() for word in secret_words):
            warnings.append("profile.md mentions secret-like terms; ensure no actual secrets are stored")

    candidates = ROOT / "references" / "experience-candidates.md"
    if candidates.is_file():
        candidate_text = read_text(candidates)
        statuses = re.findall(r"^状态：(.+)$", candidate_text, flags=re.MULTILINE)
        if not statuses:
            errors.append("experience-candidates.md has no candidate statuses")
        for status in statuses:
            if status.strip() not in ALLOWED_STATUSES:
                errors.append(f"Invalid candidate status: {status}")

    print("zzn-skill validation")
    print(f"Root: {ROOT}")

    if warnings:
        print("Warnings:")
        for item in warnings:
            print(f"  - {item}")

    if errors:
        print("Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
