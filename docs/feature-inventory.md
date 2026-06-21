# 功能清单

本文件记录 AI Dev System 当前提供的长期基础设施能力。它面向后续所有项目复用，不绑定某个具体项目。

## 1. AI 协作规则

- `AGENTS.md`：通用 Agent 工作规则，约束 AI 在项目中的默认行为。
- `CLAUDE.md`：Claude Code 适配说明。
- `GEMINI.md`：Gemini 适配说明。
- `.cursorrules`：Cursor 适配说明。
- `README-AI.md`：给任意 AI 工具读取的通用协作说明。

核心能力：

- 修改前先理解项目。
- 不凭空假设项目结构、接口或业务规则。
- 小步修改，避免无审批的大范围重构。
- 完成后输出改动摘要、测试结果和剩余风险。

## 2. 审批与风险边界

- `docs/ai-approval-rules.md`：定义必须人工确认的高风险动作。

覆盖范围：

- 删除文件或数据。
- 安装、升级、移除依赖。
- 修改数据库、权限、安全、支付、审计逻辑。
- 修改生产配置或密钥管理。
- 发布、部署、修改 Git 历史。
- 大范围重构或目录迁移。

## 3. 项目初始化与同步

- `scripts/init-ai-dev-system.ps1`：把基础设施模板复制到目标项目。
- `scripts/update-ai-dev-system.ps1`：从模板仓库更新目标项目。
- `scripts/sync-selected-ai-dev-system.ps1`：按功能模块选择性同步到目标项目。
- `scripts/start-ai-dev-system-gui.ps1`：选择性同步的简易图形界面。
- `start-ai-dev-system-gui.bat`：双击启动简易同步界面。
- `docs/sync-rules.md`：定义多电脑、多项目同步规则。

默认策略：

- 不覆盖目标项目已有文件。
- 保留目标项目自己的业务规则和长期记忆。
- 通用模板只沉淀跨项目适用的规则。
- 可以只同步需要的功能模块，不必一次复制全套基础设施。

## 4. 审计与维护

- `scripts/audit-ai-dev-system.ps1`：检查基础设施文件完整性和文档长度。
- `docs/maintenance-checklist.md`：定期维护检查清单。
- `docs/evolution-rules.md`：定义规则、模板、脚本如何健康增长。

维护原则：

- 一次性问题只记录，不进入通用规则。
- 反复出现且跨项目适用的问题才沉淀到模板。
- 能自动检查的规则优先做成脚本。
- 能固定复用的流程优先做成 prompt。

## 5. 任务模板

`prompts/` 目录保存可复用任务提示词：

- `add-feature.md`：新增功能。
- `fix-bug.md`：修复 Bug。
- `review-code.md`：代码审查。
- `refactor.md`：重构。
- `write-tests.md`：补测试。
- `codegraph-usage.md`：CodeGraph 使用判断和常用指令。
- `start-project.md`：启动新项目。
- `improve-ai-dev-system.md`：改进基础设施。
- `add-experience-candidate.md`：提交经验沉淀候选项。

这些模板用于让任务输入更稳定，减少 AI 对目标、范围、验收和输出格式的误解。

## 6. 项目记忆与工作记录

- `docs/project-memory.md`：长期经验、偏好、风险提醒和固定流程。
- `docs/ai-work-log.md`：单次任务过程记录。
- `docs/ai-task-template.md`：复杂任务描述模板。

分层规则：

- `ai-work-log.md` 记录一次性任务。
- `project-memory.md` 记录反复出现的项目经验。
- 通用模板只记录跨项目共性。

## 7. CodeGraph 可选代码理解基础设施

- `docs/codegraph-integration.md`：CodeGraph 使用说明。
- `scripts/setup-codegraph.ps1`：检查、安装、配置和初始化 CodeGraph 的辅助脚本。
- `.gitignore`：忽略 `.codegraph/` 本地索引目录。

定位：

- CodeGraph 用于建立本地代码知识图谱。
- 适合新项目接手、代码审查、影响分析和复杂修改。
- 不作为强制依赖，不同步每个项目生成的 `.codegraph/` 数据库。

常用启用命令：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-codegraph.ps1 -InstallCli -ConfigureAgents -DisableTelemetry
powershell -ExecutionPolicy Bypass -File .\scripts\setup-codegraph.ps1 -ProjectPath "D:\path\to\project" -InitProject -EnsureGitIgnore
```

## 8. 发布与测试检查

- `docs/release-checklist.md`：发布前检查清单。
- `docs/test-checklist.md`：测试检查清单。

这些清单用于约束 AI 在打包、发布、测试时必须说明验证范围和剩余风险。

## 9. 当前不包含的能力

本基础设施项目当前不直接包含：

- 具体业务项目代码。
- 私有客户资料、公司专属流程或密钥。
- 每个项目的 `.codegraph/` 索引数据。
- 自动发布生产版本的脚本。
- 重依赖的个人智能体平台。

这些内容应留在具体项目、私有知识库或单独的技能仓库中。
