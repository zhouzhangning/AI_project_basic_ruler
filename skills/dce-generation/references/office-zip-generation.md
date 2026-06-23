# Office ZIP/XML 生成参考

XLSX, DOCX, and PPTX are Office Open XML ZIP containers. Use this reference when generation must preserve templates, images, relationships, comments, or complex formatting.

## Shared Package Rules

- Validate the file starts with `PK\x03\x04`.
- Preserve `[Content_Types].xml`.
- Preserve relationship files under `_rels/` and nested `_rels/` directories.
- When adding media, add both the media file and its relationship entry.
- When replacing XML blocks, preserve namespace prefixes and surrounding document structure.
- Prefer explicit placeholders over fuzzy text matching.

## DOCX

DCE technical plan export lives mainly in `core/technical_plan/exporter.py`.

- Main document: `word/document.xml`.
- Relationships: `word/_rels/document.xml.rels`.
- Media: `word/media/*`.
- Template replacement should target placeholders such as `{{产品图片}}`, `{{工位配置表}}`, `{{缺陷参数表}}`, `{{工位成像效果图}}`.
- When replacing an existing table, require positive and negative guards, for example “contains 参考价格” and “row contains 玻璃盘” for the consumables table.

## PPTX

PowerPoint uses a similar package structure:

- Slides: `ppt/slides/slideN.xml`.
- Slide relationships: `ppt/slides/_rels/slideN.xml.rels`.
- Media: `ppt/media/*`.

For generated PPTX reports, prefer a placeholder slide template. Replace text boxes or table cells by placeholder text, then update media relationships for images.

## PDF

Prefer generating PDF from DOCX/PPTX/HTML when layout matters. Direct PDF editing is more brittle.

Verify:

- Page count.
- Text presence for key labels.
- Image count or visual screenshots when images matter.
- No accidental blank pages.

## DCE Preview Alignment

If a generated DOCX/PPTX/PDF table has a realtime preview, update HTML preview rows and export rows from the same mapping/helper where possible.
