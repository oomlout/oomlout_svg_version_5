import os
import tempfile
import unittest
from pathlib import Path

from components.generate_all_component_tests import PREVIEW_IMAGE_NAMES, generate_all_component_tests


class GenerateAllComponentTests(unittest.TestCase):
    def _write_component(self, root: Path):
        component_dir = root / "demo"
        component_dir.mkdir()
        (component_dir / "working.py").write_text(
            """
def test():
    samples = [{"filename": "test_1", "kwargs": {}}]
    marker = __file__.replace("working.py", "called.txt")
    with open(marker, "w", encoding="utf-8") as handle:
        handle.write("called")
    return []
""".strip(),
            encoding="utf-8",
        )
        return component_dir

    def _write_preview_images(self, component_dir: Path):
        sample_dir = component_dir / "test" / "test_1"
        sample_dir.mkdir(parents=True)
        for image_name in PREVIEW_IMAGE_NAMES:
            (sample_dir / image_name).write_bytes(b"png")

    def test_skip_existing_images_skips_component_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            component_dir = self._write_component(root)
            self._write_preview_images(component_dir)

            result = generate_all_component_tests(root, skip_existing_images=True)

            self.assertEqual(result, 0)
            self.assertFalse((component_dir / "called.txt").exists())

    def test_skip_existing_images_env_is_restored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            component_dir = self._write_component(root)
            self._write_preview_images(component_dir)

            os.environ.pop("OOBB_SKIP_EXISTING_IMAGES", None)
            generate_all_component_tests(root, skip_existing_images=True)

            self.assertNotIn("OOBB_SKIP_EXISTING_IMAGES", os.environ)


if __name__ == "__main__":
    unittest.main()

