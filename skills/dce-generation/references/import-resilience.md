# DCE Excel Import Resilience

Use this reference when FAR, quotation, optical, or finance Excel imports fail, hang, or differ between button import and drag/drop import.

## Shared Principles

- Button import and drag/drop import should share the same parsing path after file classification.
- Keep quick file classification shallow: enough to distinguish expected file types without deeply binding to volatile content.
- For quotation imports, accept at most two files at once:
  - one optical table,
  - one finance table.
- Reject duplicates such as two optical tables, two finance tables, `A + B + extra`, or more than two files.

## Fallback Chain

For `.xlsx` / `.xlsm` files:

1. Fast ZIP/XML inspection for type detection and simple previews.
2. `openpyxl` load for normal files.
3. If the file is invalid or WPS/Excel-encrypted/oddly saved, try Office/WPS normalization by opening and saving to a standard `.xlsx`.
4. In frozen EXE builds, use the external Python fallback when available. FAR import already relied on this pattern historically; quotation/optical/finance import should not regress compared with FAR.
5. Return actionable warnings that name the failed stage.

## Performance

- Avoid expensive deep parsing during drag-enter or file classification.
- Do not block the UI with unnecessary full workbook parsing before validating type/count constraints.
- If a file import can take time, validate basic file count/type first, then parse only the accepted files.

## Verification

- Test button import and drag/drop import with the same files.
- Test optical-first and finance-first import order.
- Test invalid count/type cases.
- Test on packaged EXE when the issue only appears on coworker machines.
