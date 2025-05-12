import re
from openpyxl import load_workbook
from pathlib import Path

FIELD_PATTERN = re.compile(r"{{\s*(\w+)\s*}}")

def extract_fields_from_excel(file_path: Path) -> list[str]:
    workbook = load_workbook(filename=file_path)
    found_fields = set()

    for sheet in workbook.worksheets:
        for row in sheet.iter_rows(values_only=True):
            for cell in row:
                if isinstance(cell, str):
                    for match in FIELD_PATTERN.findall(cell):
                        found_fields.add(match)

    return sorted(found_fields)
