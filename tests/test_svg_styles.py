"""
tests/test_svg_styles.py

Unit and integration tests for svg_styles.py.
"""

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tempfile

import svg_styles
import opsvg


# ── TestDefaultStyles ─────────────────────────────────────────────────────────

class TestDefaultStyles(unittest.TestCase):

    def test_returns_dict(self):
        self.assertIsInstance(svg_styles.default_styles(), dict)

    def test_has_required_names(self):
        styles = svg_styles.default_styles()
        for name in ("plate", "hole", "label", "header", "outline", "engraved"):
            self.assertIn(name, styles, f"Expected '{name}' in default_styles()")

    def test_returns_copy(self):
        s1 = svg_styles.default_styles()
        s2 = svg_styles.default_styles()
        s1["plate"]["color"] = "#MUTATED"
        self.assertNotEqual(s2["plate"]["color"], "#MUTATED",
            "default_styles() should return a fresh copy each time")

    def test_plate_has_color_and_stroke(self):
        styles = svg_styles.default_styles()
        plate  = styles["plate"]
        self.assertIn("color",  plate)
        self.assertIn("stroke", plate)

    def test_label_has_text_props(self):
        styles = svg_styles.default_styles()
        label  = styles["label"]
        for key in ("font", "size", "halign", "valign"):
            self.assertIn(key, label, f"label style missing '{key}'")


# ── TestGetStylesheet ─────────────────────────────────────────────────────────

class TestGetStylesheet(unittest.TestCase):

    def test_default_name(self):
        sheet = svg_styles.get_stylesheet("default")
        self.assertIsInstance(sheet, dict)
        self.assertIn("plate", sheet)

    def test_jazzy_name(self):
        sheet = svg_styles.get_stylesheet("jazzy")
        self.assertIsInstance(sheet, dict)
        self.assertIn("plate", sheet)

    def test_jazzy_has_different_colors_from_default(self):
        d = svg_styles.get_stylesheet("default")
        j = svg_styles.get_stylesheet("jazzy")
        self.assertNotEqual(d["plate"]["color"], j["plate"]["color"],
            "Default and Jazzy should have different plate colors")

    def test_unknown_name_falls_back_to_default(self):
        sheet = svg_styles.get_stylesheet("__nonexistent__")
        # Should not raise; returns DEFAULT
        self.assertIsInstance(sheet, dict)
        self.assertIn("plate", sheet)

    def test_returns_copy(self):
        s1 = svg_styles.get_stylesheet("default")
        s2 = svg_styles.get_stylesheet("default")
        s1["plate"]["color"] = "#MUTATED"
        self.assertNotEqual(s2["plate"]["color"], "#MUTATED")

    def test_all_registered_names(self):
        for name in svg_styles.STYLESHEETS:
            sheet = svg_styles.get_stylesheet(name)
            self.assertIsInstance(sheet, dict)
            self.assertIn("plate", sheet, f"Stylesheet '{name}' missing 'plate'")


# ── TestResolve ───────────────────────────────────────────────────────────────

class TestResolve(unittest.TestCase):

    def setUp(self):
        self.styles = svg_styles.default_styles()

    def test_known_style(self):
        result = svg_styles.resolve("plate", self.styles)
        self.assertIsInstance(result, dict)
        self.assertIn("color", result)

    def test_unknown_style_returns_empty(self):
        result = svg_styles.resolve("__missing__", self.styles)
        self.assertEqual(result, {})

    def test_dot_notation_inherits_base(self):
        result = svg_styles.resolve("plate.accent", self.styles)
        # Should contain base keys like stroke (from "plate") + color (from "plate.accent")
        self.assertIn("color",  result)
        self.assertIn("stroke", result)

    def test_dot_notation_variant_wins_over_base(self):
        styles = svg_styles.default_styles()
        styles["plate"]        = {"color": "#AAAAAA", "stroke": "none"}
        styles["plate.accent"] = {"color": "#E85D04"}
        result = svg_styles.resolve("plate.accent", styles)
        self.assertEqual(result["color"], "#E85D04",
            "Variant color should win over base color")
        self.assertEqual(result["stroke"], "none",
            "Base stroke should be inherited when variant doesn't set it")

    def test_dot_notation_missing_variant_returns_base(self):
        result = svg_styles.resolve("plate.__nonexistent__", self.styles)
        # base only
        self.assertIn("color", result)

    def test_dot_notation_missing_base_returns_variant_only(self):
        styles = {"plate.onlyvariant": {"color": "#FF0000"}}
        result = svg_styles.resolve("plate.onlyvariant", styles)
        self.assertEqual(result["color"], "#FF0000")

    def test_returns_copy(self):
        r1 = svg_styles.resolve("plate", self.styles)
        r1["color"] = "#MUTATED"
        r2 = svg_styles.resolve("plate", self.styles)
        self.assertNotEqual(r2.get("color"), "#MUTATED")

    def test_label_dot_small_overrides_size(self):
        result = svg_styles.resolve("label.small", self.styles)
        base   = svg_styles.resolve("label",       self.styles)
        self.assertNotEqual(result["size"], base["size"],
            "label.small should have a different size than label")
        self.assertEqual(result["font"], base["font"],
            "label.small should inherit font from label")


