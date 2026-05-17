import json
import tempfile
import unittest
from pathlib import Path

from components.documentation import (
    export_documentation_html,
    export_documentation_json,
    export_documentation_markdown,
    get_all_objects_documentation,
    get_all_part_sets_documentation,
)


ROOT = Path(__file__).resolve().parents[1]
OBJECTS_ROOT = ROOT / "components"
SETS_ROOT = ROOT / "components"


class DocumentationGenerationTests(unittest.TestCase):
    def test_get_all_objects_documentation_returns_list(self):
        docs = get_all_objects_documentation(objects_root=OBJECTS_ROOT)
        self.assertIsInstance(docs, list)
        self.assertGreaterEqual(len(docs), 3)
        self.assertTrue(all(isinstance(item, dict) for item in docs))

    def test_object_doc_entry_has_required_keys(self):
        docs = get_all_objects_documentation(objects_root=OBJECTS_ROOT)
        self.assertGreaterEqual(len(docs), 1)
        required = {"command", "name_long", "description", "variables", "category", "summary"}
        for item in docs:
            self.assertTrue(required.issubset(item.keys()))
            self.assertIsInstance(item["command"], str)
            self.assertTrue(item["command"].strip())
            self.assertIsInstance(item["variables"], list)

    def test_get_all_part_sets_documentation_returns_list(self):
        docs = get_all_part_sets_documentation(sets_root=SETS_ROOT)
        self.assertIsInstance(docs, list)
        self.assertGreaterEqual(len(docs), 3)

    def test_export_json_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "documentation_data.json"
            export_documentation_json(output, objects_root=OBJECTS_ROOT, sets_root=SETS_ROOT)
            self.assertTrue(output.exists())

            payload = json.loads(output.read_text(encoding="utf-8"))
            for key in ["objects", "part_sets", "generated_date", "total_objects", "total_part_sets"]:
                self.assertIn(key, payload)

            self.assertGreaterEqual(payload["total_objects"], 3)
            self.assertGreaterEqual(payload["total_part_sets"], 3)

    def test_documentation_variable_structure(self):
        docs = get_all_objects_documentation(objects_root=OBJECTS_ROOT)
        target = None
        for item in docs:
            if item.get("command") == "circles":
                target = item
                break
        self.assertIsNotNone(target)
        variables = target.get("variables", [])
        self.assertGreaterEqual(len(variables), 1)
        for variable in variables:
            for key in ["name", "description", "type", "default"]:
                self.assertIn(key, variable)
            self.assertTrue(str(variable["name"]).strip())

    def test_export_html_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            template = tmp_path / "template.html"
            output = tmp_path / "documentation.html"
            template.write_text(
                "<html><body><!-- DOCUMENTATION_DATA_PLACEHOLDER --></body></html>",
                encoding="utf-8",
            )

            export_documentation_html(
                template,
                output,
                objects_root=OBJECTS_ROOT,
                sets_root=SETS_ROOT,
            )

            self.assertTrue(output.exists())
            text = output.read_text(encoding="utf-8")
            self.assertIn("DOCUMENTATION_DATA", text)
            self.assertIn("circles", text)

    def test_export_markdown_creates_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            objects_root = tmp_path / "objects"
            sets_root = tmp_path / "sets"

            obj_folder = objects_root / "sample"
            obj_folder.mkdir(parents=True)
            (obj_folder / "working.py").write_text(
                """
def define():
    return {
        "name": "sample",
        "name_short": ["sample"],
        "name_long": "Sample Object",
        "description": "Sample object description.",
        "category": "Sample",
        "variables": [{"name": "size", "description": "s", "type": "string", "default": "oobb"}],
    }

def action(**kwargs):
    return {"type": "sample", "components": []}
""".strip(),
                encoding="utf-8",
            )

            set_folder = sets_root / "sample_set"
            set_folder.mkdir(parents=True)
            (set_folder / "working.py").write_text(
                """
def define():
    return {
        "name": "sample_set",
        "name_long": "Sample Set",
        "description": "Sample set description.",
        "category": "Sample",
        "variables": ["size"],
    }

def items(size="oobb", **kwargs):
    return [{"type": "sample", "size": size}]
""".strip(),
                encoding="utf-8",
            )

            export_documentation_markdown(objects_root=objects_root, sets_root=sets_root)

            objects_index = objects_root / "README.md"
            sets_index = sets_root / "README.md"
            self.assertTrue(objects_index.exists())
            self.assertTrue(sets_index.exists())
            self.assertIn("|", objects_index.read_text(encoding="utf-8"))
            self.assertIn("sample", objects_index.read_text(encoding="utf-8"))
            self.assertIn("sample_set", sets_index.read_text(encoding="utf-8"))

    def test_per_folder_readme_generated(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            objects_root = tmp_path / "objects"
            sets_root = tmp_path / "sets"

            obj_folder = objects_root / "sample"
            obj_folder.mkdir(parents=True)
            (obj_folder / "working.py").write_text(
                """
def define():
    return {
        "name": "sample",
        "name_long": "Sample Object",
        "description": "Sample object description.",
        "category": "Sample",
        "variables": [{"name": "size", "description": "s", "type": "string", "default": "oobb"}],
    }

def action(**kwargs):
    return {"type": "sample", "components": []}
""".strip(),
                encoding="utf-8",
            )

            set_folder = sets_root / "sample_set"
            set_folder.mkdir(parents=True)
            (set_folder / "working.py").write_text(
                """
def define():
    return {
        "name": "sample_set",
        "name_long": "Sample Set",
        "description": "Sample set description.",
        "category": "Sample",
        "variables": ["size"],
    }

def items(size="oobb", **kwargs):
    return [{"type": "sample", "size": size}]
""".strip(),
                encoding="utf-8",
            )

            export_documentation_markdown(objects_root=objects_root, sets_root=sets_root)

            object_readme = obj_folder / "README.md"
            set_readme = set_folder / "README.md"
            self.assertTrue(object_readme.exists())
            self.assertTrue(set_readme.exists())

            object_text = object_readme.read_text(encoding="utf-8")
            set_text = set_readme.read_text(encoding="utf-8")

            self.assertIn("Sample object description.", object_text)
            self.assertIn("| Name | Description | Type | Default |", object_text)
            self.assertIn("Sample set description.", set_text)
            self.assertIn("| Name | Description | Type | Default |", set_text)


if __name__ == "__main__":
    unittest.main()
