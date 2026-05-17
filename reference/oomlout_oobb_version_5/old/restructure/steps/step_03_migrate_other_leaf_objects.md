# Step 03 — Migrate `oobb_get_items_other.py` Leaf Objects

## Objective

Move the geometry code for all 8 functions in `oobb_get_items_other.py` into their respective folder `working.py` files. These are the simplest leaf objects — no internal cross-calls, no `getattr` dispatch, no composition.

## Prerequisite

- Steps 01–02 completed
- All tests pass

## Functions to Migrate (8 total)

All in `oobb_get_items_other.py` (132 lines total):

| Function | Lines | Folder | Complexity |
|----------|-------|--------|------------|
| `get_bolt(**kwargs)` | 5–17 | `oobb_object_bolt` | Simple |
| `get_nut_m3()` | 19–21 | (helper, stays) | Trivial |
| `get_nut(**kwargs)` | 24–40 | `oobb_object_nut` | Simple |
| `get_screw_countersunk(**kwargs)` | 43–55 | `oobb_object_screw_countersunk` | Simple |
| `get_screw_self_tapping(**kwargs)` | 56–68 | `oobb_object_screw_self_tapping` | Simple |
| `get_screw_socket_cap(**kwargs)` | 69–82 | `oobb_object_screw_socket_cap` | Simple |
| `get_standoff(**kwargs)` | 83–100 | `oobb_object_standoff` | Simple |
| `get_threaded_insert(**kwargs)` | 102–118 | `oobb_object_threaded_insert` | Simple |
| `get_bearing(**kwargs)` | 120–132 | `oobb_object_bearing` | Simple |

Note: `get_nut_m3()` is a trivial helper that calls `get_nut(3)` — it stays in the legacy module as a compatibility shim.

## Migration Pattern (applied to each function)

### A. Move code into folder `working.py`

Example for `get_bolt`:

```python
# part_calls/objects/oobb_object_bolt/working.py — AFTER
d = {}

def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bolt",
            "name_short": ["bolt"],
            "name_long": "OOBB Object: Bolt",
            "description": "Generates a bolt with specified radius and depth.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Bolt radius (e.g. m3, m4)", "type": "string"},
                {"name": "depth", "description": "Bolt depth in mm", "type": "number"},
            ],
            "source_module": "oobb_get_items_other",
        }
    return dict(d)

def action(**kwargs):
    """Build and return the bolt thing dict."""
    import oobb_base as ob
    from oobb_get_items_base import *  # for base helpers

    wid = kwargs["radius_name"]
    depth = kwargs["depth"]
    thing = ob.get_default_thing(**kwargs)
    thing.update({"description": f"bolt {wid}x{depth}"})
    thing.update({"depth_mm": depth})
    thing.update({"components": []})
    thing["components"].extend(ob.oe(
        t="positive", s="oobb_bolt", rn=wid, depth=depth, rotY=0, include_nut=False))
    return thing

def test(**kwargs):
    """Smoke test for bolt generation."""
    try:
        result = action(type="bolt", radius_name="m3", depth=10)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
```

### B. Replace legacy function with forwarder

```python
# oobb_get_items_other.py — AFTER
def get_bolt(**kwargs):
    # MIGRATED → part_calls/objects/oobb_object_bolt/
    from part_calls.objects.oobb_object_bolt.working import action
    return action(**kwargs)
```

### C. Update `define()` metadata

Remove "Auto-generated scaffold" from description so aliases activate in discovery.

## What Gets Modified

### Folder `working.py` files (8 files):
- `part_calls/objects/oobb_object_bolt/working.py`
- `part_calls/objects/oobb_object_nut/working.py`
- `part_calls/objects/oobb_object_screw_countersunk/working.py`
- `part_calls/objects/oobb_object_screw_self_tapping/working.py`
- `part_calls/objects/oobb_object_screw_socket_cap/working.py`
- `part_calls/objects/oobb_object_standoff/working.py`
- `part_calls/objects/oobb_object_threaded_insert/working.py`
- `part_calls/objects/oobb_object_bearing/working.py`

### Legacy module:
- `oobb_get_items_other.py` — all 8 `get_*` bodies replaced with forwarders

## Tests

### `tests/test_step03_other_migration.py`

```python
"""
Step 03 — Verify oobb_get_items_other migration.
Each function's folder output must match its legacy output exactly.
"""
import unittest
import oobb
import oobb_get_items_other

class TestBoltMigration(unittest.TestCase):
    def test_bolt_output_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_bolt.working import action
        kwargs = {"type": "bolt", "radius_name": "m3", "depth": 10}
        legacy = oobb_get_items_other.get_bolt(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"Bolt mismatch: {diff}")

class TestNutMigration(unittest.TestCase):
    def test_nut_output_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_nut.working import action
        kwargs = {"type": "nut", "radius_name": "m3"}
        legacy = oobb_get_items_other.get_nut(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"Nut mismatch: {diff}")

class TestScrewMigrations(unittest.TestCase):
    def test_screw_countersunk_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_screw_countersunk.working import action
        kwargs = {"type": "screw_countersunk", "radius_name": "m3", "depth": 10}
        legacy = oobb_get_items_other.get_screw_countersunk(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, diff)

    def test_screw_self_tapping_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_screw_self_tapping.working import action
        kwargs = {"type": "screw_self_tapping", "radius_name": "m3", "depth": 10}
        legacy = oobb_get_items_other.get_screw_self_tapping(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, diff)

    def test_screw_socket_cap_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_screw_socket_cap.working import action
        kwargs = {"type": "screw_socket_cap", "radius_name": "m3", "depth": 10}
        legacy = oobb_get_items_other.get_screw_socket_cap(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, diff)

class TestStandoffMigration(unittest.TestCase):
    def test_standoff_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_standoff.working import action
        kwargs = {"type": "standoff", "radius_name": "m3", "depth": 10}
        legacy = oobb_get_items_other.get_standoff(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, diff)

class TestThreadedInsertMigration(unittest.TestCase):
    def test_threaded_insert_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_threaded_insert.working import action
        kwargs = {"type": "threaded_insert", "radius_name": "m3"}
        legacy = oobb_get_items_other.get_threaded_insert(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, diff)

class TestBearingMigration(unittest.TestCase):
    def test_bearing_matches(self):
        from oobb_arch.testing.output_compare import compare_outputs
        from part_calls.objects.oobb_object_bearing.working import action
        kwargs = {"type": "bearing", "bearing_name": "606"}
        legacy = oobb_get_items_other.get_bearing(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, diff)

class TestLegacyForwarders(unittest.TestCase):
    def test_all_forwarders_work(self):
        """Legacy module functions still return valid dicts via forwarders."""
        self.assertIsInstance(
            oobb_get_items_other.get_bolt(type="bolt", radius_name="m3", depth=10), dict)
        self.assertIsInstance(
            oobb_get_items_other.get_nut(type="nut", radius_name="m3"), dict)
        self.assertIsInstance(
            oobb_get_items_other.get_bearing(type="bearing", bearing_name="606"), dict)

    def test_dispatch_routes_through_discovery(self):
        """oobb_base.get_thing_from_dict routes to folder action."""
        import oobb_base
        result = oobb_base.get_thing_from_dict(
            {"type": "bolt", "radius_name": "m3", "depth": 10})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step03_other_migration.py` (10 new tests) pass.

## Rollback

1. Restore original function bodies in `oobb_get_items_other.py`
2. Restore original `working.py` files in the 8 folders (they were thin wrappers)
3. Delete `tests/test_step03_other_migration.py`