# ── TestMerge ─────────────────────────────────────────────────────────────────

class TestMerge(unittest.TestCase):

    def test_returns_new_dict(self):
        base      = svg_styles.default_styles()
        overrides = {"plate": {"color": "#NEW"}}
        result    = svg_styles.merge(base, overrides)
        self.assertIsNot(result, base)

    def test_does_not_mutate_base(self):
        base      = svg_styles.default_styles()
        original  = base["plate"]["color"]
        svg_styles.merge(base, {"plate": {"color": "#CHANGED"}})
        self.assertEqual(base["plate"]["color"], original)

    def test_does_not_mutate_overrides(self):
        base      = svg_styles.default_styles()
        overrides = {"plate": {"color": "#NEW"}}
        svg_styles.merge(base, overrides)
        self.assertEqual(overrides["plate"]["color"], "#NEW")  # unchanged

    def test_overrides_single_property(self):
        result = svg_styles.merge(
            svg_styles.default_styles(),
            {"plate": {"color": "#E85D04"}},
        )
        self.assertEqual(result["plate"]["color"], "#E85D04")

    def test_preserves_unmentioned_styles(self):
        result = svg_styles.merge(
            svg_styles.default_styles(),
            {"plate": {"color": "#E85D04"}},
        )
        self.assertIn("hole",   result)
        self.assertIn("label",  result)
        self.assertIn("header", result)

    def test_preserves_unmentioned_properties_in_overridden_style(self):
        original_stroke = svg_styles.default_styles()["plate"]["stroke"]
        result = svg_styles.merge(
            svg_styles.default_styles(),
            {"plate": {"color": "#NEW"}},
        )
        self.assertEqual(result["plate"]["stroke"], original_stroke)

    def test_adds_new_style_name(self):
        result = svg_styles.merge(
            svg_styles.default_styles(),
            {"my_custom": {"color": "#ABCDEF"}},
        )
        self.assertIn("my_custom", result)
        self.assertEqual(result["my_custom"]["color"], "#ABCDEF")


# ── TestSetStyle ──────────────────────────────────────────────────────────────

class TestSetStyle(unittest.TestCase):

    def test_creates_styles_key_when_absent(self):
        thing = {}
        svg_styles.set_style(thing, "plate", {"color": "#FF0000"})
        self.assertIn("styles", thing)

    def test_overrides_single_property(self):
        thing = {"styles": svg_styles.default_styles()}
        svg_styles.set_style(thing, "plate", {"color": "#FF0000"})
        self.assertEqual(thing["styles"]["plate"]["color"], "#FF0000")

    def test_preserves_other_properties(self):
        thing = {"styles": svg_styles.default_styles()}
        original_stroke = thing["styles"]["plate"]["stroke"]
        svg_styles.set_style(thing, "plate", {"color": "#FF0000"})
        self.assertEqual(thing["styles"]["plate"]["stroke"], original_stroke)

    def test_adds_new_style_name(self):
        thing = {"styles": svg_styles.default_styles()}
        svg_styles.set_style(thing, "my_style", {"color": "#123456"})
        self.assertIn("my_style", thing["styles"])
        self.assertEqual(thing["styles"]["my_style"]["color"], "#123456")

    def test_multiple_calls_accumulate(self):
        thing = {"styles": svg_styles.default_styles()}
        svg_styles.set_style(thing, "plate", {"color": "#111111"})
        svg_styles.set_style(thing, "plate", {"stroke": "#E85D04"})
        self.assertEqual(thing["styles"]["plate"]["color"],  "#111111")
        self.assertEqual(thing["styles"]["plate"]["stroke"], "#E85D04")


# ── TestApply ─────────────────────────────────────────────────────────────────

