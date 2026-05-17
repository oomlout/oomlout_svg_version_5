import unittest

import oobb
import oobb_get_items_oobb
import oobb_get_items_oobb_holder_electronic
import oobb_get_items_oobb_wire

from oobb_arch.helpers.component_helpers import (
    get_plate_cutout_dict,
    get_plate_nut_dict,
    get_plate_screw_dict,
)
from oobb_arch.helpers.plate_helpers import get_plate_dict, get_plate_hole_dict
from oobb_arch.testing.output_compare import compare_outputs


class SharedHelperExtractionTests(unittest.TestCase):
    def test_get_plate_dict_shape(self):
        result = get_plate_dict(size="oobb", thickness=3, pos_plate=[0, 0, 0])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["shape"], "oobb_plate")
        self.assertEqual(result["type"], "positive")

    def test_get_plate_hole_dict_shape(self):
        result = get_plate_hole_dict(size="oobb", pos_plate=[0, 0, 0])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["shape"], "oobb_holes")
        self.assertEqual(result["type"], "p")

    def test_plate_helpers_match_legacy_exports(self):
        kwargs = {"size": "oobb", "thickness": 3, "pos_plate": [0, 0, 0]}
        legacy = oobb_get_items_oobb.get_plate_dict(**kwargs)
        shared = get_plate_dict(**kwargs)
        equal, diff = compare_outputs(legacy, shared)
        self.assertTrue(equal, f"plate_dict mismatch: {diff}")

        kwargs_holes = {
            "size": "oobb",
            "pos_plate": [0, 0, 0],
            "hole_sides": ["left", "right", "top"],
        }
        legacy_holes = oobb_get_items_oobb.get_plate_hole_dict(**kwargs_holes)
        shared_holes = get_plate_hole_dict(**kwargs_holes)
        equal_holes, diff_holes = compare_outputs(legacy_holes, shared_holes)
        self.assertTrue(equal_holes, f"plate_hole_dict mismatch: {diff_holes}")

    def test_component_helpers_match_legacy_exports(self):
        cutout_kwargs = {"pos_plate": [0, 0, 0], "plate_thickness": 1.5, "thickness": 3}
        legacy_cutout = oobb_get_items_oobb_holder_electronic.get_plate_cutout_dict(**cutout_kwargs)
        shared_cutout = get_plate_cutout_dict(**cutout_kwargs)
        equal_cutout, diff_cutout = compare_outputs(legacy_cutout, shared_cutout)
        self.assertTrue(equal_cutout, f"plate_cutout_dict mismatch: {diff_cutout}")

        screw_kwargs = {"pos_plate": [0, 0, 0], "thickness": 3}
        legacy_screw = oobb_get_items_oobb_holder_electronic.get_plate_screw_dict(**screw_kwargs)
        shared_screw = get_plate_screw_dict(**screw_kwargs)
        equal_screw, diff_screw = compare_outputs(legacy_screw, shared_screw)
        self.assertTrue(equal_screw, f"plate_screw_dict mismatch: {diff_screw}")

        nut_kwargs = {"pos_plate": [0, 0, 0], "thickness": 3, "width": 3}
        legacy_nut = oobb_get_items_oobb_wire.get_plate_nut_dict(**nut_kwargs)
        shared_nut = get_plate_nut_dict(**nut_kwargs)
        equal_nut, diff_nut = compare_outputs(legacy_nut, shared_nut)
        self.assertTrue(equal_nut, f"plate_nut_dict mismatch: {diff_nut}")

    def test_legacy_modules_still_export_helpers(self):
        self.assertTrue(hasattr(oobb_get_items_oobb, "get_plate_dict"))
        self.assertTrue(hasattr(oobb_get_items_oobb, "get_plate_hole_dict"))
        self.assertTrue(hasattr(oobb_get_items_oobb_holder_electronic, "get_plate_cutout_dict"))
        self.assertTrue(hasattr(oobb_get_items_oobb_holder_electronic, "get_plate_screw_dict"))
        self.assertTrue(hasattr(oobb_get_items_oobb_wire, "get_plate_nut_dict"))


if __name__ == "__main__":
    unittest.main()
