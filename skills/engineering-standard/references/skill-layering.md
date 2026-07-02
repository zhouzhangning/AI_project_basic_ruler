# Skill Layering

Use layered skills so one global standard can improve every project without absorbing project-specific knowledge.

## Layers

```text
Global engineering skill
  engineering-standard
  Cross-project workflow, quality, Spec, release discipline, sync rules.

Project/domain skill
  dce-generation, crm-generation, mes-generation, etc.
  Domain files, business rules, local commands, known pitfalls.

Project entry file
  AGENTS.md
  Which skills to use, local constraints, repo commands, special approvals.
```

## DCE Example

For DCE work:

1. Use `engineering-standard` to decide Spec, scope, quality gate, release safety, and logging.
2. Use `dce-generation` for Excel, Word, FAR, sales quotation, templates, preview/export consistency, and DCE release commands.
3. Use DCE `AGENTS.md` for local repository rules and current project constraints.

`engineering-standard` must not replace `dce-generation`; it governs how `dce-generation` is applied.

## Promotion Rule

Promote a rule upward only when it is reusable:

- DCE-only issue: keep in `dce-generation`.
- One project's local constraint: keep in that project's `AGENTS.md`.
- Cross-project engineering behavior: move to `engineering-standard`.
- Repeated deterministic check: make it a script.
