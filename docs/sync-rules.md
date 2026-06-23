# 多电脑同步规则

本文件定义在家里、公司、不同电脑、不同 AI 工具之间复用和更新 AI Dev System 的规则。

## 核心原则

```text
模板仓库负责通用规则，项目仓库负责项目规则。
先更新模板，再同步项目。
默认不覆盖，确认后再覆盖。
```

## 仓库分工

### AI Dev System 模板仓库

用于保存跨项目通用内容：

- 通用 `AGENTS.md`
- AI 工具适配规则
- 审批规则
- 任务模板
- 检查清单
- 初始化和审计脚本
- 可选基础设施说明和辅助脚本，例如 CodeGraph 集成

### 具体项目仓库

用于保存项目私有内容：

- 项目技术栈
- 启动和测试命令
- 业务规则
- 项目禁区
- 项目工作日志
- 项目长期记忆

不要把公司项目的专属业务规则回灌到通用模板，除非它已经被确认是跨项目通用规则。

## 在新电脑上使用

1. 克隆模板仓库。
2. 运行审计脚本确认模板完整。
3. 把模板初始化到目标项目。
4. 根据目标项目补充项目私有规则。

```powershell
git clone https://github.com/zhouzhangning/AI_project_basic_ruler.git
cd AI_project_basic_ruler
.\scripts\audit-ai-dev-system.ps1
.\scripts\init-ai-dev-system.ps1 -TargetPath "D:\path\to\project"
```

如果模板仓库包含本地 Codex skills，也可以安装到当前电脑：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-local-skills.ps1
```

例如 `skills\dce-generation`、`skills\karpathy-guidelines` 会安装到 `%USERPROFILE%\.codex\skills`，供 Codex 在对应任务中自动使用。

如果只需要同步部分功能，可以双击 `start-ai-dev-system-gui.bat`，或使用：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync-selected-ai-dev-system.ps1 -TargetPath "D:\path\to\project" -Features core-rules,approval,task-prompts
```

如果这台电脑需要启用 CodeGraph：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-codegraph.ps1 -InstallCli -ConfigureAgents -DisableTelemetry
powershell -ExecutionPolicy Bypass -File .\scripts\setup-codegraph.ps1 -ProjectPath "D:\path\to\project" -InitProject -EnsureGitIgnore
```

## 在已有电脑上更新

```powershell
cd D:\test\ai-dev-system
git pull
.\scripts\audit-ai-dev-system.ps1
.\scripts\update-ai-dev-system.ps1 -TargetPath "D:\path\to\project"
```

## 默认同步策略

默认情况下：

- 新文件会复制到目标项目。
- 已存在文件不会覆盖。
- 目标项目自己的 `AGENTS.md`、`README-AI.md`、`docs/project-memory.md` 不会被破坏。
- `.codegraph/` 这类本地索引不进入 Git，同步的是启用方法和规则，不是索引数据。
- `skills/` 中的是可提交的 skill 模板；每台电脑通过 `install-local-skills.ps1` 安装到本机 Codex skills 目录。
- 简易界面和选择性同步脚本默认同样不覆盖已有文件，除非明确选择覆盖。

如果确实要覆盖，必须显式使用：

```powershell
.\scripts\update-ai-dev-system.ps1 -TargetPath "D:\path\to\project" -Overwrite
```

## 公司环境注意事项

在公司电脑或公司项目中：

- 不要把公司代码、客户资料、密钥、内部流程提交到个人模板仓库。
- 不要把公司项目专属规则写入通用模板。
- 不要覆盖公司项目已有规则文件。
- 更新前先查看目标项目 Git 状态。
- 如涉及公司安全、权限、发布、客户数据，必须人工确认。

## 冲突处理

如果模板和目标项目都有同名文件：

1. 先比较差异。
2. 判断目标项目内容是否是项目私有规则。
3. 项目私有规则优先保留。
4. 通用规则可以复制到单独文件，再人工合并。
5. 不要让脚本自动覆盖业务规则。

## 什么时候更新模板仓库

适合更新：

- 出现跨项目重复问题。
- 新增了更好的 AI 任务模板。
- 审批规则发现明显缺口。
- 审计脚本需要检查更多风险。
- 某个流程在多个项目中验证有效。

不适合更新：

- 只属于某个公司项目的规则。
- 只出现一次的问题。
- 临时实验性提示词。
- 未验证的新流程。

