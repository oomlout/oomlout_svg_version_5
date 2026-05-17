import tempfile
import unittest
from pathlib import Path

from components.run_tests import run_all_object_tests, run_all_set_tests, run_all_tests


ROOT = Path(__file__).resolve().parents[1]
OBJECTS_ROOT = ROOT / "components"
SETS_ROOT = ROOT / "components"


class PerFolderTestRunnerTests(unittest.TestCase):
    def test_run_all_object_tests_returns_results(self):
        results = run_all_object_tests(objects_root=OBJECTS_ROOT)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result.entity_type == "object" for result in results))

    def test_run_all_set_tests_returns_results(self):
        results = run_all_set_tests(sets_root=SETS_ROOT)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result.entity_type == "set" for result in results))

    def test_run_all_tests_combined(self):
        results = run_all_tests(objects_root=OBJECTS_ROOT, sets_root=SETS_ROOT)
        self.assertGreaterEqual(len(results), 85)
        types = {result.entity_type for result in results}
        self.assertIn("object", types)
        self.assertIn("set", types)

    def test_skip_result_for_missing_test_fn(self):
        with tempfile.TemporaryDirectory() as tmp:
            objects_root = Path(tmp) / "objects"
            folder = objects_root / "skip_demo"
            folder.mkdir(parents=True)
            (folder / "working.py").write_text(
                """
def define():
    return {"name": "skip_demo", "description": "skip demo", "variables": []}

def action(**kwargs):
    return {"type": "skip_demo", "components": []}
""".strip(),
                encoding="utf-8",
            )

            results = run_all_object_tests(objects_root=objects_root)
            target = [result for result in results if result.name == "skip_demo"]
            self.assertEqual(len(target), 1)
            self.assertEqual(target[0].status, "SKIP")


if __name__ == "__main__":
    unittest.main()
