# Release And Sync Standard

This file defines cross-project release and synchronization expectations. Project-specific commands belong in project skills or `AGENTS.md`.

## Release Discipline

- Use official release scripts.
- Do not manually assemble production artifacts when a script exists.
- Validate version numbers in app metadata, package names, manifests, and release records.
- Validate every listed artifact exists and is downloadable or otherwise available through the intended channel.
- Preserve rollback path and record known risks.

## Incremental Update Baselines

If an updater supports incremental patches:

- every retained old version that may update directly should have a matching patch entry
- missing patch coverage must fail release validation when full-package fallback is unreliable
- large full-package fallback should be avoided on hosts that may return quota or 403 errors

## Cross-Project Synchronization

Keep one source of truth for global standards:

```text
AI_project_basic_ruler/
  skills/engineering-standard/
  prompts/
  docs/
  scripts/
```

Target projects should receive:

- lightweight `AGENTS.md` entry rules
- copied or installed skills when needed
- project-local scripts only when they enforce local behavior

Do not overwrite a target project's business rules during synchronization unless explicitly requested.
