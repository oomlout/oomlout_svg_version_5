import unittest
from unittest import mock
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import SimpleNamespace
import sys

class MakeSetsDiscoveryIntegrationTests(unittest.TestCase):
    def _load_make_sets_module(self):
        repo_root = Path(__file__).resolve().parents[1]
        file_path = repo_root / "oobb_make_sets.py"
        fake_oobb_base = SimpleNamespace(
            get_default_thing=mock.Mock(return_value={"id": "fake_id"}),
            get_thing_from_dict=mock.Mock(return_value={"id": "fake_id", "components": []}),
            add_thing=mock.Mock(),
        )

        module_name = f"test_oobb_make_sets_{abs(hash(str(file_path)))}"
        spec = spec_from_file_location(module_name, str(file_path))
        module = module_from_spec(spec)
        with mock.patch.dict(sys.modules, {"oobb_base": fake_oobb_base}):
            spec.loader.exec_module(module)
        return module, fake_oobb_base

    def test_make_all_prefers_discovered_provider(self):
        oobb_make_sets, _ = self._load_make_sets_module()
        fake_discovered = mock.Mock()
        fake_discovered.items_fn.return_value = [{"type": "bearing_circle", "size": "oobb"}]

        with mock.patch.object(oobb_make_sets, "_get_discovered_part_set_lookup", return_value={"bearing_circles": fake_discovered}):
            with mock.patch.object(oobb_make_sets, "get_bearing_circles", return_value=[]):
                oobb_make_sets.make_all(filter=["__never__"])

        fake_discovered.items_fn.assert_called_once()

    def test_make_all_falls_back_to_legacy_getter(self):
        oobb_make_sets, _ = self._load_make_sets_module()
        with mock.patch.object(oobb_make_sets, "_get_discovered_part_set_lookup", return_value={}):
            with mock.patch.object(oobb_make_sets, "get_bearing_circles", return_value=[{"type": "bearing_circle", "size": "oobb"}]) as legacy_getter:
                oobb_make_sets.make_all(filter=["__never__"])

        legacy_getter.assert_called_once()

    def test_bridge_returns_none_when_set_missing(self):
        oobb_make_sets, _ = self._load_make_sets_module()
        with mock.patch.object(oobb_make_sets, "_get_discovered_part_set_lookup", return_value={}):
            value = oobb_make_sets.get_set_items_discovered("missing_set")
        self.assertIsNone(value)

    def test_bridge_returns_items_for_discovered_set(self):
        oobb_make_sets, _ = self._load_make_sets_module()
        fake_discovered = mock.Mock()
        fake_discovered.items_fn.return_value = [{"type": "jig"}]
        with mock.patch.object(oobb_make_sets, "_get_discovered_part_set_lookup", return_value={"jigs": fake_discovered}):
            value = oobb_make_sets.get_set_items_discovered("jigs")
        self.assertEqual(value, [{"type": "jig"}])

    def test_migrated_get_bearing_circles_uses_discovery_bridge(self):
        oobb_make_sets, _ = self._load_make_sets_module()
        expected = [{"type": "bearing_circle", "diameter": 99, "size": "oobb"}]
        with mock.patch.object(oobb_make_sets, "get_set_items_discovered", return_value=expected):
            value = oobb_make_sets.get_bearing_circles(size="oobb")
        self.assertEqual(value, expected)


if __name__ == "__main__":
    unittest.main()
