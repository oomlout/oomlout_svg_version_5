import tempfile
import unittest
from pathlib import Path

from components.report_migration_status import build_status


class PartSetMigrationStatusTests(unittest.TestCase):
    def test_build_status_reports_missing_expected_sets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            one = root / "jigs"
            one.mkdir(parents=True)
            (one / "working.py").write_text(
                """
def define():
    return {"name": "jigs"}

def items(size="oobb", **kwargs):
    return []
""".strip(),
                encoding="utf-8",
            )

            status = build_status(expected_sets=["jigs", "plates"], sets_root=root)
            self.assertEqual(status["discovered_count"], 1)
            self.assertEqual(status["missing"], ["plates"])
            self.assertIn("jigs", status["discovered"])


if __name__ == "__main__":
    unittest.main()
