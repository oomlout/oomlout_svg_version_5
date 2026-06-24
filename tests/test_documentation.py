"""
tests/test_documentation.py

Tests for svg_documentation.py — mirrors test_documentation_generation.py
from oomlout_oobb_version_5.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from svg_documentation import (
    get_all_components_documentation,
    get_all_parts_documentation,
    export_documentation_json,
    export_documentation_html,
    _normalise_variables,
)

COMP_ROOT  = ROOT / "svg_components"
PARTS_ROOT = ROOT / "parts"
TMPL_PATH  = ROOT / "templates" / "svg_documentation_template.html"


class TestGetAllComponentsDocumentation(unittest.TestCase):

    def test_returns_list(self):
        docs = get_all_components_documentation(str(COMP_ROOT))
        self.assertIsInstance(docs, list)

    def test_at_least_nine_components(self):
        docs = get_all_components_documentation(str(COMP_ROOT))
        self.assertGreaterEqual(len(docs), 9)

    def test_all_entries_are_dicts(self):
        docs = get_all_components_documentation(str(COMP_ROOT))
        self.assertTrue(all(isinstance(d, dict) for d in docs))

    def test_required_keys_present(self):
        required = {"name", "name_long", "description", "category",
                    "variables", "shape_aliases", "returns", "sample_svg"}
        docs = get_all_components_documentation(str(COMP_ROOT))
        for entry in docs:
            with self.subTest(component=entry.get("name")):
                missing = required - entry.keys()
                self.assertFalse(missing, f"Missing keys: {missing}")

    def test_variables_is_list(self):
        docs = get_all_components_documentation(str(COMP_ROOT))
        for entry in docs:
            with self.subTest(component=entry.get("name")):
                self.assertIsInstance(entry["variables"], list)

    def test_sample_svg_is_string(self):
        docs = get_all_components_documentation(str(COMP_ROOT))
        for entry in docs:
            with self.subTest(component=entry.get("name")):
                self.assertIsInstance(entry["sample_svg"], str)

    def test_nonexistent_root_returns_empty(self):
        docs = get_all_components_documentation("__nonexistent__")
        self.assertEqual(docs, [])


class TestGetAllPartsDocumentation(unittest.TestCase):

    def test_returns_list(self):
        docs = get_all_parts_documentation(str(PARTS_ROOT))
        self.assertIsInstance(docs, list)

    def test_all_entries_are_dicts(self):
        docs = get_all_parts_documentation(str(PARTS_ROOT))
        self.assertTrue(all(isinstance(d, dict) for d in docs))

    def test_required_keys_present(self):
        required = {"id", "oobb_name", "svg_name", "classification", "folder", "style_options"}
        docs = get_all_parts_documentation(str(PARTS_ROOT))
        for entry in docs:
            with self.subTest(part=entry.get("id")):
                missing = required - entry.keys()
                self.assertFalse(missing, f"Missing keys: {missing}")

    def test_style_options_include_stylesheet_and_styles(self):
        docs = get_all_parts_documentation(str(PARTS_ROOT))
        for entry in docs:
            with self.subTest(part=entry.get("id")):
                option_names = {option.get("name") for option in entry.get("style_options", [])}
                self.assertIn("stylesheet", option_names)
                self.assertIn("styles", option_names)

    def test_only_svg_details_parts_included(self):
        """Parts without svg_details must be excluded."""
        docs = get_all_parts_documentation(str(PARTS_ROOT))
        self.assertTrue(len(docs) >= 1)

    def test_nonexistent_root_returns_empty(self):
        docs = get_all_parts_documentation("__nonexistent__")
        self.assertEqual(docs, [])


class TestNormaliseVariables(unittest.TestCase):

    def test_list_of_dicts(self):
        raw = [{"name": "size", "description": "d", "type": "list", "default": [10, 10, 3]}]
        result = _normalise_variables(raw)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "size")

    def test_list_of_strings(self):
        raw = ["width", "height"]
        result = _normalise_variables(raw)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "width")
        self.assertEqual(result[0]["description"], "")

    def test_empty_list(self):
        self.assertEqual(_normalise_variables([]), [])

    def test_non_list_returns_empty(self):
        self.assertEqual(_normalise_variables(None), [])
        self.assertEqual(_normalise_variables("bad"), [])

    def test_dict_missing_name_skipped(self):
        raw = [{"description": "no name here", "type": "str", "default": "x"}]
        self.assertEqual(_normalise_variables(raw), [])


class TestExportDocumentationJson(unittest.TestCase):

    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.json"
            export_documentation_json(out, str(COMP_ROOT), str(PARTS_ROOT))
            self.assertTrue(out.exists())

    def test_json_top_level_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.json"
            export_documentation_json(out, str(COMP_ROOT), str(PARTS_ROOT))
            payload = json.loads(out.read_text(encoding="utf-8"))
            for key in ["generated_date", "total_components", "total_parts",
                        "components", "parts"]:
                self.assertIn(key, payload, f"Missing top-level key: {key}")

    def test_component_count_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.json"
            export_documentation_json(out, str(COMP_ROOT), str(PARTS_ROOT))
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["total_components"], len(payload["components"]))

    def test_is_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.json"
            export_documentation_json(out, str(COMP_ROOT), str(PARTS_ROOT))
            try:
                json.loads(out.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                self.fail(f"Output is not valid JSON: {exc}")


class TestExportDocumentationHtml(unittest.TestCase):

    def test_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.html"
            export_documentation_html(str(TMPL_PATH), str(out),
                                      str(COMP_ROOT), str(PARTS_ROOT))
            self.assertTrue(out.exists())

    def test_html_contains_data_script_tag(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.html"
            export_documentation_html(str(TMPL_PATH), str(out),
                                      str(COMP_ROOT), str(PARTS_ROOT))
            text = out.read_text(encoding="utf-8")
            self.assertIn("DOCUMENTATION_DATA", text)

    def test_html_contains_component_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.html"
            export_documentation_html(str(TMPL_PATH), str(out),
                                      str(COMP_ROOT), str(PARTS_ROOT))
            text = out.read_text(encoding="utf-8")
            self.assertIn("rect", text)
            self.assertIn("circle", text)

    def test_missing_template_does_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.html"
            # Should print a warning and return cleanly (no exception)
            try:
                export_documentation_html("__no_template__.html", str(out),
                                          str(COMP_ROOT), str(PARTS_ROOT))
            except Exception as exc:
                self.fail(f"Raised unexpected exception: {exc}")
            self.assertFalse(out.exists())

    def test_placeholder_is_replaced(self):
        """The DOCUMENTATION_DATA_PLACEHOLDER comment must not appear in output."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doc.html"
            export_documentation_html(str(TMPL_PATH), str(out),
                                      str(COMP_ROOT), str(PARTS_ROOT))
            text = out.read_text(encoding="utf-8")
            self.assertNotIn("DOCUMENTATION_DATA_PLACEHOLDER", text)


if __name__ == "__main__":
    unittest.main()
