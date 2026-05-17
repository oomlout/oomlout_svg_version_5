import unittest
from types import SimpleNamespace
from unittest import mock
import sys

from oobb_arch.catalog import BuilderRegistry
from oobb_arch.catalog.legacy_registry import build_legacy_builder_registry
from oobb_arch.compat import legacy_api
from oobb_arch.domain import BuildRequest, PartSpec
from oobb_arch.engine import build_from_plan, plan_build


class ArchitectureScaffoldTests(unittest.TestCase):
    def test_registry_register_and_resolve(self):
        reg = BuilderRegistry()

        def fake_builder(item):
            return {"id": "example", "components": [], "item": item}

        reg.register("plate", fake_builder)
        self.assertTrue(reg.has("plate"))
        self.assertIs(reg.resolve("plate"), fake_builder)

    def test_plan_and_build_stub(self):
        spec = PartSpec(identifier="demo_part", part_type="plate", payload={"type": "plate"})
        request = BuildRequest(part=spec)

        plan = plan_build(request)
        result = build_from_plan(plan)

        self.assertEqual(result.part_id, "demo_part")
        self.assertEqual(result.artifacts, [])

    def test_legacy_registry_preserves_first_module_precedence(self):
        first = SimpleNamespace(get_plate=lambda **kwargs: {"source": "first", **kwargs})
        second = SimpleNamespace(get_plate=lambda **kwargs: {"source": "second", **kwargs})

        registry = build_legacy_builder_registry([first, second])
        resolved = registry.resolve("plate")
        thing = resolved(type="plate")

        self.assertEqual(thing["source"], "first")

    def test_compat_legacy_api_delegates_to_oobb_base(self):
        fake = SimpleNamespace(
            get_thing_from_dict=lambda payload: {"id": "from_fake", "payload": payload},
            build_thing=lambda *args, **kwargs: {"build_thing": True, "args": args, "kwargs": kwargs},
            build_things=lambda *args, **kwargs: {"build_things": True, "args": args, "kwargs": kwargs},
        )

        with mock.patch.dict(sys.modules, {"oobb_base": fake}):
            thing = legacy_api.get_thing_from_dict({"type": "demo"})
            one = legacy_api.build_thing("id_1", overwrite=True)
            many = legacy_api.build_things(["id_1", "id_2"])

        self.assertEqual(thing["id"], "from_fake")
        self.assertTrue(one["build_thing"])
        self.assertTrue(many["build_things"])


if __name__ == "__main__":
    unittest.main()