class TestApply(unittest.TestCase):

    def setUp(self):
        self.styles = svg_styles.default_styles()

    def test_returns_style_properties(self):
        result = svg_styles.apply("plate", self.styles)
        self.assertIn("color", result)

    def test_inline_beats_style(self):
        result = svg_styles.apply("plate", self.styles, color="#FF0000")
        self.assertEqual(result["color"], "#FF0000")

    def test_inline_extends_style(self):
        result = svg_styles.apply("plate", self.styles, my_extra="value")
        self.assertIn("my_extra", result)
        self.assertIn("color",    result)   # style property still present

    def test_unknown_style_returns_only_inline(self):
        result = svg_styles.apply("__unknown__", self.styles, color="#FF0000")
        self.assertEqual(result["color"], "#FF0000")
        self.assertEqual(len(result), 1)


# ── Integration: se() with style= kwarg ────────────────────────────────────

class TestSeStyleIntegration(unittest.TestCase):
    """Verify that opsvg.se() correctly resolves style= before dispatch."""

    def _make_thing(self):
        thing = {"svg_components": [], "styles": svg_styles.default_styles()}
        return thing

    def test_se_with_style_applies_color(self):
        thing = self._make_thing()
        plate_color = thing["styles"]["plate"]["color"]
        opsvg.se(thing, shape="rect", style="plate", size=[10, 10, 3], pos=[0, 0, 0])
        self.assertEqual(len(thing["svg_components"]), 1)
        desc = thing["svg_components"][0]
        self.assertEqual(desc["color"], plate_color)

    def test_se_inline_beats_style(self):
        thing = self._make_thing()
        opsvg.se(thing, shape="rect", style="plate",
                 size=[10, 10, 3], pos=[0, 0, 0], color="#FF0000")
        desc = thing["svg_components"][0]
        self.assertEqual(desc["color"], "#FF0000",
            "Inline color should beat the style's color")

    def test_se_style_kwarg_stripped_from_descriptor(self):
        thing = self._make_thing()
        opsvg.se(thing, shape="rect", style="plate", size=[10, 10, 3], pos=[0, 0, 0])
        desc = thing["svg_components"][0]
        self.assertNotIn("style", desc,
            "'style' key must be stripped before reaching the descriptor")

    def test_se_dot_notation_style(self):
        thing = self._make_thing()
        opsvg.se(thing, shape="rect", style="plate.accent", size=[10, 10, 3], pos=[0, 0, 0])
        desc  = thing["svg_components"][0]
        expected = svg_styles.resolve("plate.accent", thing["styles"])["color"]
        self.assertEqual(desc["color"], expected)

    def test_se_text_style_applies_font(self):
        thing = self._make_thing()
        opsvg.se(thing, shape="text", style="label", text="Hello", pos=[0, 0, 0])
        desc = thing["svg_components"][0]
        self.assertIn("font", desc)

    def test_se_unknown_style_does_not_crash(self):
        thing = self._make_thing()
        try:
            opsvg.se(thing, shape="rect", style="__nonexistent__",
                     size=[10, 10, 3], pos=[0, 0, 0])
        except Exception as exc:
            self.fail(f"se() with unknown style raised: {exc}")

    def test_se_no_style_kwarg_still_works(self):
        thing = self._make_thing()
        opsvg.se(thing, shape="rect", color="#333333", size=[10, 10, 3], pos=[0, 0, 0])
        self.assertEqual(len(thing["svg_components"]), 1)


# ── TestGetStylesheetArray ────────────────────────────────────────────────────

class TestGetStylesheetArray(unittest.TestCase):
    """get_stylesheet() accepting a list of names for cascade merging."""

    def test_list_single_element_same_as_string(self):
        by_str  = svg_styles.get_stylesheet("default")
        by_list = svg_styles.get_stylesheet(["default"])
        self.assertEqual(by_str["plate"]["color"], by_list["plate"]["color"])

    def test_list_later_overrides_earlier(self):
        # Build a two-entry list: "default" then a tiny override sheet
        # We test with two real built-ins: default + jazzy should give jazzy colors
        merged = svg_styles.get_stylesheet(["default", "jazzy"])
        jazzy  = svg_styles.get_stylesheet("jazzy")
        self.assertEqual(merged["plate"]["color"], jazzy["plate"]["color"],
            "Last stylesheet in list should win for overlapping properties")

    def test_list_preserves_base_keys_not_in_later(self):
        # jazzy doesn't define every key that default does (label.muted etc.)
        merged  = svg_styles.get_stylesheet(["default", "jazzy"])
        default = svg_styles.get_stylesheet("default")
        # Both have "engraved.light"; check it came from jazzy (last wins)
        self.assertIn("engraved.light", merged)

    def test_list_empty_returns_empty_dict(self):
        result = svg_styles.get_stylesheet([])
        self.assertIsInstance(result, dict)

    def test_tuple_also_accepted(self):
        result = svg_styles.get_stylesheet(("default", "jazzy"))
        self.assertIsInstance(result, dict)
        self.assertIn("plate", result)

    def test_list_returns_copy(self):
        r1 = svg_styles.get_stylesheet(["default", "jazzy"])
        r2 = svg_styles.get_stylesheet(["default", "jazzy"])
        r1["plate"]["color"] = "#MUTATED"
        self.assertNotEqual(r2["plate"]["color"], "#MUTATED")


