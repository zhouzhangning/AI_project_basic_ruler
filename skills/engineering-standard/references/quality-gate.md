# Quality Gate

Quality gate means the work is not complete until the changed behavior is verified.

## Minimum Gate

- inspect current worktree before editing
- make a scoped change
- run the narrowest relevant check
- report changed files, verification, and residual risk

## Test Selection

- Parser/import/export: use fixture-based tests or a real sample file.
- UI display: instantiate relevant component or capture screenshot when practical.
- Generated Office files: inspect ZIP/XML/package structure and openpyxl/python-docx level properties.
- Build/release: run official scripts and validate manifests/artifacts.
- Shared library behavior: run unit tests plus one integration path.

## If Tests Cannot Run

State:

```text
Unable to run:
Reason:
Substitute verification:
Remaining risk:
```

Do not claim success only because code was edited.
