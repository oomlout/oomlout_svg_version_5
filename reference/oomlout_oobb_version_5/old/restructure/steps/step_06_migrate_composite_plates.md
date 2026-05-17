# Step 06 — Migrate Composite Plate Functions

## Objective

Move the geometry code for the 4 composite plate functions from `oobb_get_items_oobb.py` into their folder `working.py` files. These are "composite" objects — they compose sub-parts by calling `oobb_base.get_thing_from_dict({"type": "plate", ...})`.

## Prerequisite

- Steps 01–05 completed
- `get_plate_base` already migrated (Step 05) and available via dispatch
- All tests pass

## Functions to Migrate (4 total)

| Function | Lines in `oobb_get_items_oobb.py` | Folder | LOC | Composition Pattern |
|----------|-----------------------------------|--------|-----|---------------------|
| `get_plate_l(**kwargs)` | 578–634 | `oobb_object_plate_l` | ~55 | Composes 2 plates via `get_thing_from_dict` |
| `get_plate_t(**kwargs)` | 788–845 | `oobb_object_plate_t` | ~55 | Composes 2 plates via `get_thing_from_dict` |
| `get_plate_u(**kwargs)` | 846–896 | `oobb_object_plate_u` | ~50 | Composes plate_l + extra arm via `get_thing_from_dict` |
| `get_plate_u_double(**kwargs)` | 897–960 | `oobb_object_plate_u_double` | ~60 | Composes 2 side plates + bottom via `get_thing_from_dict` |

## Dependency Chain

```
plate_u_double  →  get_thing_from_dict({"type": "plate", ...})
plate_u         →  get_thing_from_dict({"type": "plate", "extra": "l"})  →  get_plate_l via dispatch
plate_t         →  get_thing_from_dict({"type": "plate", ...})
plate_l         →  get_thing_from_dict({"type": "plate", ...})
```

All of these call `oobb_base.get_thing_from_dict()` to compose sub-plates. After Step 05, `plate_base` is in its folder, and `plate` router still works (it hasn't been migrated yet — Step 08 will do that). So the dispatch chain works:

```
plate_l calls get_thing_from_dict({"type": "plate", ...})
  → get_plate() in legacy (still there)
    → get_plate_base() forwarder → folder action()
```

**Migration order within this step:** `plate_l` first, then `plate_t`, then `plate_u` (depends on plate_l via dispatch), then `plate_u_double`.

## Migration Pattern

### Example: `get_plate_l` → `oobb_object_plate_l/working.py`

```python
def action(**kwargs):
    import copy
    import oobb_base

    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    thickness = kwargs.get("thickness", 3)
    size = kwargs.get("size", "oobb")
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    full_object = kwargs.get("full_object", True)
    holes = kwargs.get("holes", True)
    both_holes = kwargs.get("both_holes", True)
    kwargs["pos"] = pos

    thing = oobb_base.get_default_thing(**kwargs)
    th = thing["components"]
    kwargs.pop("size", "")

    # width plate
    p3 = copy.deepcopy(kwargs)
    pos1 = copy.deepcopy(pos)
    p3["pos"] = pos1
    p3["type"] = "plate"
    p3["width"] = width
    p3["height"] = 1
    p3["full_object"] = False
    p3.pop("extra", "")
    width_plate = oobb_base.get_thing_from_dict(p3)  # ← composition via dispatch
    th.append(width_plate)

    # height plate
    p3 = copy.deepcopy(p3)
    pos1 = copy.deepcopy(pos)
    pos1[0] += -(width - 1) / 2 * 15
    pos1[1] += (height - 1) / 2 * 15
    p3["pos"] = pos1
    p3["width"] = 1
    p3["height"] = height
    height_plate = oobb_base.get_thing_from_dict(p3)  # ← composition via dispatch
    th.append(height_plate)

    if full_object:
        return thing
    else:
        return th
```

### Legacy Forwarder

```python
def get_plate_l(**kwargs):
    # MIGRATED → part_calls/objects/oobb_object_plate_l/
    from part_calls.objects.oobb_object_plate_l.working import action
    return action(**kwargs)
```

## What Gets Modified

### Folder `working.py` files (4 files):
- `part_calls/objects/oobb_object_plate_l/working.py`
- `part_calls/objects/oobb_object_plate_t/working.py`
- `part_calls/objects/oobb_object_plate_u/working.py`
- `part_calls/objects/oobb_object_plate_u_double/working.py`

### Legacy module:
- `oobb_get_items_oobb.py` — 4 function bodies replaced with forwarders

## Tests

### `tests/test_step06_composite_plate_migration.py`

```python
"""
Step 06 — Verify composite plate migration.
Each function's folder output must match its legacy output exactly.
"""
import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_get_items_oobb
from oobb_arch.testing.output_compare import compare_outputs

class TestPlateLMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_plate_l.working import action
        kwargs = {"type": "plate_l", "width": 3, "height": 3, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate_l(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate_l mismatch: {diff}")

    def test_varied_sizes(self):
        from part_calls.objects.oobb_object_plate_l.working import action
        for w, h in [(2, 4), (5, 2), (1, 1)]:
            with self.subTest(w=w, h=h):
                kwargs = {"type": "plate_l", "width": w, "height": h, "thickness": 3, "size": "oobb"}
                legacy = oobb_get_items_oobb.get_plate_l(**kwargs)
                folder = action(**kwargs)
                is_eq, diff = compare_outputs(legacy, folder)
                self.assertTrue(is_eq, diff)

class TestPlateTMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_plate_t.working import action
        kwargs = {"type": "plate_t", "width": 5, "height": 3, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate_t(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate_t mismatch: {diff}")

class TestPlateUMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_plate_u.working import action
        kwargs = {"type": "plate_u", "width": 3, "height": 3, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate_u(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate_u mismatch: {diff}")

class TestPlateUDoubleMigration(unittest.TestCase):
    def test_output_matches(self):
        from part_calls.objects.oobb_object_plate_u_double.working import action
        kwargs = {"type": "plate_u_double", "width": 5, "height": 3, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate_u_double(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate_u_double mismatch: {diff}")

class TestCompositionChain(unittest.TestCase):
    def test_plate_u_uses_plate_l_via_dispatch(self):
        """plate_u composes plate_l via get_thing_from_dict — verify the chain works."""
        import oobb_base
        result = oobb_base.get_thing_from_dict(
            {"type": "plate", "extra": "u", "width": 3, "height": 3, "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

class TestLegacyForwarders(unittest.TestCase):
    def test_all_forwarders(self):
        for func_name in ["get_plate_l", "get_plate_t", "get_plate_u", "get_plate_u_double"]:
            with self.subTest(func=func_name):
                func = getattr(oobb_get_items_oobb, func_name)
                result = func(type=func_name.replace("get_", ""),
                              width=3, height=3, thickness=3, size="oobb")
                self.assertIsInstance(result, dict)
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step06_composite_plate_migration.py` (6 new tests with subtests) pass.

## Rollback

1. Restore original function bodies in `oobb_get_items_oobb.py` (lines 578–960)
2. Restore original `working.py` files in the 4 folders
3. Delete `tests/test_step06_composite_plate_migration.py`
