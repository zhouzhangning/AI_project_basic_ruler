# ZZN Skill Evolution Rules

Use this process when zzn asks to remember, evolve, or upgrade an experience.

## Trigger

Create or update a candidate when:

- zzn explicitly says to remember or沉淀 an experience
- the same AI mistake appears again
- zzn corrects the same workflow misunderstanding
- a repeated operation has a fixed safer process
- a lesson applies across projects

## Candidate First

Default destination is `references/experience-candidates.md`.

Do not write directly to `references/profile.md` unless zzn explicitly confirms upgrade.

## Frequency

- 1 occurrence: `候选`
- 2 occurrences: `高频候选`
- 3 or more occurrences and cross-project value: propose formal upgrade
- explicit user confirmation: `已升级`
- obsolete or wrong: `废弃`

## Upgrade Checklist

Before upgrading a candidate, answer:

```text
What repeated mistake does this prevent?
When exactly should it trigger?
Is it personal, project-specific, or global engineering?
Should it go to zzn-skill, engineering-standard, dce-generation, or project AGENTS.md?
Can it be checked by script?
Does it contain secrets or customer-private information?
```

## Placement

- Personal preference or environment: `zzn-skill/references/profile.md`
- Cross-project engineering rule: `engineering-standard`
- DCE business/document/release rule: `dce-generation` or DCE `AGENTS.md`
- One-off context: do not store in formal memory

## Cleanup

Candidates should stay concise. Merge duplicates. Do not keep long chat transcripts.
