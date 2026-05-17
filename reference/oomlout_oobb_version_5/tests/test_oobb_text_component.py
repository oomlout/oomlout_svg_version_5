import unittest
from types import ModuleType
from unittest import mock


def _fake_opsc():
    fake = ModuleType("opsc")

    def opsc_easy(**kwargs):
        return kwargs

    fake.opsc_easy = opsc_easy
    return fake


class OobbTextComponentTests(unittest.TestCase):
    def test_action_applies_legacy_defaults_and_aliases(self):
        from components.oobb_text.working import action

        with mock.patch.dict("sys.modules", {"opsc": _fake_opsc()}):
            result = action(text="bearing_plate_set", concate=True, depth=1.2, pos=[0, 0, 0])
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertEqual(item["shape"], "text")
        self.assertEqual(item["text"], "bps")
        self.assertEqual(item["height"], 1.2)
        self.assertEqual(item["size"], 7)
        self.assertEqual(item["font"], "Candara:Light")
        self.assertEqual(item["halign"], "center")
        self.assertEqual(item["valign"], "center")

    def test_shape_dispatch_accepts_oobb_text(self):
        import sys

        sys.modules.pop("oobb", None)
        with mock.patch.dict("sys.modules", {"opsc": _fake_opsc()}):
            import oobb

            result = oobb.oobb_easy(s="oobb_text", t="positive", text="OOBB", pos=[0, 0, 0])
            self.assertTrue(result)
            self.assertEqual(result[0][0]["shape"], "text")

    def test_metadata_is_documentation_ready(self):
        from components.oobb_text.working import define

        metadata = define()
        self.assertEqual(metadata["name"], "oobb_text")
        self.assertIn("oobb_text", metadata["shape_aliases"])
        self.assertTrue(metadata["description"])
        self.assertGreaterEqual(len(metadata["variables"]), 8)


if __name__ == "__main__":
    unittest.main()
