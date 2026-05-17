import unittest

import oobb
import oobb_get_items_oobb

from oobb_arch.testing.output_compare import compare_outputs


class TestCoreMigrationWave1(unittest.TestCase):
    def test_plate_dict_forwarder_matches_folder(self):
        from components.plate_dict.working import action

        kwargs = {"type": "plate_dict", "size": "oobb", "thickness": 3, "pos_plate": [1, 2, 3]}
        legacy = oobb_get_items_oobb.get_plate_dict(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_plate_hole_dict_forwarder_matches_folder(self):
        from components.plate_hole_dict.working import action

        kwargs = {
            "type": "plate_hole_dict",
            "size": "oobb",
            "hole_sides": ["left", "right", "top", "bottom"],
            "pos_plate": [0, 0, 0],
        }
        legacy = oobb_get_items_oobb.get_plate_hole_dict(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_other_forwarder_matches_folder(self):
        from components.others.working import action

        kwargs = {
            "type": "other",
            "extra": "bolt_stacker",
            "size": "oobb",
            "width": 1,
            "height": 1,
            "thickness": 3,
        }
        legacy = oobb_get_items_oobb.get_other(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_dispatch_uses_wave1_core_types(self):
        cases = [
            {"type": "plate_dict", "size": "oobb", "thickness": 3, "pos_plate": [1, 2, 3]},
            {"type": "plate", "size": "oobb", "width": 3, "height": 3, "thickness": 3},
            {
                "type": "plate_hole_dict",
                "size": "oobb",
                "hole_sides": ["left", "right", "top", "bottom"],
                "pos_plate": [0, 0, 0],
            },
            {"type": "circle", "size": "oobb", "diameter": 3, "thickness": 3},
            {"type": "other", "extra": "bolt_stacker", "size": "oobb", "width": 1, "height": 1, "thickness": 3},
            {"type": "test", "extra": "rotation", "size": "oobb", "thickness": 3},
            {"type": "wheel", "extra": "no_tire", "size": "oobb", "thickness": 3},
            {"type": "wire", "extra": "motor", "size": "oobb", "width": 3, "height": 3},
        ]
        for payload in cases:
            with self.subTest(type=payload["type"]):
                result = oobb_base.get_thing_from_dict(payload)
                self.assertIsInstance(result, dict)

    def test_test_forwarder_matches_folder(self):
        from components.tests.working import action

        kwargs = {"type": "test", "extra": "rotation", "size": "oobb", "thickness": 3}
        legacy = oobb_get_items_oobb.get_test(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_wheel_forwarder_matches_folder(self):
        from components.wheels.working import action

        kwargs = {"type": "wheel", "extra": "no_tire", "size": "oobb", "thickness": 3}
        legacy = oobb_get_items_oobb.get_wheel(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_wire_forwarder_matches_folder(self):
        from components.wires.working import action

        kwargs = {"type": "wire", "extra": "motor", "size": "oobb", "width": 3, "height": 3}
        legacy = oobb_get_items_oobb.get_wire(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_plate_forwarder_matches_folder(self):
        from components.plates.working import action

        kwargs = {"type": "plate", "size": "oobb", "width": 3, "height": 3, "thickness": 3}
        legacy = oobb_get_items_oobb.get_plate(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_circle_forwarder_matches_folder(self):
        from components.circles.working import action

        kwargs = {"type": "circle", "size": "oobb", "diameter": 3, "thickness": 3}
        legacy = oobb_get_items_oobb.get_circle(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)


if __name__ == "__main__":
    unittest.main()
