# CodeGraph 集成说明

本文件定义如何把 CodeGraph 作为可选的代码理解基础设施使用。CodeGraph 用于建立本地代码知识图谱，帮助 AI 更快理解项目结构、调用关系和影响范围。

## 定位

```text
AI Dev System：管理 AI 工作规则和审批边界。
CodeGraph：提供代码结构索引和影响分析能力。
```

CodeGraph 不是必选依赖。只在中大型代码项目、陌生项目接手、复杂修改、代码审查、影响分析时启用。

## 适用场景

- 接手一个新代码库，需要快速理解入口、模块和调用链。
- 修改公共函数、核心流程、导出流程、权限逻辑等高影响代码。
- 做代码审查，需要判断调用方、被调方和影响范围。
- 希望减少 AI 反复 `rg`、读文件和无效探索。

不适合用于纯文档项目、小脚本项目、视频分析素材目录或没有源码结构的文件夹。

## 推荐流程

在新电脑上：

```powershell
git clone https://github.com/zhouzhangning/AI_project_basic_ruler.git
cd AI_project_basic_ruler
powershell -ExecutionPolicy Bypass -File .\scripts\setup-codegraph.ps1 -InstallCli -ConfigureAgents -DisableTelemetry
```

在具体项目中启用：

```powershell
cd AI_project_basic_ruler
powershell -ExecutionPolicy Bypass -File .\scripts\setup-codegraph.ps1 -ProjectPath "D:\path\to\project" -InitProject -EnsureGitIgnore
```

检查状态：

```powershell
codegraph status "D:\path\to\project"
```

## 使用原则

- `.codegraph/` 是本地索引目录，不提交到 Git。
- 公司项目或敏感项目建议关闭 telemetry。
- CodeGraph 结果用于快速定位和建立结构理解，关键修改仍要读源码和运行测试。
- 没有 `.codegraph/` 的项目不要强制启用，由用户确认后再初始化。
- 安装 CLI、写入 Agent 配置、初始化项目索引都属于环境变更，应明确执行。

## 常用命令

```powershell
codegraph install
codegraph init "D:\path\to\project"
codegraph status "D:\path\to\project"
codegraph explore "how does login work"
codegraph callers "functionName"
codegraph callees "functionName"
codegraph impact "functionName"
codegraph affected --stdin
codegraph telemetry off
```

## 多电脑同步策略

同步的内容：

- 本说明文件。
- `scripts/setup-codegraph.ps1`。
- AI 使用 CodeGraph 的规则和流程。

不同步的内容：

- 每台电脑的全局安装目录。
- Agent 本地配置文件。
- 每个项目的 `.codegraph/` 索引目录。

每台新电脑只需要执行一次全局安装和 Agent 配置；每个项目只需要执行一次 `codegraph init`。
