# AI Dev System Dashboard

AI 基础设施可视化控制台。

---

## 三种打开方式

### 方式一：静态双击（零依赖）

直接双击 `index.html` 即可打开。Three.js 3D 场景需联网加载 CDN。

### 方式二：本地服务器（实时数据+脚本执行）

```powershell
cd D:\test\AI_project_basic_ruler
python dashboard\server.py
```

或双击 `dashboard\start-server.bat`

浏览器访问 `http://127.0.0.1:8765`

### 方式三：数据生成（离线更新）

```powershell
python scripts\generate-dashboard-data.py
```

重扫描项目结构，更新 `dashboard/dashboard-data.json`。也支持监控模式：

```powershell
python scripts\generate-dashboard-data.py --watch
```

---

## 页面结构（6屏控制台）

| 导航 | 名称 | 内容 |
|------|------|------|
| 🛰 | Control Center | 身份链路(我是谁→规范→Skill→进化→健康)、系统状态卡片、启动流程 |
| 🌌 | Skill Universe | **3D 交互** Skill 分层塔 + **10个功能模块卫星节点** + 分支连线 |
| 🧬 | Evolution Pipeline | 经验候选 5 阶段流水线、已升级候选列表、升级审核清单 |
| 🛡 | Governance Matrix | 6维治理维度：个人记忆/工程规范/项目规则/审批/脚本/Git |
| ⬡ | Command Deck | 终端风格命令面板（静态模式可复制，服务器模式可点击执行） |
| 🔌 | Project Integration | DCE 项目 6 项集成状态、Skill 加载链路图 |

---

## Skill Universe 3D 交互

- **拖拽旋转**、**滚轮缩放**、**自动旋转**
- **4层分层塔**：zzn-skill(粉) → engineering-standard(紫) → 项目Skill(青) → AGENTS.md(金)
- **10个卫星节点**环绕分层塔，带彩色连线，点击查看详情
  - AI协作规则 / 审批风险 / 初始化同步 / 审计维护 / 任务模板
  - 记忆记录 / CodeGraph / 发布测试 / 本地Skills / 边界声明
- 点击任意节点 → 右侧滑出详情面板

---

## API 端点（服务器模式）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/status` | 状态快照 (Skills, Git, DCE集成) |
| GET | `/api/git-status` | Git 详细状态 |
| GET | `/api/data` | 完整 dashboard-data.json |
| POST | `/api/run-script` | 执行校验脚本 (SSE流式输出) |

### 执行脚本示例

```bash
curl -X POST http://127.0.0.1:8765/api/run-script \
  -H "Content-Type: application/json" \
  -d '{"script":"skills/engineering-standard/scripts/validate_engineering_standard.py"}'
```

---

## 文件清单

```
dashboard/
├── index.html              # 主页面 (1495行)
├── server.py               # Flask 本地服务
├── start-server.bat        # Windows 一键启动
├── dashboard-data.json     # 项目扫描数据
├── requirements.txt        # Python 依赖
└── README.md               # 本文件

scripts/
└── generate-dashboard-data.py  # 数据生成脚本 (支持 --watch 监控)
```

---

## 升级路线（已完成）

- ✅ 第一阶段: 静态高级 Dashboard（6屏控制台 + 3D Skill Universe）
- ✅ 第二阶段: 自动数据生成脚本 (`generate-dashboard-data.py` + `--watch`)
- ✅ 第三阶段: 本地 Web 服务 + API 命令执行 (`server.py`)
- 🔮 未来: CI 集成、健康评分、AI 体检报告