# ── TestYamlStyleFiles ────────────────────────────────────────────────────────

class TestYamlStyleFiles(unittest.TestCase):
    """Loading stylesheets from styles/*.yaml files."""

    STYLES_DIR = ROOT / "styles"
    EXPECTED_FILES = ["blueprint", "high_contrast", "neon", "pastel", "minimal"]

    def test_styles_dir_exists(self):
        self.assertTrue(self.STYLES_DIR.is_dir(),
            f"styles/ directory not found at {self.STYLES_DIR}")

    def test_expected_yaml_files_present(self):
        for name in self.EXPECTED_FILES:
            p = self.STYLES_DIR / f"{name}.yaml"
            self.assertTrue(p.exists(), f"styles/{name}.yaml not found")

    def test_each_yaml_loads_successfully(self):
        for name in self.EXPECTED_FILES:
            with self.subTest(stylesheet=name):
                try:
                    sheet = svg_styles.get_stylesheet(name)
                except Exception as exc:
                    self.fail(f"{name}.yaml failed to load: {exc}")
                self.assertIsInstance(sheet, dict)

    def test_yaml_sheets_have_plate_style(self):
        for name in self.EXPECTED_FILES:
            with self.subTest(stylesheet=name):
                sheet = svg_styles.get_stylesheet(name)
                self.assertIn("plate", sheet,
                    f"{name} stylesheet missing 'plate' style")

    def test_yaml_sheets_have_label_style(self):
        for name in self.EXPECTED_FILES:
            with self.subTest(stylesheet=name):
                sheet = svg_styles.get_stylesheet(name)
                self.assertIn("label", sheet,
                    f"{name} stylesheet missing 'label' style")

    def test_yaml_plate_color_is_string(self):
        for name in self.EXPECTED_FILES:
            with self.subTest(stylesheet=name):
                sheet = svg_styles.get_stylesheet(name)
                color = sheet["plate"].get("color", "")
                self.assertIsInstance(color, str,
                    f"{name} plate.color should be a string")

    def test_each_yaml_is_distinct_from_default(self):
        default_plate = svg_styles.get_stylesheet("default")["plate"]["color"]
        for name in self.EXPECTED_FILES:
            with self.subTest(stylesheet=name):
                sheet = svg_styles.get_stylesheet(name)
                self.assertNotEqual(sheet["plate"]["color"], default_plate,
                    f"{name} plate color should differ from default")

    def test_load_from_custom_dir(self):
        """get_stylesheet looks in extra styles_dir before built-ins."""
        with tempfile.TemporaryDirectory() as tmp:
            import yaml
            yaml_path = Path(tmp) / "custom.yaml"
            yaml_path.write_text(
                "meta:\n  name: Custom\nplate:\n  color: \"#ABCDEF\"\n",
                encoding="utf-8"
            )
            sheet = svg_styles.get_stylesheet("custom", styles_dir=tmp)
            self.assertEqual(sheet["plate"]["color"], "#ABCDEF")

    def test_custom_dir_shadows_builtin(self):
        """A file named 'default.yaml' in styles_dir overrides the built-in."""
        with tempfile.TemporaryDirectory() as tmp:
            yaml_path = Path(tmp) / "default.yaml"
            yaml_path.write_text(
                "plate:\n  color: \"#OVERRIDDEN\"\n",
                encoding="utf-8"
            )
            sheet = svg_styles.get_stylesheet("default", styles_dir=tmp)
            self.assertEqual(sheet["plate"]["color"], "#OVERRIDDEN")


# ── TestListAvailableStylesheets ─────────────────────────────────────────────

