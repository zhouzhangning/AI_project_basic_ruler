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

## Approval

AI may propose global rule changes, but should not silently add them during unrelated feature work. Global rules need explicit user confirmation or a direct task to update the standard.
