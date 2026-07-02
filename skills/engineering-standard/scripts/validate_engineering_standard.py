#!/usr/bin/env python
"""Validate engineering-standard structure and rule hygiene."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATUSES = {"候选", "高频候选", "已升级", "废弃"}
MAX_SKILL_LINES = 180
MAX_REFERENCE_LINES = 220


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_count(path: Path) -> int:
    return len(read_text(path).splitlines())


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        ROOT / "SKILL.md",
        ROOT / "agents" / "openai.yaml",
        ROOT / "references" / "spec-first.md",
        ROOT / "references" / "quality-gate.md",
        ROOT / "references" / "skill-layering.md",
        ROOT / "references" / "rule-evolution.md",
        ROOT / "references" / "release-and-sync.md",
        ROOT / "references" / "evolution-candidates.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    skill = ROOT / "SKILL.md"
    if skill.is_file():
        text = read_text(skill)
        required_phrases = [
            "name: engineering-standard",
            "Spec",
            "quality",
            "evolution-candidates.md",
            "validate_engineering_standard.py",
        ]
        for phrase in required_phrases:
            if phrase not in text:
                errors.append(f"SKILL.md missing required phrase: {phrase}")
        if line_count(skill) > MAX_SKILL_LINES:
            warnings.append(f"SKILL.md has more than {MAX_SKILL_LINES} lines")

    candidates = ROOT / "references" / "evolution-candidates.md"
    if candidates.is_file():
        text = read_text(candidates)
        statuses = re.findall(r"^状态：(.+)$", text, flags=re.MULTILINE)
        if not statuses:
            errors.append("evolution-candidates.md has no candidate statuses")
        for status in statuses:
            if status.strip() not in ALLOWED_STATUSES:
                errors.append(f"Invalid candidate status: {status}")
        project_specific_terms = ["报价模块", "FAR", "NAT6602"]
        for term in project_specific_terms:
            if term in text:
                warnings.append(f"Candidate pool mentions project-specific term: {term}; verify it is only source context, not formal global rule")

    evolution = ROOT / "references" / "rule-evolution.md"
    if evolution.is_file():
        evolution_text = read_text(evolution)
        for phrase in [
            "D:\\test\\AI_project_basic_ruler\\skills\\engineering-standard",
            "C:\\Users\\HUAWEI\\.codex\\skills\\engineering-standard",
            "install-local-skills.ps1",
        ]:
            if phrase not in evolution_text:
                errors.append(f"rule-evolution.md missing source-of-truth phrase: {phrase}")

    references_dir = ROOT / "references"
    if references_dir.is_dir():
        for path in references_dir.glob("*.md"):
            if line_count(path) > MAX_REFERENCE_LINES:
                warnings.append(f"{path.relative_to(ROOT)} has more than {MAX_REFERENCE_LINES} lines")

    print("engineering-standard validation")
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
