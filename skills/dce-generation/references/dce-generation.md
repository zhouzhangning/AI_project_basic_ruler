# DCE 表生成参考

## 项目定位

DCE 是 PyQt6 桌面工具，用 `ReportData` 作为统一内存模型，生成 FAR Excel、HTML 报告和技术方案 Word 文档。源码根目录：

```text
D:\test\DCE_V1.1_clean\src\excel_report_editor
```

不要修改发布产物中的 `_internal` 文件；这些会在下次打包时被源码覆盖。

## 关键文件职责

- `core/models.py`：统一数据模型。新增可持久化字段时必须同步 `to_dict()` 和 `from_dict()`。
- `core/excel_parser.py`：Excel 输入解析。涉及新表字段来源时先看这里。
- `core/excel_exporter.py`：导出单 sheet 结构化 `.xlsx`，适合新增简单行类型或调试数据交换格式。
- `core/original_far_exporter.py`：把 `ReportData` 写回视觉 FAR 模板。这里大量直接编辑 XLSX XML，目的是保留模板样式、合并单元格、图片和 WPS 行为。
- `core/html_generator.py`：FAR HTML 报告生成。
- `core/technical_plan/mapper.py`：从 `ReportData` 映射技术方案字段、缺陷行、工位行。
- `core/technical_plan/html_preview.py`：技术方案实时预览 HTML。新增预览表时要同步 CSS、HTML 和 JS 桥接。
- `core/technical_plan/exporter.py`：技术方案 Word DOCX 导出。支持占位符块、表格 XML 替换、图片关系写入。
- `core/technical_plan/docx_builder.py`：无模板时生成简化 DOCX 的小型 writer。
- `core/technical_plan/templates.py`：技术方案模板目录和默认模板管理。
- `ui/editor_bridge.py`：预览 JS 与 Python 的保存/更新桥接。
- `ui/main_window.py`：导出、预览、模板选择、打包相关 UI 入口。
- `src/excel_report_editor/report_editor_onedir.spec`：PyInstaller 数据收集。新增 `config/*.json`、模板、源码通常会自动收集，但仍需验证。

## 常见任务模式

### 新增技术方案中的表格

1. 在 `mapper.py` 中整理字段来源，避免在 exporter/html 里重复业务判断。
2. 在 `html_preview.py` 添加 `*_rows()` 和 `table_html()` 调用，保证实时预览可见。
3. 在 `exporter.py` 添加 Word 输出：
   - 无模板路径：用 `DocxBuilder.add_table()` 或 `table()`。
   - 模板路径：优先添加明确占位符，例如 `{{新表格}}`；如必须替换已有模板表，定位条件必须包含表头和排除条件。
4. 若用户需要预览里编辑并保存，增加独立 `config/*.json` 模块，桥接方法放到 `editor_bridge.py`，保存后调用 `refresh_preview()`。
5. 同步模板 `.docx` 时，用 Word 修改源模板，避免直接改打包产物。

### 修改原始 FAR Excel 导出

1. 先判断是结构化 `excel_exporter.py` 还是视觉模板 `original_far_exporter.py`。
2. 对视觉模板，优先复用已有 XML helper：`_find_row`、`_find_cell`、`_set_cell_text`、合并区域 helper、图片 anchor helper。
3. 改行高、列宽、合并单元格、图片位置时，要检查与现有 merge ranges 是否冲突。
4. 保留模板文件有效性：首字节应为 `PK\x03\x04`，ZIP 中应有 `[Content_Types].xml` 和 workbook/document 主文件。

### 新增可配置表项

1. 配置文件放在 `src/excel_report_editor/config/*.json`。
2. 读路径参考 `technical_plan/consumables.py`：开发环境从源码 config 读；frozen 环境优先读 exe 同级 `config`，再读 `_internal` 内置资源。
3. 写路径必须写到 exe 同级 `config`，不要写 `_internal`。
4. 规范化函数要兼容旧字段名和空值。
5. 预览 JS 必须避免把未转义中文表头直接拼进 `onclick/oninput` 字符串；优先用索引或 `data-*` 属性。

## 验证方法

### Python 语法

```powershell
$env:PYTHONIOENCODING='utf-8'
python -m py_compile "D:\test\DCE_V1.1_clean\src\excel_report_editor\core\technical_plan\exporter.py" "D:\test\DCE_V1.1_clean\src\excel_report_editor\core\technical_plan\html_preview.py" "D:\test\DCE_V1.1_clean\src\excel_report_editor\ui\editor_bridge.py"
```

### 生成技术方案预览 HTML

```powershell
$env:PYTHONIOENCODING='utf-8'
python -c "import sys; from pathlib import Path; sys.path.insert(0, r'D:\test\DCE_V1.1_clean\src'); from excel_report_editor.core.models import ReportData; from excel_report_editor.core.technical_plan.html_preview import generate_technical_plan_html; html=generate_technical_plan_html(ReportData(title='测试'), highlight=True); Path(r'D:\test\technical_preview_test.html').write_text(html, encoding='utf-8'); print(len(html))"
```

### 生成 Word 并检查 DOCX

```powershell
$env:PYTHONIOENCODING='utf-8'
python -c "import sys, zipfile; from pathlib import Path; sys.path.insert(0, r'D:\test\DCE_V1.1_clean\src'); from excel_report_editor.core.models import ReportData; from excel_report_editor.core.technical_plan.exporter import TechnicalPlanExporter; out=Path(r'D:\test\technical_export_test.docx'); tpl=Path(r'D:\test\DCE_V1.1_clean\src\excel_report_editor\templates\technical_plan\技术方案V1占位符模板.docx'); TechnicalPlanExporter().export(ReportData(title='测试'), str(out), template_path=str(tpl), highlight=True, redacted=False); z=zipfile.ZipFile(out); print(out, out.stat().st_size, 'word/document.xml' in z.namelist())"
```

### 回归测试

```powershell
python "D:\test\DCE_V1.1_clean\tools\run_regression_tests.py"
```

### 打包但不发布

```powershell
$env:PYTHONPATH='D:\test\DCE_V1.1_clean\.build_deps'
python "D:\test\DCE_V1.1_clean\src\excel_report_editor\build_exe.py" --clean
python "D:\test\DCE_V1.1_clean\tools\package_release.py"
```

## 已知本机注意事项

- Windows sandbox helper 可能失败；必要时用提升权限读取/构建。
- 全局 PyInstaller 曾出现源码文件损坏，打包应优先使用 `D:\test\DCE_V1.1_clean\.build_deps`。
- PowerShell 直接 `Get-Content` 可能把 UTF-8 中文显示成乱码；用 `$env:PYTHONIOENCODING='utf-8'` + Python 读取更可靠。
- 不要把 `DCE_v*`、`build/`、`test_outputs/`、`__pycache__/` 当源码修改。
