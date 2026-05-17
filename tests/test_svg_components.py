"""
tests/test_svg_components.py

Tests the component contract for every working.py in svg_components/.
Each component must expose define() and action() meeting the expected interface.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT       = Path(__file__).resolve().parents[1]
COMP_ROOT  = ROOT / "svg_components"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ── helpers ───────────────────────────────────────────────────────────────────

def _all_component_dirs():
    return sorted(
        d for d in COMP_ROOT.iterdir()
        if d.is_dir() and (d / "working.py").exists()
    )


def _load(component_dir: Path):
    working_py  = component_dir / "working.py"
    module_name = f"_test_comp_{component_dir.name}"
    spec   = importlib.util.spec_from_file_location(module_name, working_py)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


COMPONENT_DIRS = _all_component_dirs()
COMPONENT_NAMES = [d.name for d in COMPONENT_DIRS]

# Minimal action kwargs that work for every component
_SAFE_KWARGS = {
    "pos":      [0, 0, 0],
    "color":    "#333333",
    "width":    2,
    "height":   2,
    "r":        5.0,
    "w":        20.0,
    "size":     [20, 15, 3],
    "diameter": 3,
    "text":     "test",
    "font":     "sans-serif",
    "halign":   "center",
    "valign":   "center",
    "points":   [[0, 8], [-8, -6], [8, -6]],
}


# ── test cases ────────────────────────────────────────────────────────────────

class TestComponentContract(unittest.TestCase):

    def test_expected_component_count(self):
        self.assertGreaterEqual(len(COMPONENT_DIRS), 9,
            "Expected at least 9 svg_components, found fewer.")

    def test_every_component_has_working_py(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                self.assertTrue((d / "working.py").exists())

    def test_every_component_loads(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                try:
                    _load(d)
                except Exception as exc:
                    self.fail(f"{d.name}: import failed — {exc}")

    def test_every_component_has_define(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module = _load(d)
                self.assertTrue(callable(getattr(module, "define", None)),
                    f"{d.name}: missing callable define()")

    def test_define_returns_required_keys(self):
        required = {"name", "name_long", "description", "category", "variables"}
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module = _load(d)
                meta   = module.define()
                self.assertIsInstance(meta, dict)
                missing = required - meta.keys()
                self.assertFalse(missing,
                    f"{d.name}: define() missing keys {missing}")

    def test_define_variables_is_list(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module = _load(d)
                meta   = module.define()
                self.assertIsInstance(meta.get("variables"), list,
                    f"{d.name}: define()['variables'] must be a list")

    def test_variable_entries_have_required_keys(self):
        required = {"name", "description", "type", "default"}
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module = _load(d)
                meta   = module.define()
                for var in meta.get("variables", []):
                    if not isinstance(var, dict):
                        continue
                    missing = required - var.keys()
                    self.assertFalse(missing,
                        f"{d.name}: variable entry missing keys {missing}")

    def test_every_component_has_action(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module = _load(d)
                self.assertTrue(callable(getattr(module, "action", None)),
                    f"{d.name}: missing callable action()")

    def test_action_returns_list(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module      = _load(d)
                descriptors = module.action(**_SAFE_KWARGS)
                self.assertIsInstance(descriptors, list,
                    f"{d.name}: action() must return a list")
                self.assertGreater(len(descriptors), 0,
                    f"{d.name}: action() returned empty list")

    def test_action_descriptors_have_shape_and_pos(self):
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module      = _load(d)
                descriptors = module.action(**_SAFE_KWARGS)
                for desc in descriptors:
                    self.assertIn("shape", desc,
                        f"{d.name}: descriptor missing 'shape' key")
                    self.assertIn("pos",   desc,
                        f"{d.name}: descriptor missing 'pos' key")

    def test_no_type_key_in_descriptors(self):
        """type (positive/negative) has been removed from the pipeline."""
        for d in COMPONENT_DIRS:
            with self.subTest(component=d.name):
                module      = _load(d)
                descriptors = module.action(**_SAFE_KWARGS)
                for desc in descriptors:
                    self.assertNotIn("type", desc,
                        f"{d.name}: descriptor still contains 'type' key — should be removed")


if __name__ == "__main__":
    unittest.main()
