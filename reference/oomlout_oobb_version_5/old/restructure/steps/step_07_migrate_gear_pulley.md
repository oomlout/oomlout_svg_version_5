# Step 07 — Migrate Gear & Pulley Functions

## Objective

Move the geometry code for gear and pulley functions from `oobb_get_items_oobb.py` into their folder `working.py` files. These are medium-high complexity: gears have shaft logic and double-stack composition.

## Prerequisite

- Steps 01–06 completed
- `add_oobb_shaft` and `get_shaft_center` available in `oobb_arch/helpers/`
- All tests pass

## Functions to Migrate (4 total)

| Function | Lines in `oobb_get_items_oobb.py` | Folder | LOC | Dependencies |
|----------|-----------------------------------|--------|-----|--------------|
| `get_gear(**kwargs)` | 174–381 | `oobb_object_gear` | ~210 | `add_oobb_shaft` (helper), calls `get_gear_double_stack` for list diameters |
| `get_gear_double_stack(**kwargs)` | 382–428 | `oobb_object_gear_double_stack` | ~45 | Composes via `get_thing_from_dict(p3)` with `type` kept in dict |
| `get_pulley_gt2(**kwargs)` | 961–1195 | `oobb_object_pulley_gt2` | ~235 | `oobb_base` only |
| `get_pulley_gt2_shield_double(**kwargs)` | 1196–1401 | `oobb_object_pulley_gt2_shield_double` | ~205 | `oobb_base` only |

## Dependency Analysis

### `get_gear()` → `get_gear_double_stack()`

Currently, `get_gear()` directly calls `get_gear_double_stack(**kwargs)` when `diameter` is a list:

```python
def get_gear(**kwargs):
    ...
    if isinstance(diameter, list):
        return get_gear_double_stack(**kwargs)
```

After migration, this should route through dispatch:

```python
def action(**kwargs):
    ...
    if isinstance(diameter, list):
        return oobb_base.get_thing_from_dict({**kwargs, "type": "gear_double_stack"})
```

### `get_gear_double_stack()` → composition

`get_gear_double_stack` composes sub-gears via `oobb_base.get_thing_from_dict(p3)`. The `p3` dict still has the original `type` from kwargs — after migration we need to ensure it sets `type` properly for sub-gear dispatch. Looking at the code, `p3` gets `type` from kwargs which is likely "gear" + extra, so it naturally routes to the gear folder.

### Migration Order

1. `get_pulley_gt2` — standalone, no cross-calls
2. `get_pulley_gt2_shield_double` — standalone, no cross-calls
3. `get_gear_double_stack` — uses dispatch for composition
4. `get_gear` — depends on gear_double_stack (now in folder, routed via dispatch)

## What Gets Modified

### Folder `working.py` files (4 files):
- `part_calls/objects/oobb_object_gear/working.py`
- `part_calls/objects/oobb_object_gear_double_stack/working.py`
- `part_calls/objects/oobb_object_pulley_gt2/working.py`
- `part_calls/objects/oobb_object_pulley_gt2_shield_double/working.py`

### Legacy module:
- `oobb_get_items_oobb.py` — 4 function bodies + `add_oobb_shaft` replaced with forwarders
  - Note: `add_oobb_shaft` is NOT replaced as a forwarder — it was already extracted to `oobb_arch/helpers/` in Step 02. It stays as-is in the legacy module for backward compatibility.

### Key change in `get_gear` migration:

```python
# BEFORE (in legacy)
if isinstance(diameter, list):
    return get_gear_double_stack(**kwargs)

# AFTER (in folder working.py)
if isinstance(diameter, list):
    import oobb_base
    return oobb_base.get_thing_from_dict({**kwargs, "type": "gear_double_stack"})
```

## Tests

### `tests/test_step07_gear_pulley_migration.py`

```python
"""
Step 07 — Verify gear and pulley migration.
"""
import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_get_items_oobb
from oobb_arch.testing.output_compare import compare_outputs

class TestGearMigration(unittest.TestCase):
    def test_simple_gear(self):
        from part_calls.objects.oobb_object_gear.working import action
        kwargs = {"type": "gear", "diameter": 3, "thickness": 3, "size": "oobb", "extra": ""}
        legacy = oobb_get_items_oobb.get_gear(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"gear mismatch: {diff}")

    def test_gear_with_shaft(self):
        from part_calls.objects.oobb_object_gear.working import action
        kwargs = {"type": "gear", "diameter": 5, "thickness": 6, "size": "oobb",
                  "shaft": "m6", "extra": ""}
        legacy = oobb_get_items_oobb.get_gear(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"gear+shaft mismatch: {diff}")

class TestGearDoubleStackMigration(unittest.TestCase):
    def test_double_stack(self):
        from part_calls.objects.oobb_object_gear_double_stack.working import action
        kwargs = {"type": "gear_double_stack", "diameter": [3, 5],
                  "thickness": 6, "size": "oobb", "extra": ["", ""],
                  "shaft": "m6"}
        legacy = oobb_get_items_oobb.get_gear_double_stack(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"gear_double_stack mismatch: {diff}")

    def test_gear_routes_to_double_stack_for_list(self):
        """get_gear with list diameter should route to gear_double_stack."""
        import oobb_base
        result = oobb_base.get_thing_from_dict(
            {"type": "gear", "diameter": [3, 5], "thickness": 6,
             "size": "oobb", "extra": ["", ""], "shaft": "m6"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

class TestPulleyGt2Migration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_pulley_gt2.working import action
        kwargs = {"type": "pulley_gt2", "diameter": 3, "thickness": 3,
                  "size": "oobb", "extra": "", "shaft": "m6"}
        legacy = oobb_get_items_oobb.get_pulley_gt2(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"pulley_gt2 mismatch: {diff}")

class TestPulleyGt2ShieldDoubleMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_pulley_gt2_shield_double.working import action
        kwargs = {"type": "pulley_gt2_shield_double", "diameter": 3,
                  "thickness": 3, "size": "oobb", "extra": "", "shaft": "m6"}
        legacy = oobb_get_items_oobb.get_pulley_gt2_shield_double(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"pulley_gt2_shield_double mismatch: {diff}")

class TestLegacyForwarders(unittest.TestCase):
    def test_gear_forwarder(self):
        result = oobb_get_items_oobb.get_gear(
            type="gear", diameter=3, thickness=3, size="oobb", extra="")
        self.assertIsInstance(result, dict)

    def test_pulley_forwarder(self):
        result = oobb_get_items_oobb.get_pulley_gt2(
            type="pulley_gt2", diameter=3, thickness=3, size="oobb", extra="", shaft="m6")
        self.assertIsInstance(result, dict)
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step07_gear_pulley_migration.py` (8 new tests) pass.

## Rollback

1. Restore original function bodies in `oobb_get_items_oobb.py` (lines 174–428, 961–1401)
2. Restore original `working.py` files in the 4 folders
3. Delete `tests/test_step07_gear_pulley_migration.py`
