import tempfile
import unittest
from pathlib import Path

from oobb_arch.catalog.object_discovery import build_object_lookup, discover_objects


class ObjectDiscoveryContractTests(unittest.TestCase):
    def test_discover_objects_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            valid = root / "test_obj"
            valid.mkdir(parents=True)
            (valid / "working.py").write_text(
                """
def define():
    return {
        "name": "test_obj",
        "name_short": ["tobj"],
        "description": "Test",
        "category": "Test",
        "variables": []
    }

def action(**kwargs):
    return {"type": "test", "components": []}

def test(**kwargs):
    return True
""".strip(),
                encoding="utf-8",
            )

            discovered = discover_objects(objects_root=root)
            self.assertIn("test_obj", discovered)
            item = discovered["test_obj"]
            self.assertEqual(item.metadata["name"], "test_obj")
            self.assertTrue(callable(item.action_fn))
            self.assertTrue(callable(item.test_fn))

    def test_discover_objects_skips_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            invalid = root / "invalid"
            invalid.mkdir(parents=True)
            (invalid / "working.py").write_text(
                """
def define():
    return {"name": "invalid"}
""".strip(),
                encoding="utf-8",
            )

            discovered = discover_objects(objects_root=root)
            self.assertEqual(discovered, {})

    def test_build_object_lookup_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            valid = root / "alias"
            valid.mkdir(parents=True)
            (valid / "working.py").write_text(
                """
def define():
    return {"name": "alias", "name_short": ["alias1", "alias2"]}

def action(**kwargs):
    return {"type": "alias", "components": []}
""".strip(),
                encoding="utf-8",
            )

            lookup = build_object_lookup(objects_root=root)
            self.assertIn("alias", lookup)
            self.assertIn("alias1", lookup)
            self.assertIn("alias2", lookup)
            self.assertEqual(lookup["alias1"].name, "alias")
            self.assertEqual(lookup["alias2"].name, "alias")

    def test_discover_objects_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            discovered = discover_objects(objects_root=root)
            self.assertEqual(discovered, {})


if __name__ == "__main__":
    unittest.main()
