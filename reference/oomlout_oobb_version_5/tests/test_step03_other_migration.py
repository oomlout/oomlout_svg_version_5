import unittest

import oobb
import oobb_get_items_other

from oobb_arch.testing.output_compare import compare_outputs


class OtherModuleFolderMigrationTests(unittest.TestCase):
    def test_bolt_forwarder_matches_folder(self):
        from components.bolt.working import action

        kwargs = {"type": "bolt", "radius_name": "m6", "depth": 10}
        legacy = oobb_get_items_other.get_bolt(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_nut_forwarder_matches_folder(self):
        from components.nuts.working import action

        kwargs = {"type": "nut", "radius_name": "m3"}
        legacy = oobb_get_items_other.get_nut(**kwargs)
        folder = action(**kwargs)
        equal, diff = compare_outputs(legacy, folder)
        self.assertTrue(equal, diff)

    def test_screw_variants_forwarders(self):
        cases = [
            ("get_screw_countersunk", "screw_countersunk", {"type": "screw_countersunk", "radius_name": "m3", "depth": 10}),
            ("get_screw_self_tapping", "screw_self_tapping", {"type": "screw_self_tapping", "radius_name": "m3", "depth": 10}),
            ("get_screw_socket_cap", "screw_socket_cap", {"type": "screw_socket_cap", "radius_name": "m3", "depth": 10}),
        ]
        for legacy_name, folder_name, kwargs in cases:
            with self.subTest(legacy_name=legacy_name):
                legacy_func = getattr(oobb_get_items_other, legacy_name)
                legacy = legacy_func(**kwargs)

                module = __import__(f"components.{folder_name}.working", fromlist=["action"])
                folder = module.action(**kwargs)
                equal, diff = compare_outputs(legacy, folder)
                self.assertTrue(equal, diff)

    def test_standoff_and_insert_and_bearing_forwarders(self):
        cases = [
            (oobb_get_items_other.get_standoff, {"type": "standoff", "radius_name": "m3", "depth": 10}),
            (oobb_get_items_other.get_threaded_insert, {"type": "threaded_insert", "radius_name": "m3", "style": "01"}),
            (oobb_get_items_other.get_bearing, {"type": "bearing", "bearing_name": "606"}),
        ]
        for func, kwargs in cases:
            with self.subTest(func=func.__name__):
                result = func(**kwargs)
                self.assertIsInstance(result, dict)
                self.assertIn("components", result)

    def test_dispatch_routes_to_migrated_folder_actions(self):
        result = oobb_base.get_thing_from_dict({"type": "bolt", "radius_name": "m6", "depth": 10})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


if __name__ == "__main__":
    unittest.main()