class TestListAvailableStylesheets(unittest.TestCase):

    def test_returns_list(self):
        result = svg_styles.list_available_stylesheets()
        self.assertIsInstance(result, list)

    def test_at_least_seven_entries(self):
        # 2 built-in + 5 yaml files
        result = svg_styles.list_available_stylesheets()
        self.assertGreaterEqual(len(result), 7)

    def test_each_entry_has_required_keys(self):
        for entry in svg_styles.list_available_stylesheets():
            with self.subTest(name=entry.get("name")):
                for key in ("name", "label", "description", "source", "styles"):
                    self.assertIn(key, entry)

    def test_default_and_jazzy_present(self):
        names = {e["name"] for e in svg_styles.list_available_stylesheets()}
        self.assertIn("default", names)
        self.assertIn("jazzy",   names)

    def test_yaml_sheets_present(self):
        names = {e["name"] for e in svg_styles.list_available_stylesheets()}
        for expected in ("blueprint", "neon", "pastel", "minimal", "high_contrast"):
            self.assertIn(expected, names)

    def test_builtin_source_correct(self):
        entries = {e["name"]: e for e in svg_styles.list_available_stylesheets()}
        self.assertEqual(entries["default"]["source"], "builtin")
        self.assertEqual(entries["jazzy"]["source"],   "builtin")

    def test_file_source_correct(self):
        entries = {e["name"]: e for e in svg_styles.list_available_stylesheets()}
        for name in ("blueprint", "neon", "pastel"):
            self.assertEqual(entries[name]["source"], "file",
                f"{name} should have source='file'")

    def test_labels_are_non_empty(self):
        for entry in svg_styles.list_available_stylesheets():
            with self.subTest(name=entry["name"]):
                self.assertTrue(entry["label"].strip(),
                    f"{entry['name']} has empty label")


# ── Integration: get_default_thing seeds styles ────────────────────────────

class TestGetDefaultThingStyles(unittest.TestCase):

    def test_thing_has_styles_key(self):
        import svg_help
        thing = svg_help.get_default_thing()
        self.assertIn("styles", thing)

    def test_default_thing_uses_default_stylesheet(self):
        import svg_help
        thing  = svg_help.get_default_thing()
        expect = svg_styles.default_styles()["plate"]["color"]
        self.assertEqual(thing["styles"]["plate"]["color"], expect)

    def test_jazzy_stylesheet_via_kwarg(self):
        import svg_help
        thing  = svg_help.get_default_thing(stylesheet="jazzy")
        jazzy  = svg_styles.get_stylesheet("jazzy")["plate"]["color"]
        self.assertEqual(thing["styles"]["plate"]["color"], jazzy)

    def test_array_stylesheet_via_kwarg(self):
        import svg_help
        thing  = svg_help.get_default_thing(stylesheet=["default", "jazzy"])
        jazzy  = svg_styles.get_stylesheet("jazzy")["plate"]["color"]
        self.assertEqual(thing["styles"]["plate"]["color"], jazzy,
            "Array stylesheet: last entry should win")

    def test_part_styles_override(self):
        import svg_help
        thing = svg_help.get_default_thing(part_styles={"plate": {"color": "#ABCDEF"}})
        self.assertEqual(thing["styles"]["plate"]["color"], "#ABCDEF")


# ── TestLineWeights ───────────────────────────────────────────────────────────

