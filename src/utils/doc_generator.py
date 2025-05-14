import re
from pathlib import Path
from datetime import datetime
from openpyxl import load_workbook
from shutil import copyfile

from utils.data_expander import expand_data_for_template


class ActDocumentGenerator:
    def __init__(self, act, template, output_dir="output"):
        self.act = act
        self.template = template
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def expand_data(self):
        return expand_data_for_template(self.act.data)

    def fill_template(self, expanded_data: dict, template_path: Path, output_path: Path):
        wb = load_workbook(template_path)
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str):
                        matches = re.findall(r"\{\{\s*(\w+)\s*\}\}", cell.value)
                        for match in matches:
                            if match in expanded_data:
                                cell.value = cell.value.replace(f"{{{{ {match} }}}}", str(expanded_data[match]))
        wb.save(output_path)

    def generate(self):
        object_dir = self.output_dir / self.act.build_object.name
        object_dir.mkdir(parents=True, exist_ok=True)

        output_filename = f"{self.act.name} от {self.timestamp}.xlsx"
        output_path = object_dir / output_filename

        expanded_data = self.expand_data()
        self.fill_template(Path(self.template.path), output_path)

        return output_path
