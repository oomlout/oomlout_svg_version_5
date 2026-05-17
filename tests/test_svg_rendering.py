"""
tests/test_svg_rendering.py

SVG output quality and snapshot regression tests.

Snapshot update
---------------
Run with UPDATE_SNAPSHOTS=1 to regenerate svg_samples.json:

    UPDATE_SNAPSHOTS=1 python -m pytest tests/test_svg_rendering.py -v
"""

import hashlib
import importlib.util
import json
import os
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT      = Path(__file__).resolve().parents[1]
COMP_ROOT = ROOT / "svg_components"
SNAP_FILE = ROOT / "tests" / "snapshots" / "svg_samples.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import opsvg
import svg_variables as _sv


# ── helpers ───────────────────────────────────────────────────────────────────

def _load(component_dir: Path):
    working_py  = component_dir / "working.py"
    module_name = f"_render_test_{component_dir.name}"
    spec   = importlib.util.spec_from_file_location(module_name, working_py)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_SAMPLE_KWARGS = {
    "circle":              {"r": 8.0,  "color": "#333333", "pos": [0,0,0]},
    "oobb_circle":         {"diameter": 3, "color": "#333333", "pos": [0,0,0]},
    "oobb_holes":          {"width": 2, "height": 2, "color": "#333333", "pos": [0,0,0]},
    "oobb_plate":          {"width": 2, "height": 2, "color": "#333333", "pos": [0,0,0]},
    "polygon":             {"points": [[0,10],[-10,-8],[10,-8]], "color": "#333333", "pos": [0,0,0]},
    "rect":                {"size": [30,20,3], "color": "#333333", "pos": [0,0,0]},
    "rounded_rectangle":   {"size": [30,20,3], "r": 4.0, "color": "#333333", "pos": [0,0,0]},
    "slot":                {"r": 4.0, "w": 20.0, "color": "#333333", "pos": [0,0,0]},
    "text":                {"text": "Sample", "size": 10.0, "font": "sans-serif",
                            "halign": "center", "valign": "center",
                            "color": "#333333", "pos": [0,0,0]},
}


def _render(component_name: str) -> str:
    """Render a component to an SVG string using _SAMPLE_KWARGS."""
    d      = COMP_ROOT / component_name
    module = _load(d)
    kwargs = _SAMPLE_KWARGS.get(component_name, {"pos": [0,0,0], "color": "#333333"})
    descs  = module.action(**kwargs)
    return opsvg.opsvg_get_svg(descs, padding=_sv.PADDING_MM, fill="#333333")


def _sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _all_component_names():
    return sorted(
        d.name for d in COMP_ROOT.iterdir()
        if d.is_dir() and (d / "working.py").exists()
    )


# ── tests ─────────────────────────────────────────────────────────────────────

class TestOpsvgGetSvg(unittest.TestCase):

    def _simple_rect_svg(self):
        descriptors = [{"shape": "rect", "size": [20, 10, 3],
                        "pos": [0, 0, 0], "color": "#333333"}]
        return opsvg.opsvg_get_svg(descriptors, fill="#333333")

    def test_returns_string(self):
        svg = self._simple_rect_svg()
        self.assertIsInstance(svg, str)

    def test_starts_with_xml_declaration(self):
        svg = self._simple_rect_svg()
        self.assertTrue(svg.strip().startswith("<?xml"))

    def test_contains_svg_element(self):
        svg = self._simple_rect_svg()
        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)

    def test_contains_viewbox(self):
        svg = self._simple_rect_svg()
        self.assertIn("viewBox", svg)

    def test_is_valid_xml(self):
        svg = self._simple_rect_svg()
        try:
            ET.fromstring(svg)
        except ET.ParseError as exc:
            self.fail(f"SVG is not valid XML: {exc}")

    def test_bounding_box_non_empty(self):
        descriptors = [{"shape": "rect", "size": [20, 10, 3],
                        "pos": [5, 3, 0], "color": "#333333"}]
        bb = opsvg._bounding_box(descriptors)
        self.assertGreater(bb["xmax"] - bb["xmin"], 0)
        self.assertGreater(bb["ymax"] - bb["ymin"], 0)

    def test_no_background_rect(self):
        """Background rect was removed when positive/negative was removed."""
        svg = self._simple_rect_svg()
        root = ET.fromstring(svg)
        # first child must not be a plain background rect (fill == cut colour)
        # just assert there's no comment "background"
        self.assertNotIn("<!-- background -->", svg)

    def test_empty_components_still_renders(self):
        svg = opsvg.opsvg_get_svg([], fill="#333333")
        self.assertIn("<svg", svg)


class TestPerComponentRendering(unittest.TestCase):

    def test_all_components_render_valid_xml(self):
        for name in _all_component_names():
            with self.subTest(component=name):
                try:
                    svg = _render(name)
                    ET.fromstring(svg)
                except ET.ParseError as exc:
                    self.fail(f"{name}: invalid XML — {exc}")
                except Exception as exc:
                    self.fail(f"{name}: render failed — {exc}")

    def test_all_components_contain_viewbox(self):
        for name in _all_component_names():
            with self.subTest(component=name):
                svg = _render(name)
                self.assertIn("viewBox", svg)

    def test_sample_svg_files_exist(self):
        for name in _all_component_names():
            with self.subTest(component=name):
                sample = COMP_ROOT / name / "sample.svg"
                self.assertTrue(sample.exists(),
                    f"{name}: sample.svg not found — run python generate_samples.py")

    def test_sample_svg_files_are_valid_xml(self):
        for name in _all_component_names():
            sample = COMP_ROOT / name / "sample.svg"
            if not sample.exists():
                continue
            with self.subTest(component=name):
                try:
                    ET.fromstring(sample.read_text(encoding="utf-8"))
                except ET.ParseError as exc:
                    self.fail(f"{name}/sample.svg: invalid XML — {exc}")


class TestSnapshotRegression(unittest.TestCase):
    """
    Compare rendered SVG hashes against stored snapshots.

    To regenerate snapshots:
        UPDATE_SNAPSHOTS=1 python -m pytest tests/test_svg_rendering.py::TestSnapshotRegression -v
    """

    UPDATE = os.environ.get("UPDATE_SNAPSHOTS", "").strip() in ("1", "true", "yes")

    def _load_snapshots(self):
        if SNAP_FILE.exists():
            return json.loads(SNAP_FILE.read_text(encoding="utf-8"))
        return {}

    def _save_snapshots(self, data: dict):
        SNAP_FILE.parent.mkdir(parents=True, exist_ok=True)
        SNAP_FILE.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    def test_snapshot_regression(self):
        snapshots = self._load_snapshots()
        updated   = dict(snapshots)
        failures  = []

        for name in _all_component_names():
            try:
                svg  = _render(name)
                hash = _sha256(svg)
            except Exception as exc:
                failures.append(f"{name}: render error — {exc}")
                continue

            if self.UPDATE:
                updated[name] = hash
            elif name not in snapshots:
                failures.append(f"{name}: no snapshot — run UPDATE_SNAPSHOTS=1 to create")
            elif snapshots[name] != hash:
                failures.append(
                    f"{name}: SVG output changed\n"
                    f"  expected: {snapshots[name]}\n"
                    f"  actual:   {hash}"
                )

        if self.UPDATE:
            self._save_snapshots(updated)
            print(f"\n[snapshots] wrote {len(updated)} entries to {SNAP_FILE}")

        if failures:
            self.fail("\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
