# Step 05 — Migrate Core Leaf Geometry from `oobb_get_items_oobb.py`

## Objective

Move the actual geometry code for the 4 core standalone builder functions from `oobb_get_items_oobb.py` into their folder `working.py` files. These are "leaf" functions that build geometry using only `oobb_base` utilities — they do NOT call other `get_*` functions (except `get_shaft_center` which is now a shared helper from Step 02).

## Prerequisite

- Steps 01–04 completed
- Shared helpers (`get_shaft_center`, `add_oobb_shaft`) available in `oobb_arch/helpers/`
- All tests pass

## Functions to Migrate (4 total)

| Function | Lines in `oobb_get_items_oobb.py` | Folder | LOC | Dependencies |
|----------|-----------------------------------|--------|-----|--------------|
| `get_circle_base(**kwargs)` | 72–173 | `oobb_object_circle_base` | ~100 | `oobb_base`, `get_shaft_center` (helper) |
| `get_plate_base(**kwargs)` | 493–577 | `oobb_object_plate_base` | ~85 | `oobb_base`, `math` |
| `get_plate_ninety_degree(**kwargs)` | 684–787 | `oobb_object_plate_ninety_degree` | ~100 | `oobb_base` |
| `get_plate_label(**kwargs)` | 635–683 | `oobb_object_plate_label` | ~50 | `oobb_base`, calls `get_thing_from_dict({"type":"plate",...})` for sub-plate |

## Important: `get_plate_label` Dependency

`get_plate_label()` calls `oobb_base.get_thing_from_dict(p3)` with `p3["type"] = "plate"` to compose a sub-plate. This is fine — it routes through dispatch, which still works. The migrated code keeps this exact pattern.

## Migration Details

### `get_circle_base` → `oobb_object_circle_base/working.py`

```python
def action(**kwargs):
    import copy
    import oobb_base
    from oobb_arch.helpers.shaft_helpers import get_shaft_center

    # ... exact code from get_circle_base lines 72-173 ...
    # Replace: get_shaft_center(thing, **kwargs)
    # With:    get_shaft_center(thing, **kwargs)  (same — it's now imported from helpers)
```

### `get_plate_base` → `oobb_object_plate_base/working.py`

```python
def action(**kwargs):
    import copy
    import math
    import oobb_base

    # ... exact code from get_plate_base lines 493-577 ...
```

### `get_plate_ninety_degree` → `oobb_object_plate_ninety_degree/working.py`

```python
def action(**kwargs):
    import copy
    import oobb_base

    # ... exact code from get_plate_ninety_degree lines 684-787 ...
```

### `get_plate_label` → `oobb_object_plate_label/working.py`

```python
def action(**kwargs):
    import copy
    import oobb_base

    # ... exact code from get_plate_label lines 635-683 ...
    # The oobb_base.get_thing_from_dict(p3) call stays as-is
```

### Legacy Forwarders in `oobb_get_items_oobb.py`

Each original function body is replaced:

```python
def get_circle_base(**kwargs):
    # MIGRATED → part_calls/objects/oobb_object_circle_base/
    from part_calls.objects.oobb_object_circle_base.working import action
    return action(**kwargs)

def get_plate_base(**kwargs):
    # MIGRATED → part_calls/objects/oobb_object_plate_base/
    from part_calls.objects.oobb_object_plate_base.working import action
    return action(**kwargs)

def get_plate_ninety_degree(**kwargs):
    # MIGRATED → part_calls/objects/oobb_object_plate_ninety_degree/
    from part_calls.objects.oobb_object_plate_ninety_degree.working import action
    return action(**kwargs)

def get_plate_label(**kwargs):
    # MIGRATED → part_calls/objects/oobb_object_plate_label/
    from part_calls.objects.oobb_object_plate_label.working import action
    return action(**kwargs)
```

### Update `define()` Metadata

Update each folder's `define()` to have proper descriptions (remove "Auto-generated scaffold") so aliases activate.

## Tests

### `tests/test_step05_core_leaf_migration.py`

```python
"""
Step 05 — Verify core leaf geometry migration.
Each function's folder output must match its legacy output exactly.
"""
import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_get_items_oobb
from oobb_arch.testing.output_compare import compare_outputs

class TestCircleBaseMigration(unittest.TestCase):
    CASES = [
        {"type": "circle_base", "diameter": 3, "thickness": 3, "size": "oobb"},
        {"type": "circle_base", "diameter": 5, "thickness": 6, "size": "oobb", "shaft": "m6"},
        {"type": "circle_base", "diameter": 3, "thickness": 3, "size": "oobb", "extra": "doughnut_5"},
    ]

    def test_circle_base_output_matches(self):
        from part_calls.objects.oobb_object_circle_base.working import action
        for kwargs in self.CASES:
            with self.subTest(kwargs=kwargs):
                legacy = oobb_get_items_oobb.get_circle_base(**kwargs)
                folder = action(**kwargs)
                is_eq, diff = compare_outputs(legacy, folder)
                self.assertTrue(is_eq, f"circle_base mismatch: {diff}")

class TestPlateBaseMigration(unittest.TestCase):
    CASES = [
        {"type": "plate_base", "width": 3, "height": 2, "thickness": 3, "size": "oobb"},
        {"type": "plate_base", "width": 1, "height": 1, "thickness": 6, "size": "oobb"},
        {"type": "plate_base", "width": 5, "height": 3, "thickness": 3, "size": "oobb", "extra": "gorm"},
    ]

    def test_plate_base_output_matches(self):
        from part_calls.objects.oobb_object_plate_base.working import action
        for kwargs in self.CASES:
            with self.subTest(kwargs=kwargs):
                legacy = oobb_get_items_oobb.get_plate_base(**kwargs)
                folder = action(**kwargs)
                is_eq, diff = compare_outputs(legacy, folder)
                self.assertTrue(is_eq, f"plate_base mismatch: {diff}")

class TestPlateNinetyDegreeMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_plate_ninety_degree.working import action
        kwargs = {"type": "plate_ninety_degree", "width": 3, "height": 2, "thickness": 15, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate_ninety_degree(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate_ninety_degree mismatch: {diff}")

class TestPlateLabelMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_plate_label.working import action
        kwargs = {"type": "plate_label", "width": 3, "height": 2, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate_label(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate_label mismatch: {diff}")

class TestLegacyForwarders(unittest.TestCase):
    def test_circle_base_forwarder(self):
        result = oobb_get_items_oobb.get_circle_base(
            type="circle_base", diameter=3, thickness=3, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_plate_base_forwarder(self):
        result = oobb_get_items_oobb.get_plate_base(
            type="plate_base", width=3, height=2, thickness=3, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_star_import_still_works(self):
        """Functions available via star import from oobb_get_items_oobb."""
        self.assertTrue(callable(getattr(oobb_get_items_oobb, "get_circle_base")))
        self.assertTrue(callable(getattr(oobb_get_items_oobb, "get_plate_base")))
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step05_core_leaf_migration.py` (7 new tests) pass.

## Rollback

1. Restore original function bodies in `oobb_get_items_oobb.py` (lines 72–173, 493–577, 635–787)
2. Restore original `working.py` files in the 4 folders
3. Delete `tests/test_step05_core_leaf_migration.py`
