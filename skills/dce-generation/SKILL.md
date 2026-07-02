---
name: dce-generation
description: General document and table generation workflow with DCE project specialization. Use when Codex needs to add, modify, or debug generated business files such as Excel/XLSX tables, Word/DOCX technical proposals, PowerPoint/PPTX reports, PDF outputs, HTML realtime previews, template placeholders, embedded images, Office ZIP/XML internals, or DCE-specific FAR/technical-plan generation in D:\test\DCE_V1.1_clean.
---

# DCE Generation

Use this skill for generated document/table work. It is intentionally broader than Excel: apply it to XLSX, DOCX, PPTX, PDF, HTML preview output, template-driven files, embedded images, and DCE-specific generation flows.

## First Moves

1. Identify the output format and generation path before editing.
2. Inspect the current worktree. For DCE: `git -C "D:\test\DCE_V1.1_clean" status --short`.
3. Do not edit packed `_internal` files. Edit source/templates, then rebuild if needed.
4. Preserve user changes and avoid broad rewrites.
5. Validate generated files structurally, not only by “no exception”.

## Format Routing

- **XLSX / Excel tables**: read `references/excel-generation.md`; in DCE inspect `core/excel_exporter.py` and `core/original_far_exporter.py`.
- **Sales quotation / 报价表**: read `references/sales-quotation.md`; inspect `src/excel_report_editor/core/plugins/sales_quotation/`.
- **DOCX / Word templates**: read `references/office-zip-generation.md`; in DCE inspect `core/technical_plan/exporter.py`, `docx_builder.py`, and templates under `src/excel_report_editor/templates/technical_plan/`.
- **PPTX / PowerPoint**: treat as Office Open XML ZIP like DOCX/XLSX; prefer placeholders and relationship-safe media insertion.
- **PDF output**: read `references/pdf-export.md`; generate from source format when possible; if editing PDF directly, preserve text/images carefully and verify page count/content.
- **HTML preview**: in DCE inspect `core/technical_plan/html_preview.py` or `core/html_generator.py`; keep preview and exported file aligned.
- **DCE field mapping**: inspect `core/technical_plan/mapper.py` and `core/models.py` before adding new generated fields.
- **Excel import failures / drag-drop import**: read `references/import-resilience.md`.
- **DCE UI changes**: read `references/ui-guidelines.md`.
- **Build, package, release, Gitee update**: read `references/release-workflow.md`.

## Core Principles

- Prefer template copy + targeted fill for business documents.
- Treat `.xlsx`, `.docx`, and `.pptx` as ZIP packages with XML relationships.
- Preserve formatting: merged cells, row heights, column widths, styles, relationships, images, content types, and existing media.
- For images, use the project’s existing anchoring conventions first; if library output is unreliable, inspect or edit ZIP/XML directly.
- For user-editable generated tables, use config JSON patterns and save outside frozen `_internal` resources.
- For template replacement, use explicit placeholders or precise table detection. Avoid broad regex that can affect unrelated tables.
- Keep generated preview, export, and parser/import behavior consistent.

## References

- `references/dce-generation.md`: DCE-specific source map, validation commands, and known local environment notes.
- `references/excel-generation.md`: Excel template preservation and image handling patterns, adapted from `excel-advanced-processor`.
- `references/office-zip-generation.md`: DOCX/PPTX/XLSX ZIP/XML safety checklist.
- `references/sales-quotation.md`: sales quotation import, finance-detail confirmation, row-height, order, and template invariants.
- `references/pdf-export.md`: WPS/LibreOffice PDF export behavior and naming rules.
- `references/import-resilience.md`: shared Excel import fallback chain and drag/drop constraints.
- `references/release-workflow.md`: official build, versioning, publishing, and Gitee update rules.
- `references/ui-guidelines.md`: DCE panel layout rules, module sections, and dialog expectations.

## Reusable Script

- `scripts/excel_template_processor.py`: optional generic Excel template helper copied from the existing advanced Excel skill. Read or adapt it when repeatedly generating Excel files from templates; do not force it into DCE if existing DCE helpers are better.

## Verification

Use narrow checks for the changed format:

```powershell
$env:PYTHONIOENCODING='utf-8'
python -m py_compile "D:\test\DCE_V1.1_clean\src\excel_report_editor\core\technical_plan\exporter.py" "D:\test\DCE_V1.1_clean\src\excel_report_editor\core\technical_plan\html_preview.py"
python "D:\test\DCE_V1.1_clean\tools\run_regression_tests.py"
```

For local DCE packaging without publishing:

```powershell
$env:PYTHONPATH='D:\test\DCE_V1.1_clean\.build_deps'
python "D:\test\DCE_V1.1_clean\src\excel_report_editor\build_exe.py" --clean
python "D:\test\DCE_V1.1_clean\tools\package_release.py"
```

Do not publish unless explicitly asked.
