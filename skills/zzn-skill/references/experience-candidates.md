# ZZN Experience Candidates

This is the candidate pool for personal memory evolution. Candidates are not formal memory until zzn explicitly confirms upgrade.

Allowed statuses:

- `候选`
- `高频候选`
- `已升级`
- `废弃`

## C001 - PowerShell 中文乱码判断

状态：已升级
频次：3
来源：DCE 与基础设施项目多次中文文件读取
触发条件：PowerShell 输出中文文件内容出现乱码
问题：AI 容易误判为文件损坏或编码错误
建议规则：优先用 `Get-Content -Encoding UTF8` 或 Python UTF-8 读取确认，不要根据默认终端输出直接判断文件损坏
适用范围：跨项目
建议位置：`references/profile.md`
验证方式：后续中文文件读取任务中减少误判
风险：真实非 UTF-8 文件仍需要二次确认

## C002 - DCE 先工程规范再项目专用 skill

状态：已升级
频次：3
来源：DCE 项目开发规范落地
触发条件：新开 AI 参与 DCE 项目开发
问题：AI 可能直接进入 DCE 业务细节，跳过工程规范、预检和质量门禁
建议规则：先使用 `engineering-standard`，再使用 `dce-generation`，并读取 DCE `AGENTS.md`
适用范围：DCE + 可泛化到项目 skill 分层
建议位置：`references/profile.md`
验证方式：DCE `tools/ai_project_preflight.py` 通过
风险：不要把 DCE 私有规则误写成全局个人规则

## Template

```md
## CXXX - <简短标题>

状态：候选
频次：1
来源：
触发条件：
问题：
建议规则：
适用范围：
建议位置：
验证方式：
风险：
```
