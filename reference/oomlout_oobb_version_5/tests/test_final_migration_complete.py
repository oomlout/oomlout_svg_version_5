import json
import tempfile
import unittest
from pathlib import Path

from oobb_arch.catalog.migration_status import get_migration_status
from oobb_arch.catalog.object_discovery import discover_objects
from oobb_arch.catalog.part_set_discovery import discover_part_sets
from components.documentation import export_documentation_json


ROOT = Path(__file__).resolve().parents[1]
OBJECTS_ROOT = ROOT / "components"
SETS_ROOT = ROOT / "components"


class FinalMigrationCompleteTests(unittest.TestCase):
    def test_100_percent_object_migration(self):
        status = get_migration_status(objects_root=OBJECTS_ROOT, sets_root=SETS_ROOT)
        self.assertEqual(status["objects"]["percentage"], 100.0)

    def test_100_percent_set_migration(self):
        status = get_migration_status(objects_root=OBJECTS_ROOT, sets_root=SETS_ROOT)
        self.assertEqual(status["sets"]["percentage"], 100.0)

    def test_documentation_json_covers_all_entities(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "documentation_data.json"
            export_documentation_json(output, objects_root=OBJECTS_ROOT, sets_root=SETS_ROOT)

            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertGreaterEqual(payload["total_objects"], 60)
            self.assertGreaterEqual(payload["total_part_sets"], 25)

            documented_objects = {item["command"] for item in payload["objects"]}
            documented_sets = {item["command"] for item in payload["part_sets"]}

            discovered_objects = set(discover_objects(objects_root=OBJECTS_ROOT).keys())
            discovered_sets = set(discover_part_sets(sets_root=SETS_ROOT).keys())

            self.assertTrue(discovered_objects.issubset(documented_objects))
            self.assertTrue(discovered_sets.issubset(documented_sets))


if __name__ == "__main__":
    unittest.main()
