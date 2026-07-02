---
name: engineering-standard
description: Unified engineering workflow standard for AI-assisted software development across projects. Use when Codex starts work in any repository, writes or changes code, handles bugs/features/refactors, prepares release/build work, creates or updates project rules, or needs to enforce Spec-first, reusable skills, quality gates, traceable change logs, and cross-project synchronization. Pair this with project-specific skills such as dce-generation instead of replacing them.
---

# Engineering Standard

Use this skill as the top-level project engineering discipline. It defines how AI should enter a project, turn requests into executable work, validate changes, and evolve reusable rules.

Project-specific skills remain responsible for domain behavior. For DCE work, use this skill first for workflow discipline, then use `dce-generation` for Excel/Word/FAR/quotation/release details.

## Operating Model

```text
engineering-standard
  Controls: Spec-first, scope, risk, quality gates, logs, release discipline, rule evolution.

project-specific skill
  Controls: project domain knowledge, file formats, business rules, local commands.

project AGENTS.md
  Controls: local entry rules, project-specific constraints, required skill pairing.
```

## First Moves

1. Read the target project's `AGENTS.md`, `README-AI.md`, or equivalent onboarding files.
2. Inspect worktree status before editing; do not overwrite user changes.
3. If the repository has `.codegraph/`, use CodeGraph before grep/read for code understanding.
4. Identify whether the task needs a written Spec. Use `references/spec-first.md` for non-trivial changes.
5. Identify project-specific skills required by the task. For DCE document/table/release work, use `dce-generation`.
6. Define verification before editing: unit test, integration test, build, release validation, or manual artifact check.

## Spec-First Rule

Use a Spec before implementation when any of these are true:

- new feature or behavior change
- release/build/update workflow change
- data migration, file format, import/export, parser, security, permission, payment, customer data, or rollback-sensitive work
- unclear requirement with multiple valid interpretations
- change spans more than one module or public interface

For small mechanical fixes, a short inline plan is enough. Do not create process overhead for trivial edits.

Read `references/spec-first.md` when writing or reviewing a Spec.

## Quality Gate

Before final response, verify the changed surface:

- run the narrowest relevant test or build command
- compile/lint changed Python/TypeScript/etc. when no focused tests exist
- validate generated artifacts structurally when file generation is involved
- explain any test that could not be run and the substitute check used
- list remaining risk if coverage is partial

Read `references/quality-gate.md` for the standard checklist.

## Reusable Skill Layering

Do not merge project business knowledge into this skill.

- Put cross-project engineering rules here.
- Put DCE-specific Excel/Word/FAR/quotation/release knowledge in `dce-generation`.
- Put another project's business rules in that project's own skill.
- Put only local entry and special constraints in the project's `AGENTS.md`.

Read `references/skill-layering.md` before creating or reorganizing skills.

## Rule Evolution

Do not add rules just because one task failed once.

1. One occurrence: record in project work log.
2. Two occurrences: consider project memory.
3. Three or more occurrences across projects: propose adding to this standard.
4. Human confirmation is required before turning experience into a global rule.
5. If a rule can be automatically checked, prefer a script.

Read `references/rule-evolution.md` before changing this skill or shared templates.

## Release And Sync

For any project that publishes packages or update manifests:

- release must be script-driven, not manually assembled
- each retained upgrade baseline needs a direct patch path when the updater cannot safely fall back to full packages
- manifests and published files must be validated before release is called complete
- release records must include version, artifacts, tests, known risks, and rollback notes

Read `references/release-and-sync.md` for release and cross-project synchronization rules.

## Scripts

- `scripts/ai_preflight.py`: checks whether a target project has basic AI onboarding files and reports recommended reads.
- `scripts/validate_project_rules.py`: checks whether a target project declares engineering-standard layering and avoids mixing project-specific rules into the global layer.

These scripts are helpers, not substitutes for reading the project.
