import unittest

from oobb_arch.catalog.migration_status import get_all_legacy_object_functions, get_migration_status


class MigrationStatusEnhancedTests(unittest.TestCase):
    def test_get_all_legacy_object_functions(self):
        items = get_all_legacy_object_functions()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)
        for item in items:
            self.assertIn("type_name", item)
            self.assertIn("function_name", item)
            self.assertIn("source_module", item)

        names = {item["type_name"] for item in items}
        self.assertIn("circle", names)
        self.assertIn("bolt", names)

    def test_migration_status_reports_migrated(self):
        status = get_migration_status()
        objects = status["objects"]
        sets = status["sets"]

        self.assertIn("circle", objects["migrated"])
        self.assertIn("bolt", objects["migrated"])
        self.assertIn("test_gear", objects["migrated"])
        self.assertNotIn("circle", objects["pending"])

        self.assertIn("bearing_circles", sets["migrated"])
        self.assertIn("jigs", sets["migrated"])
        self.assertIn("others", sets["migrated"])

    def test_migration_status_percentages(self):
        status = get_migration_status()
        objects = status["objects"]
        sets = status["sets"]

        self.assertGreater(objects["percentage"], 0)
        self.assertGreater(sets["percentage"], 0)
        self.assertGreaterEqual(objects["total_legacy"], objects["total_migrated"])


if __name__ == "__main__":
    unittest.main()
