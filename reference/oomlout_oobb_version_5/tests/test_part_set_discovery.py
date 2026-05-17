import unittest
from pathlib import Path
import tempfile

from oobb_arch.catalog.part_set_discovery import build_part_set_lookup, discover_part_sets


class PartSetDiscoveryContractTests(unittest.TestCase):
    def test_discover_part_sets_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            valid = root / "bearing_plates"
            valid.mkdir(parents=True)
            (valid / "working.py").write_text(
                """
def define():
    return {"name": "bearing_plates", "name_short": ["bps"], "description": "x", "variables": ["size"]}

def items(size=\"oobb\", **kwargs):
    return [{"type": "bearing_plate", "size": size}]
""".strip(),
                encoding="utf-8",
            )

            invalid = root / "invalid_no_items"
            invalid.mkdir(parents=True)
            (invalid / "working.py").write_text(
                """
def define():
    return {"name": "invalid_no_items"}
""".strip(),
                encoding="utf-8",
            )

            discovered = discover_part_sets(sets_root=root)
            self.assertIn("bearing_plates", discovered)
            self.assertNotIn("invalid_no_items", discovered)
            self.assertTrue(callable(discovered["bearing_plates"].items_fn))

    def test_build_lookup_includes_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            valid = root / "circles"
            valid.mkdir(parents=True)
            (valid / "working.py").write_text(
                """
def define():
    return {"name": "circles", "name_short": ["ci", "circle_set"]}

def items(size=\"oobb\", **kwargs):
    return [{"type": "circle", "size": size}]
""".strip(),
                encoding="utf-8",
            )

            lookup = build_part_set_lookup(sets_root=root)
            self.assertIn("circles", lookup)
            self.assertIn("ci", lookup)
            self.assertIn("circle_set", lookup)
            self.assertEqual(lookup["ci"].name, "circles")

    def test_default_root_discovers_seeded_project_sets(self):
        discovered = discover_part_sets()
        self.assertIn("bearing_circles", discovered)
        self.assertIn("jigs", discovered)
        self.assertIn("others", discovered)


if __name__ == "__main__":
    unittest.main()
