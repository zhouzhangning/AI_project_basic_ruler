# ZZN Profile

This file contains zzn's stable personal working profile for AI-assisted development.

## Identity

- User identity phrase: `我是 zzn-skill`.
- Preferred language: Chinese.
- Preferred answer style: direct, concise, concrete, with files, commands, verification, and risks when relevant.
- Preferred work style: inspect current state first, then make scoped changes, then verify.

## Environment

- Primary OS: Windows.
- Primary shell: PowerShell.
- Common workspace root: `D:\test`.
- Personal AI infrastructure project: `D:\test\AI_project_basic_ruler`.
- DCE project: `D:\test\DCE_V1.1_clean`.
- Chinese paths and filenames are common.

## Encoding And File Reading

- PowerShell default output can display Chinese text as mojibake.
- Do not assume a file is corrupt only because terminal output is garbled.
- Prefer explicit UTF-8 reads for Chinese files:

```powershell
Get-Content -Encoding UTF8 <file>
```

- For scripted checks, prefer explicit `encoding="utf-8"`.
- If a file may be UTF-8 with BOM, use `utf-8-sig` fallback.

## Project Startup Preference

For any project development task:

1. Read this profile when `zzn-skill` is invoked.
2. Use `engineering-standard`.
3. Read the project's `AGENTS.md` if present.
4. Check git status before edits.
5. Use CodeGraph first when `.codegraph/` exists and code understanding is needed.
6. Use project-specific skills when applicable.

For DCE:

1. Use `engineering-standard`.
2. Use `dce-generation`.
3. Run DCE preflight when starting meaningful project work:

```powershell
python D:\test\DCE_V1.1_clean\tools\ai_project_preflight.py
```

## Long-Term Preferences

- Do not overwrite user changes.
- Do not modify unrelated files.
- Do not silently skip verification.
- Explain blockers plainly.
- Prefer scripts/checks for fragile repeated workflows.
- For release, packaging, deletion, overwrite, credentials, production, and external communication, be conservative and surface risk.

## Known Recurring Lessons

- Chinese terminal output乱码 usually needs encoding verification, not immediate file rewrites.
- DCE release workflows must protect old-version update baselines to avoid full-package fallback and Gitee 403.
- DCE generated artifacts need structural validation, not just "no exception".
- Personal/global rules should stay separate from project-specific rules.
