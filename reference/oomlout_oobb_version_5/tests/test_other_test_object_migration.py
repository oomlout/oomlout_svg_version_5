import unittest
from pathlib import Path

from oobb_arch.catalog.migration_status import get_all_legacy_object_functions, get_migration_status
from oobb_arch.catalog.object_discovery import discover_objects


ROOT = Path(__file__).resolve().parents[1]
OBJECTS_ROOT = ROOT / "components"

_MERGE_MAP = {
    "bearing": "bearings", "bearing_circle": "bearing_circles", "bearing_plate": "bearing_plates",
    "circle": "circles", "gear": "gears", "holder": "holders", "jack": "jacks", "jig": "jigs",
    "mounting_plate": "mounting_plates", "nut": "nuts", "other": "others", "plate": "plates",
    "pulley_gt2": "pulleys", "shaft": "shafts", "shaft_coupler": "shaft_couplers",
    "smd_magazine": "smd_magazines", "soldering_jig": "soldering_jigs", "test": "tests",
    "tool_holder": "tool_holders", "tray": "trays", "wheel": "wheels", "wire": "wires",
    "ziptie_holder": "ziptie_holders", "bunting_alphabet": "buntings",
}


def _resolve_folder(type_name: str) -> str:
    return _MERGE_MAP.get(type_name, type_name)


class OtherTestObjectMigrationTests(unittest.TestCase):
    def _legacy_from_module(self, module_name: str):
        return [item for item in get_all_legacy_object_functions() if item["source_module"] == module_name]

    def test_all_other_functions_have_folders(self):
        for item in self._legacy_from_module("oobb_get_items_other"):
            path = OBJECTS_ROOT / _resolve_folder(item['type_name']) / "working.py"
            self.assertTrue(path.exists(), msg=f"Missing folder for {item['function_name']}")

    def test_all_test_functions_have_folders(self):
        for item in self._legacy_from_module("oobb_get_items_test"):
            path = OBJECTS_ROOT / _resolve_folder(item['type_name']) / "working.py"
            self.assertTrue(path.exists(), msg=f"Missing folder for {item['function_name']}")

    def test_zero_pending_objects(self):
        status = get_migration_status(objects_root=OBJECTS_ROOT)
        objects = status["objects"]
        self.assertEqual(objects["pending"], [])
        self.assertEqual(objects["total_migrated"], objects["total_legacy"])
        self.assertEqual(objects["percentage"], 100.0)

    def test_hardware_objects_have_enhanced_metadata(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        for name in ["nuts", "screw_socket_cap", "bearings"]:
            self.assertIn(name, discovered)
            description = discovered[name].metadata.get("description", "")
            self.assertTrue(description)
            self.assertNotIn("Auto-generated scaffold", description)

    def test_all_discovered_objects_have_action_fn(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertGreaterEqual(len(discovered), 60)
        for item in discovered.values():
            self.assertTrue(callable(item.action_fn))


if __name__ == "__main__":
    unittest.main()
