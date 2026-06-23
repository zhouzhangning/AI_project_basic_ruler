# Excel 生成参考

Use this for XLSX generation, especially when preserving an existing business template.

## Strengths Taken From excel-advanced-processor

- Copy the template first, then write into the copy.
- Capture and reapply merged cells, row heights, column widths, styles, and header formatting.
- Treat image insertion as fragile; use `TwoCellAnchor` first, then ZIP/XML editing if library output is wrong.
- Extract embedded source images when the input workbook itself contains images.
- Keep a reusable helper script for repeated non-DCE Excel generation.

## Preferred Flow

1. Copy template with `shutil.copy2(template, output)`.
2. Load the copied workbook, not the original template.
3. Capture reusable formatting from template ranges using row/column offsets.
4. Insert/delete rows carefully, then reapply merge/style/height/width.
5. Insert images after row layout is stable.
6. Save and validate the output ZIP structure.

## DCE Notes

- For normal single-sheet exchange format, use `core/excel_exporter.py`.
- For visual FAR template output, use `core/original_far_exporter.py`; it already contains XML helpers to preserve merged cells, images, relationships, WPS `DISPIMG`, and template behavior.
- Do not replace DCE XML helpers with a generic script unless the existing path cannot support the task.

## Useful Patterns

- `ws._images = []` is more reliable than `ws._images.clear()` when removing images.
- Use `copy.copy()` for `font`, `fill`, `alignment`, and `border` style objects.
- Store merge ranges as offsets from a template block start row, not absolute row numbers.
- For image anchors, remember `AnchorMarker` row/col are zero-based.

## Structural Validation

```python
import zipfile
with open(path, 'rb') as f:
    assert f.read(4) == b'PK\x03\x04'
with zipfile.ZipFile(path) as zf:
    names = set(zf.namelist())
assert '[Content_Types].xml' in names
assert 'xl/workbook.xml' in names
```
