# DCE UI Guidelines

Use this reference when changing DCE PyQt panels, especially plugin panels in the left-side editor.

## General Layout

- Prefer task-oriented modules over many small loose buttons.
- Keep import/drop zones near the top when the workflow starts with importing source files.
- Keep final actions such as preview/export at the bottom when they apply to the whole document.
- Let the central editing table use the main stretchable space.
- Avoid fixed heights for content-heavy controls. Use size policies, stretch factors, and dialogs.

## Sales Quotation Panel

Recommended order:

1. Import buttons and drag/drop area
2. Source-file status
3. Compact quote/customer fields, two fields per row where possible
4. Finance-detail confirmation module
5. Quotation item / sequence module
6. Bottom preview/export actions

Finance-detail confirmation should be a module on the panel, with a clear status and a button that opens a dialog. Do not squeeze the full finance table into the side panel.

Sequence controls belong inside the quotation item module:

- `添加序号`
- `删除序号`

Document actions belong at the bottom:

- `预览Excel`
- `导出PDF`

## Dialogs

- Use dialogs for dense editable tables, such as finance detail confirmation.
- Dialog tables should allow editing fields that users naturally need to correct.
- Include enough width/height for realistic data. Avoid tiny modal layouts.

## Verification

- Run `py_compile` for changed modules.
- Instantiate PyQt widgets with `QT_QPA_PLATFORM=offscreen` to catch missing attributes and basic layout construction errors.
- When a packaged behavior is requested, build the EXE after UI validation.
