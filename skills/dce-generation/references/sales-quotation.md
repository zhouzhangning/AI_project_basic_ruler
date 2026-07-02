# DCE Sales Quotation

Use this reference for `src/excel_report_editor/core/plugins/sales_quotation/`.

## Source Map

- Models: `models.py`
- Import parsing: `parser.py`
- Left-panel UI: `panel.py`
- XLSX/PDF export: `exporter.py`
- App version: `src/excel_report_editor/app_info.py`

## Core Invariants

- Preserve the quotation template structure. Do not break merged cells, borders, sequence column, product-name cells, unit price, amount, or remark columns.
- Do not merge remarks into the specification description unless the current template explicitly does so.
- Do not alter AI software/platform/model rows when working on machine item rows. The AI model row structure must remain intact.
- Do not solve quotation layout problems with fixed row numbers. Use content, labels, merged-cell boundaries, or template anchors.
- Row height must adapt to content. Avoid hard-coded row counts or absolute row heights except as bounded fallbacks.

## Finance Detail Confirmation

The finance table import should create editable candidates, not blindly inject all rows into item 1.

- Store candidates as `FinanceSpecOption` on `SalesQuotationData`.
- Show finance details through a confirmation UI/dialog where users can:
  - check/uncheck inclusion,
  - edit category,
  - edit component,
  - edit unit,
  - edit quantity,
  - edit quotation display text.
- The selected candidates compose the first quotation item's specs after the detection-equipment line.
- The main panel should show a module-level status such as selected/total count; use a dialog for the full finance table instead of squeezing it into the side panel.

## First Item Specification Order

For the first machine item, selected specs should be ordered:

1. Detection equipment and workstation summary
2. Camera
3. Lens
4. Industrial PC
5. GPU
6. NIC
7. Board/card
8. Fiber
9. Electrical accessories
10. Solenoid valve
11. Feeding method
12. Discharge outlet

Standard-template entries must not be omitted when applicable. Keep these display names stable:

- `光纤(基恩士)`
- `电器配件(施耐德)`
- `电磁阀(MAC)`
- `振动盘(600mm盘面*1)+皮带`
- `吹气(良品*1、不良*1、重测*1)`

`短款（标准款）` / count-discharge entries should not be default-selected unless the user explicitly chooses them.

## Import Order Safety

- Importing the optical table first or finance table first must produce the same combined result.
- Optical import owns detection-equipment/workstation specs and product images.
- Finance import owns finance candidates and selected finance spec rows.
- Do not let either import overwrite unrelated user-edited fields or unrelated template rows.

## Verification

Run at least:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONPATH='D:\test\DCE_V1.1_clean\src'
python -m py_compile src\excel_report_editor\core\plugins\sales_quotation\models.py src\excel_report_editor\core\plugins\sales_quotation\parser.py src\excel_report_editor\core\plugins\sales_quotation\panel.py src\excel_report_editor\core\plugins\sales_quotation\exporter.py
```

For sample verification, use the known `shili` optical/finance files under the Chongqing project folder when available, and inspect exported rows 18 onward for item 1, AI rows, and install/debug rows.
