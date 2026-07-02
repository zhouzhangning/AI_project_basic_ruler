---
name: zzn-skill
description: Personal identity and working profile for user zzn. Use when the user says "我是 zzn-skill", "我是zzn-skill", asks Codex to remember personal working preferences, starts a new AI session that should know zzn's environment, or wants to evolve recurring lessons into durable AI behavior. Load this before project-specific work, then dispatch to engineering-standard and project skills such as dce-generation.
---

# ZZN Skill

Use this skill as zzn's personal AI working identity. It tells Codex who it is working with, what environment and preferences to assume, how to start project work, and how to evolve recurring lessons without turning memory into clutter.

## Startup Flow

When this skill is invoked:

1. Read `references/profile.md`.
2. For project development, use `engineering-standard` next.
3. If the target project has `AGENTS.md`, read it before editing.
4. If the target project is DCE or the task involves DCE documents, quotations, FAR, Office files, preview/export, packaging, or updates, use `dce-generation`.
5. If the target project has `.codegraph/`, use CodeGraph before grep/read for complex code understanding.
6. Do not claim to remember details that are not in this skill, project files, or the current conversation.

## Memory Boundaries

Store only long-lived, cross-session personal working knowledge here:

- environment facts
- repeated personal preferences
- recurring AI failure modes
- common project entry paths
- cross-project workflow habits
- stable safety boundaries

Do not store:

- one-off chat history
- customer-private details
- full bug narratives
- DCE-only implementation rules
- temporary task state
- secrets, tokens, passwords, or private credentials

## Evolution Mechanism

Do not silently add formal memory.

Use `references/experience-candidates.md` as the candidate pool. Trigger candidate capture when zzn says phrases like:

- "沉淀这个经验"
- "这个规则记住"
- "以后都要这样"
- "这个之前说过"
- "又犯同样错误"
- "查看 zzn 候选经验"
- "确认升级第 N 条"

Default action:

1. Add repeated or requested lessons to candidate memory, not formal profile.
2. Mark candidates as `候选`, `高频候选`, `已升级`, or `废弃`.
3. Upgrade only after explicit user confirmation.
4. After upgrading, run `scripts/validate_zzn_skill.py`.

Read `references/evolution-rules.md` before changing profile or candidates.

## Command Phrases

- `我是 zzn-skill`: load this identity, read profile, then continue with the requested task.
- `沉淀这个经验`: add a structured candidate to `experience-candidates.md`.
- `查看 zzn 候选经验`: summarize candidates, ordered by value and frequency.
- `确认升级第 N 条`: move the selected candidate into `profile.md` or `SKILL.md` after checking scope.
- `清理 zzn 经验`: propose stale or duplicated candidates for removal; do not delete without confirmation.

## Scripts

- `scripts/validate_zzn_skill.py`: checks basic structure, required sections, candidate statuses, and likely scope mistakes.

## Pairing

This skill should coordinate with, not replace, other skills:

```text
zzn-skill
  Personal identity, environment, preferences, memory evolution.

engineering-standard
  Cross-project engineering workflow.

dce-generation
  DCE-specific business and document generation workflow.
```
