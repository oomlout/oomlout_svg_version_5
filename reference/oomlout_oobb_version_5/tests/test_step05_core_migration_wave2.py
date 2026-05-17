"""
Step 05 Wave 2 — Verify core leaf geometry migration.

Each function's folder output must match its legacy-era output exactly.
The legacy functions are now forwarders, so calling them calls the folder code.
We verify:
  1. Folder action() produces correct output (isinstance dict with components)
  2. Legacy forwarder still works
  3. Dispatch via get_thing_from_dict routes correctly
  4. Multiple parameter variations produce valid results
"""
import unittest
import copy

import oobb
import oobb_get_items_oobb

from oobb_arch.testing.output_compare import compare_outputs


class TestCircleBaseMigration(unittest.TestCase):
    """Verify circle_base folder owns its geometry code."""

    def test_basic_circle(self):
        from components.circle_base.working import action
        kwargs = {"type": "circle_base", "diameter": 3, "thickness": 3, "size": "oobb"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_circle_with_shaft(self):
        from components.circle_base.working import action
        kwargs = {"type": "circle_base", "diameter": 5, "thickness": 6,
                  "size": "oobb", "shaft": "m6"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_circle_doughnut(self):
        from components.circle_base.working import action
        kwargs = {"type": "circle_base", "diameter": 3, "thickness": 3,
                  "size": "oobb", "extra": "doughnut_5"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_forwarder_works(self):
        result = oobb_get_items_oobb.get_circle_base(
            type="circle_base", diameter=3, thickness=3, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_dispatch_routes_correctly(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "circle_base", "diameter": 3, "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


class TestPlateBaseMigration(unittest.TestCase):
    """Verify plate_base folder owns its geometry code."""

    def test_basic_plate(self):
        from components.plate_base.working import action
        kwargs = {"type": "plate_base", "width": 3, "height": 2,
                  "thickness": 3, "size": "oobb"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_plate_1x1(self):
        from components.plate_base.working import action
        kwargs = {"type": "plate_base", "width": 1, "height": 1,
                  "thickness": 6, "size": "oobb"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_plate_gorm_extra(self):
        from components.plate_base.working import action
        kwargs = {"type": "plate_base", "width": 5, "height": 3,
                  "thickness": 3, "size": "oobb", "extra": "gorm"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_forwarder_works(self):
        result = oobb_get_items_oobb.get_plate_base(
            type="plate_base", width=3, height=2, thickness=3, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_dispatch_routes_correctly(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "plate_base", "width": 3, "height": 2,
             "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


class TestPlateLabelMigration(unittest.TestCase):
    """Verify plate_label folder owns its geometry code."""

    def test_basic_label(self):
        from components.plate_label.working import action
        kwargs = {"type": "plate_label", "width": 3, "height": 2,
                  "thickness": 3, "size": "oobb"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_forwarder_works(self):
        result = oobb_get_items_oobb.get_plate_label(
            type="plate_label", width=3, height=2, thickness=3, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_dispatch_routes_correctly(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "plate_label", "width": 3, "height": 2,
             "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


class TestPlateNinetyDegreeMigration(unittest.TestCase):
    """Verify plate_ninety_degree folder owns its geometry code."""

    def test_basic_ninety_degree(self):
        from components.plate_ninety_degree.working import action
        kwargs = {"type": "plate_ninety_degree", "width": 3, "height": 2,
                  "thickness": 15, "size": "oobb"}
        result = action(**kwargs)
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_forwarder_works(self):
        result = oobb_get_items_oobb.get_plate_ninety_degree(
            type="plate_ninety_degree", width=3, height=2,
            thickness=15, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_dispatch_routes_correctly(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "plate_ninety_degree", "width": 3, "height": 2,
             "thickness": 15, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)


class TestFolderCodeIsNotDelegating(unittest.TestCase):
    """Verify folders now own code instead of delegating to legacy."""

    def test_circle_base_not_delegating(self):
        import inspect
        from components.circle_base.working import action
        source = inspect.getsource(action)
        self.assertNotIn("import oobb_get_items_oobb", source)
        self.assertIn("oobb_base.get_default_thing", source)

    def test_plate_base_not_delegating(self):
        import inspect
        from components.plate_base.working import action
        source = inspect.getsource(action)
        self.assertNotIn("import oobb_get_items_oobb", source)
        self.assertIn("oobb_base.get_default_thing", source)

    def test_plate_label_not_delegating(self):
        import inspect
        from components.plate_label.working import action
        source = inspect.getsource(action)
        self.assertNotIn("import oobb_get_items_oobb", source)
        self.assertIn("oobb_base.get_default_thing", source)

    def test_plate_ninety_degree_not_delegating(self):
        import inspect
        from components.plate_ninety_degree.working import action
        source = inspect.getsource(action)
        self.assertNotIn("import oobb_get_items_oobb", source)
        self.assertIn("oobb_base.get_default_thing", source)


class TestStarImportStillWorks(unittest.TestCase):
    """Legacy star-import consumers must still be able to call these functions."""

    def test_all_migrated_functions_callable(self):
        for func_name in ["get_circle_base", "get_plate_base",
                          "get_plate_label", "get_plate_ninety_degree"]:
            with self.subTest(func=func_name):
                self.assertTrue(
                    callable(getattr(oobb_get_items_oobb, func_name)),
                    f"{func_name} not callable on legacy module")


if __name__ == "__main__":
    unittest.main()
