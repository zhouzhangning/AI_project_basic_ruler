# AI Dev System 演进规则

本文件规定这套系统如何健康变大。目标不是堆规则，而是让规则、模板和脚本越来越准。

## 分层原则

系统分为三层：

```text
通用层：跨项目、跨 AI 工具都适用，放在 ai-dev-system。
项目层：只适用于某个项目，放在目标项目自己的 AGENTS.md / README-AI.md。
经验层：临时记录、失败案例、偏好和复盘，放在 ai-work-log.md / project-memory.md。
```

## 沉淀规则

- 出现 1 次：只写入 `docs/ai-work-log.md`。
- 出现 2 次：整理到 `docs/project-memory.md`。
- 出现 3 次以上，且跨项目适用：考虑进入通用模板。
- 能自动检查的规则：优先做成脚本。
- 能固定复用的流程：优先做成 prompt。
- 会影响 AI 行为边界的规则：写入 `AGENTS.md` 或 `ai-approval-rules.md`。

## 新增规则必须回答

新增任何规则前，先回答：

```text
这条规则防止什么错误？
它什么时候触发？
它适用于所有项目，还是只适用于当前项目？
它应该放在规则、prompt、checklist 还是脚本里？
它是否会让 AI 更难执行任务？
```

如果回答不清楚，不要沉淀到通用模板。

## 文件职责

- `AGENTS.md`：最高优先级行为规则，必须短、硬、稳定。
- `docs/ai-approval-rules.md`：高风险动作边界。
- `docs/project-memory.md`：经验和偏好，不要求永久稳定。
- `docs/ai-work-log.md`：过程记录，可以定期归档。
- `prompts/`：可复用任务流程。
- `scripts/`：可自动检查或自动复制的动作。

## 反膨胀规则

- 不把项目私有规则写进通用模板。
- 不把一次性错误写进 `AGENTS.md`。
- 不把长解释写进主规则，长内容应进入 `docs/`。
- 不重复描述同一条规则。
- 不保留已经无效的工具说明。

## 升级流程

每次升级本系统时：

1. 先判断新增内容属于规则、模板、日志、记忆还是脚本。
2. 修改后运行 `scripts/audit-ai-dev-system.ps1`。
3. 更新 `README.md` 的文件说明。
4. 提交 Git，并在 commit message 中说明升级目的。