class TestLineWeights(unittest.TestCase):
    """Verify line/outline/plate weight variants resolve correctly."""

    WEIGHT_NAMES = ("hairline", "thin", "thick", "heavy")
    # Expected stroke widths for each weight label (tolerance ±0.001)
    EXPECTED_WIDTHS = {
        "hairline": 0.1,
        "thin":     0.25,
        "thick":    1.0,
        "heavy":    2.0,
    }

    def _check_widths(self, base_name, sheet):
        """Resolve base.weight and confirm stroke_width matches the scale."""
        for weight, expected in self.EXPECTED_WIDTHS.items():
            style_name = f"{base_name}.{weight}"
            result = svg_styles.resolve(style_name, sheet)
            self.assertIn("stroke_width", result,
                f"'{style_name}' missing stroke_width")
            self.assertAlmostEqual(result["stroke_width"], expected, places=3,
                msg=f"'{style_name}' stroke_width should be {expected}, got {result['stroke_width']}")

    # ── default stylesheet ────────────────────────────────────────────────────

    def test_default_line_weights(self):
        self._check_widths("line", svg_styles.default_styles())

    def test_default_outline_weights(self):
        self._check_widths("outline", svg_styles.default_styles())

    def test_default_plate_weights(self):
        self._check_widths("plate", svg_styles.default_styles())

    def test_default_line_base_is_stroke_only(self):
        result = svg_styles.resolve("line", svg_styles.default_styles())
        self.assertEqual(result.get("color"), "none",
            "line base should have color='none' (pure stroke)")
        self.assertNotEqual(result.get("stroke"), "none",
            "line base should have a visible stroke color")

    def test_default_line_accent_inherits_width(self):
        """line.accent should keep the base stroke_width."""
        base   = svg_styles.resolve("line", svg_styles.default_styles())
        accent = svg_styles.resolve("line.accent", svg_styles.default_styles())
        self.assertEqual(accent["stroke_width"], base["stroke_width"])

    def test_default_outline_weight_inherits_stroke_color(self):
        """outline.thick should use the same stroke color as outline."""
        base  = svg_styles.resolve("outline", svg_styles.default_styles())
        thick = svg_styles.resolve("outline.thick", svg_styles.default_styles())
        self.assertEqual(thick["stroke"], base["stroke"],
            "outline.thick should inherit stroke color from outline base")

    def test_default_plate_weight_adds_stroke(self):
        """plate.thin should override stroke: none from plate base."""
        thin = svg_styles.resolve("plate.thin", svg_styles.default_styles())
        self.assertNotEqual(thin.get("stroke"), "none",
            "plate.thin should have a visible stroke (not 'none')")

    # ── jazzy stylesheet ──────────────────────────────────────────────────────

    def test_jazzy_line_weights(self):
        self._check_widths("line", svg_styles.get_stylesheet("jazzy"))

    def test_jazzy_outline_weights(self):
        self._check_widths("outline", svg_styles.get_stylesheet("jazzy"))

    def test_jazzy_plate_weights(self):
        self._check_widths("plate", svg_styles.get_stylesheet("jazzy"))

    # ── YAML stylesheets ──────────────────────────────────────────────────────

    YAML_SHEETS = ("blueprint", "high_contrast", "neon", "pastel", "minimal")

    def test_yaml_sheets_have_line_weights(self):
        for name in self.YAML_SHEETS:
            with self.subTest(sheet=name):
                sheet = svg_styles.get_stylesheet(name)
                self._check_widths("line", sheet)

    def test_yaml_sheets_have_outline_weights(self):
        for name in self.YAML_SHEETS:
            with self.subTest(sheet=name):
                sheet = svg_styles.get_stylesheet(name)
                self._check_widths("outline", sheet)

    def test_yaml_sheets_have_plate_weights(self):
        for name in self.YAML_SHEETS:
            with self.subTest(sheet=name):
                sheet = svg_styles.get_stylesheet(name)
                self._check_widths("plate", sheet)

    def test_yaml_line_base_is_stroke_only(self):
        for name in self.YAML_SHEETS:
            with self.subTest(sheet=name):
                sheet  = svg_styles.get_stylesheet(name)
                result = svg_styles.resolve("line", sheet)
                self.assertEqual(result.get("color"), "none",
                    f"[{name}] line base should have color='none'")

    def test_yaml_outline_weight_inherits_stroke_color(self):
        for name in self.YAML_SHEETS:
            with self.subTest(sheet=name):
                sheet  = svg_styles.get_stylesheet(name)
                base   = svg_styles.resolve("outline", sheet)
                thick  = svg_styles.resolve("outline.thick", sheet)
                self.assertEqual(thick["stroke"], base["stroke"],
                    f"[{name}] outline.thick should inherit stroke color from outline")

    def test_weight_scale_is_monotonically_increasing(self):
        """hairline < thin < default < thick < heavy for every sheet."""
        for name in ("default", "jazzy") + self.YAML_SHEETS:
            with self.subTest(sheet=name):
                sheet = svg_styles.get_stylesheet(name)
                hairline = svg_styles.resolve("line.hairline", sheet)["stroke_width"]
                thin     = svg_styles.resolve("line.thin",     sheet)["stroke_width"]
                thick    = svg_styles.resolve("line.thick",    sheet)["stroke_width"]
                heavy    = svg_styles.resolve("line.heavy",    sheet)["stroke_width"]
                self.assertLess(hairline, thin,  f"[{name}] hairline < thin")
                self.assertLess(thin,     thick, f"[{name}] thin < thick")
                self.assertLess(thick,    heavy, f"[{name}] thick < heavy")


if __name__ == "__main__":
    unittest.main()
