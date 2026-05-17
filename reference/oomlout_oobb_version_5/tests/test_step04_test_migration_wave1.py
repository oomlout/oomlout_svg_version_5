import unittest

import oobb
import oobb_get_items_test

from oobb_arch.testing.output_compare import compare_outputs


class TestModuleMigrationWave1(unittest.TestCase):
    def test_test_gear_forwarder_matches_folder(self):
        from components.test_gear.working import action

        kwargs = {"type": "test_gear", "size": "oobb", "extra": "gear"}
        legacy = oobb_get_items_test.get_test_gear(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_hole_forwarder_matches_folder(self):
        from components.test_hole.working import action

        kwargs = {
            "type": "test_hole",
            "width": 3,
            "height": 3,
            "thickness": 3,
            "shaft": 3,
            "bearing": 0.5,
        }
        legacy = oobb_get_items_test.get_test_hole(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_rotation_forwarder_matches_folder(self):
        from components.test_rotation.working import action

        kwargs = {"type": "test_rotation", "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_test.get_test_rotation(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_dispatch_uses_migrated_wave1_types(self):
        cases = [
            {"type": "test_gear", "size": "oobb", "extra": "gear"},
            {"type": "test_hole", "width": 3, "height": 3, "thickness": 3, "shaft": 3, "bearing": 0.5},
            {"type": "test_rotation", "thickness": 3, "size": "oobb"},
            {"type": "test_motor_tt_01", "size": "oobb"},
            {"type": "test_motor_tt_01_shaft", "size": "oobb"},
            {"type": "test_motor_n20_shaft", "size": "oobb"},
            {"type": "test_oobb_motor_servo_standard_01", "size": "oobb"},
            {"type": "test_oobb_nut", "size": "oobb"},
            {"type": "test_oobb_screw", "size": "oobb", "style": "socket_cap"},
            {"type": "test_oobb_screw_socket_cap", "size": "oobb"},
            {"type": "test_oobb_screw_countersunk", "size": "oobb"},
            {"type": "test_oobb_screw_self_tapping", "size": "oobb"},
            {"type": "test_oobb_screw_socket_cap_old_1", "size": "oobb"},
            {"type": "test_oobb_shape_slot", "size": "oobb"},
            {"type": "test_oobb_wire", "size": "oobb"},
        ]
        for payload in cases:
            with self.subTest(type=payload["type"]):
                result = oobb_base.get_thing_from_dict(payload)
                self.assertIsInstance(result, dict)
                self.assertIn("components", result)

    def test_test_motor_tt_01_forwarder_matches_folder(self):
        from components.test_motor_tt_01.working import action

        kwargs = {"type": "test_motor_tt_01", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_motor_tt_01(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_motor_tt_01_shaft_forwarder_matches_folder(self):
        from components.test_motor_tt_01_shaft.working import action

        kwargs = {"type": "test_motor_tt_01_shaft", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_motor_tt_01_shaft(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_motor_n20_shaft_forwarder_matches_folder(self):
        from components.test_motor_n20_shaft.working import action

        kwargs = {"type": "test_motor_n20_shaft", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_motor_n20_shaft(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_oobb_motor_servo_standard_01_forwarder_matches_folder(self):
        from components.test_oobb_motor_servo_standard_01.working import action

        kwargs = {"type": "test_oobb_motor_servo_standard_01", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_oobb_motor_servo_standard_01(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_oobb_nut_forwarder_matches_folder(self):
        from components.test_oobb_nut.working import action

        kwargs = {"type": "test_oobb_nut", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_oobb_nut(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_oobb_screw_forwarder_matches_folder(self):
        from components.test_oobb_screw.working import action

        kwargs = {"type": "test_oobb_screw", "size": "oobb", "style": "socket_cap"}
        legacy = oobb_get_items_test.get_test_oobb_screw(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_oobb_screw_wrappers_forwarders_match(self):
        wrapper_cases = [
            ("get_test_oobb_screw_socket_cap", "components.test_oobb_screw_socket_cap.working", "test_oobb_screw_socket_cap"),
            ("get_test_oobb_screw_countersunk", "components.test_oobb_screw_countersunk.working", "test_oobb_screw_countersunk"),
            ("get_test_oobb_screw_self_tapping", "components.test_oobb_screw_self_tapping.working", "test_oobb_screw_self_tapping"),
        ]
        for legacy_name, module_path, obj_type in wrapper_cases:
            with self.subTest(wrapper=legacy_name):
                module = __import__(module_path, fromlist=["action"])
                folder = module.action(type=obj_type, size="oobb")
                legacy = getattr(oobb_get_items_test, legacy_name)(type=obj_type, size="oobb")
                equal, diff = compare_outputs(legacy, folder)
                self.assertTrue(equal, diff)

    def test_test_oobb_screw_socket_cap_old_1_forwarder_matches_folder(self):
        from components.test_oobb_screw_socket_cap_old_1.working import action

        kwargs = {"type": "test_oobb_screw_socket_cap_old_1", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_oobb_screw_socket_cap_old_1(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_oobb_shape_slot_forwarder_matches_folder(self):
        from components.test_oobb_shape_slot.working import action

        kwargs = {"type": "test_oobb_shape_slot", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_oobb_shape_slot(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_test_oobb_wire_forwarder_matches_folder(self):
        from components.test_oobb_wire.working import action

        kwargs = {"type": "test_oobb_wire", "size": "oobb"}
        legacy = oobb_get_items_test.get_test_oobb_wire(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)


if __name__ == "__main__":
    unittest.main()
