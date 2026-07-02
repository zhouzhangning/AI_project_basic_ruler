# Engineering Standard Evolution Candidates

This is the candidate pool for cross-project engineering rules. Candidates are not formal standards until explicitly confirmed and upgraded.

Allowed statuses:

- `候选`
- `高频候选`
- `已升级`
- `废弃`

## E001 - Multi-baseline Incremental Release Coverage

状态：已升级
频次：3
来源：DCE v1.1.7.5 发布与 Gitee 403 更新失败
触发条件：项目存在自动更新、增量包、旧版本直升路径，且 full 包回退不可靠或成本高
问题：旧版本缺少直升补丁时会回退 full 分卷，可能触发托管平台 403 或配额限制
建议规则：发布校验必须覆盖所有保留旧版本基线，缺少直升补丁应阻止正式发布
适用范围：有自动更新机制、增量包和多旧版本客户端的桌面应用
建议位置：`references/release-and-sync.md` / 项目发布脚本
验证方式：发布脚本检查 `update.json.patches` 与保留基线版本一致
风险：不是所有项目都有增量包机制，不能强制普通 Web/API 项目照搬

## E002 - Personal Skill And Engineering Standard Layering

状态：已升级
频次：3
来源：zzn-skill、engineering-standard、dce-generation 分层落地
触发条件：同时存在个人身份、通用工程规范和项目专用 skill
问题：容易把个人偏好、通用工程规则和项目业务规则混写到同一个 skill
建议规则：个人身份放入 personal skill，跨项目工程规则放入 engineering-standard，项目业务规则放入项目专用 skill 或项目 AGENTS.md
适用范围：多 skill、多项目 AI 协作体系
建议位置：`references/skill-layering.md`
验证方式：校验脚本检查 project-specific terms 是否误入通用层
风险：分层过细会增加初始阅读成本，需要保持 SKILL.md 简洁

## Template

```md
## EXXX - <简短标题>

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
