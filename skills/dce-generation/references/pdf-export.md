# DCE PDF Export

Use this reference for PDF generation from DCE Excel/quotation outputs.

## Preferred Conversion Chain

1. Prefer native WPS export when available.
2. Use Microsoft Excel COM when the project already supports it and WPS is not available.
3. Use LibreOffice as fallback for stable headless conversion.
4. Surface clear errors when all conversion engines fail.

Do not silently switch to an HTML/image approximation for business PDFs unless the user explicitly accepts the tradeoff.

## Quotation PDF Naming

For sales quotation PDF export:

- Default export directory should be the finance table's folder when `finance_path` exists.
- Default PDF name should be based on the finance table name.
- Remove the word `模板` from the base name.
- Append month+day (`MMdd`) if the name does not already end with that suffix.
- Let the user confirm or edit the final save path.

## Layout Rules

- PDF row fitting and Excel preview row fitting may need different tuning. Keep them separate if one mode fixes one output but harms the other.
- Avoid fixed row numbers for PDF row height or image anchors. Use cell content, labels, merged ranges, and template boundaries.
- When users report a blank row/cell-sized gap, inspect generated XLSX rows and the PDF conversion output. The bug may be row-height adaptation, merged-cell expansion, or converter-specific pagination.
- For images/stamps, choose placement based on available rectangle size and image aspect ratio. Do not overlap images. Bound image regions by template labels/cells rather than absolute row numbers.

## Verification

- Generate XLSX and PDF from the same data.
- Inspect row text around the first machine item, AI rows, install/debug rows, transaction terms, and contact rows.
- If using LibreOffice, verify the local install path discovery rather than assuming a fixed installation directory.
