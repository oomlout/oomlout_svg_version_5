# Step 04 — Migrate `oobb_get_items_test.py` Leaf Objects

## Objective

Move the geometry code for all 15 functions in `oobb_get_items_test.py` into their respective folder `working.py` files. These are test/demo objects — they exercise various OOBB features but are relatively standalone.

## Prerequisite

- Steps 01–03 completed
- All tests pass

## Functions to Migrate (15 total)

All in `oobb_get_items_test.py` (~1,500 lines total):

| Function | Lines | Folder | Internal Calls |
|----------|-------|--------|----------------|
| `get_test_gear(**kwargs)` | 6–103 | `oobb_object_test_gear` | Uses `oobb_base` only |
| `get_test_hole(**kwargs)` | 104–177 | `oobb_object_test_hole` | Uses `oobb_base` only |
| `get_test_rotation(**kwargs)` | 178–238 | `oobb_object_test_rotation` | Uses `oobb_base` only |
| `get_test_motor_tt_01(**kwargs)` | 239–326 | `oobb_object_test_motor_tt_01` | Uses `oobb_base` only |
| `get_test_motor_tt_01_shaft(**kwargs)` | 327–413 | `oobb_object_test_motor_tt_01_shaft` | Uses `oobb_base` only |
| `get_test_motor_n20_shaft(**kwargs)` | 414–496 | `oobb_object_test_motor_n20_shaft` | Uses `oobb_base` only |
| `get_test_oobb_motor_servo_standard_01(**kwargs)` | 497–569 | `oobb_object_test_oobb_motor_servo_standard_01` | Uses `oobb_base` only |
| `get_test_oobb_nut(**kwargs)` | 570–715 | `oobb_object_test_oobb_nut` | Uses `oobb_base` only |
| `get_test_oobb_screw_socket_cap(**kwargs)` | 716–719 | `oobb_object_test_oobb_screw_socket_cap` | Calls `get_test_oobb_screw` |
| `get_test_oobb_screw_countersunk(**kwargs)` | 720–723 | `oobb_object_test_oobb_screw_countersunk` | Calls `get_test_oobb_screw` |
| `get_test_oobb_screw_self_tapping(**kwargs)` | 724–727 | `oobb_object_test_oobb_screw_self_tapping` | Calls `get_test_oobb_screw` |
| `get_test_oobb_screw(**kwargs)` | 728–904 | `oobb_object_test_oobb_screw` | Uses `oobb_base` only |
| `get_test_oobb_screw_socket_cap_old_1(**kwargs)` | 905–1400 | `oobb_object_test_oobb_screw_socket_cap_old_1` | Uses `oobb_base` only |
| `get_test_oobb_shape_slot(**kwargs)` | 1401–1485 | `oobb_object_test_oobb_shape_slot` | Uses `oobb_base` only |
| `get_test_oobb_wire(**kwargs)` | 1486–end | `oobb_object_test_oobb_wire` | Uses `oobb_base` only |

## Migration Order (dependency-aware)

1. **Wave 1:** Migrate standalone functions (12 functions) — no internal cross-calls
2. **Wave 2:** Migrate `get_test_oobb_screw()` (the base function)
3. **Wave 3:** Migrate the 3 screw wrappers (`screw_socket_cap`, `screw_countersunk`, `screw_self_tapping`) — these call `get_test_oobb_screw()` which by now is in a folder, so they should call through dispatch: `oobb_base.get_thing_from_dict({"type": "test_oobb_screw", ...})`

## Special Handling: Screw Wrappers

The three screw wrappers currently call `get_test_oobb_screw()` directly:

```python
# BEFORE
def get_test_oobb_screw_socket_cap(**kwargs):
    kwargs["screw_type"] = "screw_socket_cap"
    return get_test_oobb_screw(**kwargs)
```

After migration, they should route through dispatch:

```python
# AFTER — in folder working.py
def action(**kwargs):
    import oobb_base
    kwargs["screw_type"] = "screw_socket_cap"
    kwargs["type"] = "test_oobb_screw"
    return oobb_base.get_thing_from_dict(kwargs)
```

## What Gets Modified

### Folder `working.py` files (15 files):
All under `part_calls/objects/oobb_object_test_*`

### Legacy module:
- `oobb_get_items_test.py` — all 15 `get_*` bodies replaced with forwarders

## Tests

### `tests/test_step04_test_migration.py`

```python
"""
Step 04 — Verify oobb_get_items_test migration.
Each function's folder output must match its legacy output exactly.
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_get_items_test

class TestTestGearMigration(unittest.TestCase):
    def test_output_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_test_gear.working import action
        kwargs = {"type": "test_gear", "diameter": 3, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_test.get_test_gear(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"test_gear mismatch: {diff}")

class TestTestHoleMigration(unittest.TestCase):
    def test_output_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_test_hole.working import action
        kwargs = {"type": "test_hole"}
        legacy = oobb_get_items_test.get_test_hole(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"test_hole mismatch: {diff}")

class TestTestScrewMigration(unittest.TestCase):
    def test_screw_base_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_test_oobb_screw.working import action
        kwargs = {"type": "test_oobb_screw", "screw_type": "screw_socket_cap"}
        legacy = oobb_get_items_test.get_test_oobb_screw(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"test_oobb_screw mismatch: {diff}")

    def test_screw_socket_cap_wrapper_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_test_oobb_screw_socket_cap.working import action
        kwargs = {"type": "test_oobb_screw_socket_cap"}
        legacy = oobb_get_items_test.get_test_oobb_screw_socket_cap(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"test_oobb_screw_socket_cap mismatch: {diff}")

class TestAllForwardersWork(unittest.TestCase):
    def test_legacy_forwarders(self):
        """All legacy functions still return valid dicts via forwarders."""
        result = oobb_get_items_test.get_test_gear(
            type="test_gear", diameter=3, thickness=3, size="oobb")
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

    def test_dispatch_routes_through_discovery(self):
        """oobb_base routes test_ types to folder action."""
        import oobb_base
        result = oobb_base.get_thing_from_dict(
            {"type": "test_gear", "diameter": 3, "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step04_test_migration.py` (6 new tests) pass.

## Rollback

1. Restore original function bodies in `oobb_get_items_test.py`
2. Restore original `working.py` files in the 15 folders
3. Delete `tests/test_step04_test_migration.py`
