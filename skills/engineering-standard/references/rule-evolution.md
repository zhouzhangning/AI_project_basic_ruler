# Rule Evolution

Rules should reduce repeated mistakes without making normal work heavy.

## Intake

Before adding a rule, answer:

```text
What error does this prevent?
When does it trigger?
Is it global, project-specific, or temporary?
Should it be a rule, prompt, checklist, script, or project memory?
Can it be checked automatically?
What complexity does it add?
```

## Decision

- One-off issue: work log only.
- Repeated in one project: project memory or project skill.
- Repeated across projects: candidate for `engineering-standard`.
- Risky manual sequence: script it.
- Long explanation: move to references, keep `SKILL.md` concise.

## Candidate Pool

Use `references/evolution-candidates.md` before formalizing new engineering rules.

Allowed statuses:

- `候选`
- `高频候选`
- `已升级`
- `废弃`

Useful command phrases:

- `沉淀到工程规范候选`
- `查看工程规范候选`
- `确认升级工程规范第 N 条`
- `从 <skill-name> 提炼可复用规则`

## Approval

AI may propose global rule changes, but should not silently add them during unrelated feature work. Global rules need explicit user confirmation or a direct task to update the standard.

After upgrading a candidate, run `scripts/validate_engineering_standard.py`.

## Source Of Truth

Formal upgrades to `engineering-standard` must be written to the infrastructure repository first:

```text
D:\test\AI_project_basic_ruler\skills\engineering-standard
```

Do not treat `C:\Users\HUAWEI\.codex\skills\engineering-standard` as the long-term maintenance source. It is an installed runtime copy and may be overwritten by `scripts\install-local-skills.ps1`.

After any formal upgrade:

1. Modify the source skill under `D:\test\AI_project_basic_ruler\skills\engineering-standard`.
2. Run `scripts\validate_engineering_standard.py`.
3. Commit the change in `D:\test\AI_project_basic_ruler`.
4. Run `scripts\install-local-skills.ps1` to refresh the installed Codex skill.
