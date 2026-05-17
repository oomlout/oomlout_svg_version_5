import unittest
from pathlib import Path

from oobb_arch.catalog.object_discovery import build_object_lookup, discover_objects


ROOT = Path(__file__).resolve().parents[1]
OBJECTS_ROOT = ROOT / "components"


class ObjectWorkingFileTests(unittest.TestCase):
    def _assert_required_metadata(self, metadata: dict):
        for key in ["name", "description", "category", "variables"]:
            self.assertIn(key, metadata)
        self.assertIsInstance(metadata["variables"], list)

    def test_circle_define_metadata(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertIn("circles", discovered)
        metadata = discovered["circles"].metadata
        self._assert_required_metadata(metadata)

    def test_bolt_define_metadata(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertIn("bolt", discovered)
        metadata = discovered["bolt"].metadata
        self._assert_required_metadata(metadata)
        self.assertEqual(metadata.get("category"), "Hardware")

    def test_test_gear_define_metadata(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertIn("test_gear", discovered)
        metadata = discovered["test_gear"].metadata
        self._assert_required_metadata(metadata)
        self.assertEqual(metadata.get("category"), "OOBB Test")

    def test_circle_discovered(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertIn("circles", discovered)

    def test_bolt_discovered(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertIn("bolt", discovered)

    def test_test_gear_discovered(self):
        discovered = discover_objects(objects_root=OBJECTS_ROOT)
        self.assertIn("test_gear", discovered)

    def test_circle_alias_dispatch(self):
        lookup = build_object_lookup(objects_root=OBJECTS_ROOT)
        self.assertIn("circle", lookup)
        self.assertEqual(lookup["circle"].name, "circles")


if __name__ == "__main__":
    unittest.main()
