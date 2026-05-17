import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from oobb_arch.catalog.object_discovery import discover_objects
from oobb_arch.catalog.object_scaffold_generator import generate_object_scaffold


def _load_module(path: Path):
    spec = spec_from_file_location(f"test_mod_{path.stem}", str(path))
    module = module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ObjectScaffoldGeneratorTests(unittest.TestCase):
    def test_scaffold_generates_valid_working_py(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            path = generate_object_scaffold(
                "test_type",
                "oobb_get_items_test",
                "get_test_gear",
                output_dir=output,
            )
            self.assertTrue(path.is_file())

            module = _load_module(path)
            self.assertTrue(callable(getattr(module, "define", None)))
            self.assertTrue(callable(getattr(module, "action", None)))
            self.assertTrue(callable(getattr(module, "test", None)))

            metadata = module.define()
            self.assertEqual(metadata.get("name"), "test_type")
            self.assertEqual(metadata.get("source_module"), "oobb_get_items_test")

    def test_scaffold_respects_overwrite_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            path = generate_object_scaffold(
                "overwrite_demo",
                "oobb_get_items_other",
                "get_bolt",
                output_dir=output,
            )
            path.write_text("sentinel", encoding="utf-8")

            same_path = generate_object_scaffold(
                "overwrite_demo",
                "oobb_get_items_other",
                "get_bolt",
                output_dir=output,
                overwrite=False,
            )
            self.assertEqual(same_path, path)
            self.assertEqual(path.read_text(encoding="utf-8"), "sentinel")

            generate_object_scaffold(
                "overwrite_demo",
                "oobb_get_items_other",
                "get_bolt",
                output_dir=output,
                overwrite=True,
            )
            self.assertIn("def define():", path.read_text(encoding="utf-8"))

    def test_scaffold_auto_detects_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            first = generate_object_scaffold("geom", "oobb_get_items_oobb", "get_circle", output_dir=output)
            second = generate_object_scaffold("hw", "oobb_get_items_other", "get_bolt", output_dir=output)

            first_meta = _load_module(first).define()
            second_meta = _load_module(second).define()
            self.assertEqual(first_meta.get("category"), "OOBB Geometry")
            self.assertEqual(second_meta.get("category"), "Hardware")

    def test_scaffold_generates_discoverable_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            generate_object_scaffold("discoverable", "oobb_get_items_other", "get_bolt", output_dir=output)

            discovered = discover_objects(objects_root=output)
            self.assertIn("discoverable", discovered)
            self.assertTrue(callable(discovered["discoverable"].action_fn))


if __name__ == "__main__":
    unittest.main()
