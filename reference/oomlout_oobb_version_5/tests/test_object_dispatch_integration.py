import unittest
from types import SimpleNamespace
from unittest import mock

import oobb


class ObjectDispatchIntegrationTests(unittest.TestCase):
    def test_dispatch_prefers_discovered(self):
        sentinel = {"source": "discovered", "components": []}
        discovered = SimpleNamespace(action_fn=lambda **kwargs: sentinel)
        legacy_registry = SimpleNamespace(resolve=lambda typ: (lambda **kwargs: {"source": "legacy", "components": []}))

        with mock.patch.object(oobb, "_get_object_lookup", return_value={"demo": discovered}), mock.patch.object(
            oobb, "_get_legacy_builder_registry", return_value=legacy_registry
        ):
            result = oobb.get_thing_from_dict({"type": "demo"})

        self.assertEqual(result, sentinel)

    def test_dispatch_falls_back_to_legacy(self):
        expected = {"source": "legacy", "components": []}
        legacy_registry = SimpleNamespace(resolve=lambda typ: (lambda **kwargs: expected))

        with mock.patch.object(oobb, "_get_object_lookup", return_value={}), mock.patch.object(
            oobb, "_get_legacy_builder_registry", return_value=legacy_registry
        ):
            result = oobb.get_thing_from_dict({"type": "plate"})

        self.assertEqual(result, expected)

    def test_dispatch_circle_via_discovery(self):
        oobb._OBJECT_LOOKUP = None
        payload = {"type": "circle", "diameter": 3, "thickness": 3, "size": "oobb"}
        result = oobb_base.get_thing_from_dict(payload)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


if __name__ == "__main__":
    unittest.main()
