import copy
import unittest

import oobb
import oobb_get_items_oobb

from oobb_arch.testing.output_compare import (
    capture_legacy_output,
    compare_outputs,
    normalize_thing_for_comparison,
)


class OutputComparisonHarnessTests(unittest.TestCase):
    def test_normalize_strips_volatile_keys(self):
        thing = {
            "id": "abc",
            "file_path": "c:/tmp/out.scad",
            "timestamp": "2026-03-28T00:00:00",
            "components": [],
        }
        result = normalize_thing_for_comparison(thing)
        self.assertIn("id", result)
        self.assertNotIn("file_path", result)
        self.assertNotIn("timestamp", result)

    def test_normalize_rounds_floats(self):
        thing = {"value": 3.141592653589793}
        result = normalize_thing_for_comparison(thing)
        self.assertEqual(result["value"], round(3.141592653589793, 10))

    def test_compare_identical(self):
        a = {"id": "x", "components": [{"type": "p", "pos": [0, 0, 0]}]}
        b = copy.deepcopy(a)
        equal, diff = compare_outputs(a, b)
        self.assertTrue(equal)
        self.assertEqual(diff, "")

    def test_compare_different(self):
        a = {"id": "x", "components": [{"type": "p"}]}
        b = {"id": "x", "components": [{"type": "n"}]}
        equal, diff = compare_outputs(a, b)
        self.assertFalse(equal)
        self.assertIn("First diff", diff)

    def test_compare_ignores_volatile(self):
        a = {"id": "x", "timestamp": "2024-01-01", "components": []}
        b = {"id": "x", "timestamp": "2026-01-01", "components": []}
        equal, _ = compare_outputs(a, b)
        self.assertTrue(equal)

    def test_capture_legacy_output_real_module(self):
        result = capture_legacy_output(
            oobb_get_items_oobb,
            "get_plate_dict",
            {"size": "oobb", "thickness": 3, "pos_plate": [0, 0, 0]},
        )
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("shape"), "oobb_plate")


if __name__ == "__main__":
    unittest.main()
