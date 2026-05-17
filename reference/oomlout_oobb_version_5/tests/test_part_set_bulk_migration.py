import unittest
from types import SimpleNamespace
from unittest import mock
from pathlib import Path

import oobb
import oobb_make_sets

from oobb_arch.catalog.migration_status import get_all_legacy_set_functions, get_migration_status
from oobb_arch.catalog.part_set_discovery import discover_part_sets


ROOT = Path(__file__).resolve().parents[1]
SETS_ROOT = ROOT / "components"


class PartSetBulkMigrationTests(unittest.TestCase):
    def test_all_make_sets_functions_have_folders(self):
        for item in get_all_legacy_set_functions():
            path = SETS_ROOT / item["set_name"] / "working.py"
            self.assertTrue(path.exists(), msg=f"Missing set folder for {item['function_name']}")

    def test_all_sets_discovered(self):
        discovered = discover_part_sets(sets_root=SETS_ROOT)
        self.assertGreaterEqual(len(discovered), 25)

    def test_zero_pending_sets(self):
        status = get_migration_status(sets_root=SETS_ROOT)
        sets = status["sets"]
        self.assertEqual(sets["pending"], [])
        self.assertEqual(sets["percentage"], 100.0)

    def test_key_sets_have_rich_metadata(self):
        discovered = discover_part_sets(sets_root=SETS_ROOT)
        for name in ["circles", "plates", "gears", "holders"]:
            self.assertIn(name, discovered)
            metadata = discovered[name].metadata
            self.assertTrue(metadata.get("description"))
            self.assertNotIn("part-set definitions", metadata.get("description", ""))
            self.assertTrue(metadata.get("name_long"))

    def test_make_all_still_works(self):
        fake_oobb_base = SimpleNamespace(
            get_default_thing=lambda **kwargs: {"id": "skip_always"},
            get_thing_from_dict=lambda payload: payload,
            add_thing=lambda thing: None,
        )
        with mock.patch.object(oobb_make_sets, "oobb_base", fake_oobb_base):
            # Use an impossible filter so add_thing path is skipped.
            result = oobb_make_sets.make_all(filter="__NO_MATCH__")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
