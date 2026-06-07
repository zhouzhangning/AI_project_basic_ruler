# AI Dev System

一套可复制到任何项目里的 AI 开发治理模板。目标是让 Codex、Claude Code、Gemini、Cursor 等 AI 工具在同一套规则下工作：先理解项目，再按边界修改，关键动作需要审批，结果必须可验证、可记录、可回滚。

## 适用场景

- 新项目初始化 AI 协作规则
- 老项目补充 AI 开发治理
- 多台电脑、多种 AI 工具之间复用同一套工作流
- 把 Git 版本管理和 AI 行为管理接起来

## 文件说明

- `AGENTS.md`：Codex / 通用 Agent 项目规则
- `CLAUDE.md`：Claude Code 适配规则
- `GEMINI.md`：Gemini 适配规则
- `.cursorrules`：Cursor 适配规则
- `README-AI.md`：给任意 AI 工具读取的通用说明
- `docs/ai-approval-rules.md`：AI 高风险动作审批规则
- `docs/ai-task-template.md`：AI 任务描述模板
- `docs/ai-work-log.md`：AI 工作日志
- `docs/project-memory.md`：项目长期记忆
- `docs/evolution-rules.md`：系统如何健康增长的规则
- `docs/maintenance-checklist.md`：定期维护和清理清单
- `docs/release-checklist.md`：发布检查清单
- `docs/test-checklist.md`：测试检查清单
- `prompts/`：常用提示词模板
- `scripts/init-ai-dev-system.ps1`：把模板复制到目标项目的一键初始化脚本
- `scripts/audit-ai-dev-system.ps1`：检查模板完整性、文件大小和维护风险

## 快速使用

在 PowerShell 中运行：

```powershell
.\scripts\init-ai-dev-system.ps1 -TargetPath "D:\path\to\your-project"
```

如果目标项目已有同名文件，脚本默认不会覆盖。需要覆盖时使用：

```powershell
.\scripts\init-ai-dev-system.ps1 -TargetPath "D:\path\to\your-project" -Overwrite
```

## 推荐工作流

1. 让 AI 先阅读项目，不修改文件。
2. 让 AI 输出任务方案、影响范围和风险。
3. 人确认后，AI 才开始改代码。
4. AI 修改后运行测试或给出无法运行的原因。
5. AI 输出改动摘要、测试结果、剩余风险。
6. 人检查后再 Git commit。

## 核心原则

- Git 管代码结果，AI Dev System 管 AI 行为。
- 低风险任务可以自动推进，高风险动作必须暂停审批。
- 所有复杂任务都要有目标、范围、约束、验收和输出要求。
- 重复出现的偏好写进规则，重复流程做成模板。
- 通用规则只收跨项目共性，项目特例留在项目自己的规则里。
- 系统要健康变大：新增规则必须说明用途、触发条件和维护位置。

## 维护方式

每次扩展本系统前，先阅读：

```text
docs/evolution-rules.md
docs/maintenance-checklist.md
```

扩展后运行：

```powershell
.\scripts\audit-ai-dev-system.ps1
```
