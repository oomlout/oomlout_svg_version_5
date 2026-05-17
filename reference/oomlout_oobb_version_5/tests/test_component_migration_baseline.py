"""Baseline snapshot test for the component migration.

Captures the output of every discovered object's action() and every
discovered set's items() into a JSON snapshot file.

Compare mode (default): asserts current output matches snapshot.
Update mode: set env var UPDATE_SNAPSHOTS=1 to regenerate the snapshot.
"""
import json
import os
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from oobb_arch.catalog.object_discovery import discover_objects
from oobb_arch.catalog.part_set_discovery import discover_part_sets

SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
SNAPSHOT_FILE = SNAPSHOT_DIR / "component_migration_baseline.json"


def _collect_snapshot():
    """Collect all object and set outputs into a dict."""
    data = {"objects": {}, "sets": {}}

    # Collect object action() outputs
    objects = discover_objects()
    for name, obj in sorted(objects.items()):
        try:
            result = obj.action_fn(type=name)
            # Only store serializable parts
            if isinstance(result, dict):
                # Store keys list and component count as a fingerprint
                data["objects"][name] = {
                    "keys": sorted(result.keys()),
                    "has_components": "components" in result,
                    "component_count": len(result.get("components", [])),
                }
            else:
                data["objects"][name] = {"type": str(type(result))}
        except Exception as e:
            data["objects"][name] = {"error": str(e)[:200]}

    # Collect set items() outputs
    sets = discover_part_sets()
    for name, s in sorted(sets.items()):
        try:
            result = s.items_fn()
            if isinstance(result, list):
                data["sets"][name] = {
                    "count": len(result),
                    "first_type": result[0].get("type", "?") if result else None,
                }
            else:
                data["sets"][name] = {"type": str(type(result))}
        except Exception as e:
            data["sets"][name] = {"error": str(e)[:200]}

    return data


class TestComponentMigrationBaseline(unittest.TestCase):
    def test_snapshot(self):
        current = _collect_snapshot()
        update_mode = os.environ.get("UPDATE_SNAPSHOTS", "").strip() == "1"

        if update_mode or not SNAPSHOT_FILE.exists():
            SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
            SNAPSHOT_FILE.write_text(json.dumps(current, indent=2, sort_keys=True))
            self.skipTest("Snapshot updated/created")
            return

        expected = json.loads(SNAPSHOT_FILE.read_text())
        self.assertEqual(
            sorted(current["objects"].keys()),
            sorted(expected["objects"].keys()),
            "Object list changed",
        )
        self.assertEqual(
            sorted(current["sets"].keys()),
            sorted(expected["sets"].keys()),
            "Set list changed",
        )
        for name in expected["objects"]:
            self.assertEqual(
                current["objects"].get(name),
                expected["objects"][name],
                f"Object '{name}' output changed",
            )
        for name in expected["sets"]:
            self.assertEqual(
                current["sets"].get(name),
                expected["sets"][name],
                f"Set '{name}' output changed",
            )


if __name__ == "__main__":
    unittest.main()
