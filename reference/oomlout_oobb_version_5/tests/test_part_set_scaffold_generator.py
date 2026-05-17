import tempfile
import unittest
from pathlib import Path

from components.generate_set_scaffold import create_set_scaffold


class PartSetScaffoldGeneratorTests(unittest.TestCase):
    def test_create_set_scaffold_writes_working_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            sets_root = Path(tmp)
            working_file = create_set_scaffold("demo_set", sets_root=sets_root)

            self.assertTrue(working_file.is_file())
            content = working_file.read_text(encoding="utf-8")
            self.assertIn("def define():", content)
            self.assertIn("def items(size=\"oobb\", **kwargs):", content)
            self.assertIn('"name": "demo_set"', content)


if __name__ == "__main__":
    unittest.main()
