# AGENTS.md

本文件是 AI Agent 的项目入口规则。任何 AI 工具参与本项目或使用本模板接入其他项目时，必须先阅读并遵守。

## 项目定位

本仓库是跨项目复用的 AI 工程基础设施，不是具体业务项目。

核心职责：

- 提供通用 AI 协作规则和项目入口模板。
- 提供跨项目可复用的 Codex skills。
- 提供初始化、同步、审计和维护脚本。
- 管理规则如何沉淀、升级、同步到其他项目。

## Skill 分层

通用工程规范和项目专用技能必须分层使用：

```text
zzn-skill
  个人身份档案：用户环境、长期偏好、常见坑和经验进化机制。

engineering-standard
  所有项目统一工程规范：Spec 先行、质量门禁、发布纪律、规则演进、同步边界。

project-specific skill
  项目领域能力：业务规则、文件格式、局部命令、特殊风险。

project AGENTS.md
  项目入口：声明本项目需要哪些 skill，以及本项目特殊约束。
```

当前基础设施包含：

- `skills/zzn-skill`：个人身份档案、长期偏好和经验候选进化机制。
- `skills/engineering-standard`：所有项目通用工程规范。
- `skills/dce-generation`：DCE 项目专用文档、表格、报价、发布工作流。
- `skills/karpathy-guidelines`：编码 Agent 行为约束。
- `skills/codegraph-project-index`：CodeGraph 项目索引和代码理解基础设施。

修改 DCE 业务规则时，不要写进 `engineering-standard`；应更新 `dce-generation` 或 DCE 项目自己的 `AGENTS.md`。

## 工作方式

- 修改前先查看工作区状态。
- 先读相关文档、脚本和现有实现，再动手。
- 不凭空假设项目结构、接口或业务规则。
- 不修改无关文件。
- 优先小步修改，避免一次性大范围重构。
- 遇到不确定问题，先列出判断点；高风险事项等待确认。
- 完成后说明修改文件、核心逻辑、测试结果和剩余风险。

## CodeGraph 使用

- 本仓库没有 `.codegraph/` 时，不强制使用 CodeGraph。
- 目标项目已有 `.codegraph/` 时，理解代码结构、调用关系、复杂 bug、重构或代码审查前，应优先使用 CodeGraph。
- 不要擅自为目标项目初始化 `.codegraph/`；先说明价值和影响，等待确认。
- CodeGraph 结果不能替代源码阅读、测试和人工验收。

## 系统演进规则

通用系统只沉淀跨项目规则：

- 出现 1 次：记录到 `docs/ai-work-log.md`。
- 出现 2 次：整理到 `docs/project-memory.md`。
- 出现 3 次以上且跨项目适用：提出进入通用模板或 `engineering-standard`。
- 项目私有规则留在项目自己的 `AGENTS.md` 或项目专用 skill。
- 未经人工确认，AI 不得擅自把经验、规则、禁区或流程加入通用系统。
- 能自动检查的规则优先做成脚本。
- 能固定复用的流程优先做成 prompt 或 skill reference。

修改本系统前，优先阅读：

```text
docs/evolution-rules.md
docs/maintenance-checklist.md
docs/feature-inventory.md
```

## Git 规则

- 修改前先查看当前分支和工作区状态。
- 不允许擅自执行 `git reset --hard`、`git checkout -- <file>` 等会丢失改动的命令。
- 不允许覆盖用户已有改动。
- 不允许修改 Git 历史，除非用户明确要求。
- 提交信息应说明变更目的和影响范围。

## 代码和脚本规则

- 遵守项目现有风格。
- 优先使用已有脚本、目录结构和模板。
- 不新增不必要抽象。
- 不引入无关依赖。
- 不隐藏错误，不吞掉异常。
- 涉及同步、覆盖、发布、删除、权限、安全、密钥或外部网络的动作必须谨慎处理。

## 测试规则

- 能写或运行测试时优先验证。
- 修改脚本后至少运行对应脚本的基础路径或语法检查。
- 修改 skill 后运行 skill 校验。
- 修改基础设施后运行 `scripts/audit-ai-dev-system.ps1`。
- 如果无法运行测试，必须说明原因和替代验证方式。

## 高风险红线

AI 不得擅自执行以下动作：

- 删除数据或清空目录。
- 覆盖目标项目已有业务规则。
- 修改生产配置、密钥、Token、API Key 或 `.env`。
- 发布生产版本。
- 修改支付、权限、合规、审计逻辑。
- 发送外部消息、邮件或客户通知。
- 大范围重构或目录迁移。

## 输出格式

完成任务后输出：

```text
改动摘要：
修改文件：
测试结果：
剩余风险：
需要人工确认：
```
