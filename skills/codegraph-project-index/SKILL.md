---
name: codegraph-project-index
description: Locator skill for CodeGraph project indexing and AI codebase onboarding. Use when the user asks for a skill/tool that helps AI read or understand a project, build a local code knowledge graph, inspect call relationships, reduce repeated source-code reading, save tokens/context, initialize .codegraph indexes, or install/use CodeGraph.
---

# CodeGraph Project Index

This is a locator skill, not a full bundled implementation. Its purpose is to make the optional CodeGraph project-indexing workflow discoverable from the skills list.

## Use

When this skill triggers:

1. Read `D:\test\AI_project_basic_ruler\docs\codegraph-integration.md`.
2. Use `D:\test\AI_project_basic_ruler\scripts\setup-codegraph.ps1` for installation, agent configuration, telemetry disablement, project initialization, and `.gitignore` updates.
3. Do not install CodeGraph, initialize `.codegraph/`, or change agent configuration without explicit user approval.

## Quick Commands

Check availability:

```powershell
powershell -ExecutionPolicy Bypass -File D:\test\AI_project_basic_ruler\scripts\setup-codegraph.ps1
```

Install and configure this computer:

```powershell
powershell -ExecutionPolicy Bypass -File D:\test\AI_project_basic_ruler\scripts\setup-codegraph.ps1 -InstallCli -ConfigureAgents -DisableTelemetry
```

Initialize a project index:

```powershell
powershell -ExecutionPolicy Bypass -File D:\test\AI_project_basic_ruler\scripts\setup-codegraph.ps1 -ProjectPath "D:\path\to\project" -InitProject -EnsureGitIgnore
```
