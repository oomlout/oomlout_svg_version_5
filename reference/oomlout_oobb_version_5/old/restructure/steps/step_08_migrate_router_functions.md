# Step 08 — Migrate Router Functions (circle, plate, holder, other, test, wheel, wire)

## Objective

Migrate the 7 "router" functions that dispatch to sub-functions based on the `extra` kwarg. These are the gateway functions — they don't do geometry themselves, they route to specialized builders. After this step, the routers live in their own folders and use clean `oobb_base.get_thing_from_dict()` dispatch instead of `getattr`/`importlib.reload` hacks.

## Prerequisite

- Steps 01–07 completed (all leaf/composite functions already migrated to folders)
- All tests pass

## Functions to Migrate (7 total)

| Function | Lines in source | Folder | Pattern |
|----------|----------------|--------|---------|
| `get_circle(**kwargs)` | `oobb_get_items_oobb.py:40–71` | `oobb_object_circle` | `getattr` + `importlib.reload` → `get_plate_{extra}` or `get_circle_base` |
| `get_plate(**kwargs)` | `oobb_get_items_oobb.py:471–492` | `oobb_object_plate` | `getattr` + `importlib.reload` → `get_plate_{extra}` or `get_plate_base` |
| `get_gear(**kwargs)` | Already migrated in Step 07 | `oobb_object_gear` | Routes list-diameter to `gear_double_stack` — **already done** |
| `get_holder(**kwargs)` | `oobb_get_items_oobb.py:429–453` | `oobb_object_holder` | `getattr` on `oobb_get_items_oobb_holder` → `get_holder_{extra}` |
| `get_other(**kwargs)` | `oobb_get_items_oobb.py:455–469` | `oobb_object_other` | `getattr` on `oobb_get_items_oobb_other` → `get_other_{extra}` |
| `get_test(**kwargs)` | `oobb_get_items_oobb.py:1436–1451` | `oobb_object_test` | `getattr` on `oobb_get_items_test` → `get_test_{extra}` |
| `get_wheel(**kwargs)` | `oobb_get_items_oobb.py:1452–1469` | `oobb_object_wheel` | `getattr` on `oobb_get_items_oobb_wheel` → `get_wheel_{extra}` |
| `get_wire(**kwargs)` | `oobb_get_items_oobb.py:1472–1490` | `oobb_object_wire` | `getattr` on `oobb_get_items_oobb_wire` → `get_wire_{extra}` |

Note: `get_gear` was already handled in Step 07. We migrate the remaining 6 here.

## The Key Transformation

### BEFORE (legacy — uses `getattr` hacks):

```python
def get_circle(**kwargs):
    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    if extra != "" and "doughnut" not in extra:
        function_name = "get_plate_" + extra
        import sys, importlib
        importlib.reload(sys.modules[__name__])
        function_to_call = getattr(sys.modules[__name__], function_name)
        return function_to_call(**kwargs)
    else:
        return get_circle_base(**kwargs)
```

### AFTER (folder — uses clean dispatch):

```python
def action(**kwargs):
    import copy
    import oobb_base

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    thickness = p3.get("thickness", 3)
    zz = p3.get("zz", "bottom")
    pos = p3.get("pos", [0, 0, 0])

    # Handle z-position
    if zz == "bottom":
        pass
    elif zz == "middle":
        pos[2] += -thickness / 2
    elif zz == "top":
        pos[2] += -thickness
    p3["pos"] = pos

    if extra != "" and "doughnut" not in extra:
        # Route to plate_{extra} via standard dispatch
        p3["type"] = f"plate_{extra}"
        return oobb_base.get_thing_from_dict(p3)
    else:
        # Route to circle_base via standard dispatch
        p3["type"] = "circle_base"
        return oobb_base.get_thing_from_dict(p3)
```

### Pattern for holder/other/test/wheel/wire:

```python
# holder
def action(**kwargs):
    import copy
    import oobb_base

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    if extra != "":
        p3["type"] = f"holder_{extra}"
        return oobb_base.get_thing_from_dict(p3)
    else:
        raise ValueError("holder requires 'extra' parameter")
```

This is cleaner because:
- No `importlib.reload` (which was causing stale module state)
- No `getattr` on runtime-loaded modules
- Sub-types route through discovery → they find their folder `working.py`
- If a sub-type's folder doesn't have real code yet, dispatch falls through to the legacy forwarder

## What Gets Modified

### Folder `working.py` files (6 files updated):
- `part_calls/objects/oobb_object_circle/working.py`
- `part_calls/objects/oobb_object_plate/working.py`
- `part_calls/objects/oobb_object_holder/working.py`
- `part_calls/objects/oobb_object_other/working.py`
- `part_calls/objects/oobb_object_test/working.py`
- `part_calls/objects/oobb_object_wheel/working.py`
- `part_calls/objects/oobb_object_wire/working.py`

### Legacy module:
- `oobb_get_items_oobb.py` — 6 router function bodies replaced with forwarders

## Special Handling: `get_plate` Fallback

The current `get_plate()` has a fallback: if `get_plate_{extra}` doesn't exist, it calls `get_plate_base()`:

```python
try:
    function_to_call = getattr(sys.modules[__name__], function_name)
    return function_to_call(**kwargs)
except:
    print(f"Function {function_name} not found using basic plate")
    return get_plate_base(**kwargs)
```

The migrated version preserves this:

```python
def action(**kwargs):
    import copy
    import oobb_base

    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    p3.pop("extra", "")

    if extra != "":
        p3["type"] = f"plate_{extra}"
        try:
            return oobb_base.get_thing_from_dict(p3)
        except Exception:
            print(f"plate_{extra} not found, using plate_base")
            p3["type"] = "plate_base"
            return oobb_base.get_thing_from_dict(p3)
    else:
        p3["type"] = "plate_base"
        return oobb_base.get_thing_from_dict(p3)
```

## Tests

### `tests/test_step08_router_migration.py`

```python
"""
Step 08 — Verify router function migration.
Routers must produce identical output to legacy when dispatching to sub-types.
"""
import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_base
import oobb_get_items_oobb
from oobb_arch.testing.output_compare import compare_outputs

class TestCircleRouter(unittest.TestCase):
    def test_circle_basic(self):
        """circle with no extra → circle_base"""
        from part_calls.objects.oobb_object_circle.working import action
        kwargs = {"type": "circle", "diameter": 3, "thickness": 3, "size": "oobb", "extra": ""}
        legacy = oobb_get_items_oobb.get_circle(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"circle basic mismatch: {diff}")

    def test_circle_doughnut(self):
        """circle with doughnut extra → circle_base (doughnut handled inside)"""
        kwargs = {"type": "circle", "diameter": 3, "thickness": 3,
                  "size": "oobb", "extra": "doughnut_5"}
        from part_calls.objects.oobb_object_circle.working import action
        legacy = oobb_get_items_oobb.get_circle(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"circle doughnut mismatch: {diff}")

    def test_circle_dispatch_via_base(self):
        """Full dispatch: get_thing_from_dict → circle folder → circle_base folder"""
        result = oobb_base.get_thing_from_dict(
            {"type": "circle", "diameter": 3, "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

class TestPlateRouter(unittest.TestCase):
    def test_plate_basic(self):
        """plate with no extra → plate_base"""
        from part_calls.objects.oobb_object_plate.working import action
        kwargs = {"type": "plate", "width": 3, "height": 2, "thickness": 3, "size": "oobb"}
        legacy = oobb_get_items_oobb.get_plate(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate basic mismatch: {diff}")

    def test_plate_l_via_router(self):
        """plate with extra=l → plate_l"""
        kwargs = {"type": "plate", "extra": "l", "width": 3, "height": 3,
                  "thickness": 3, "size": "oobb"}
        from part_calls.objects.oobb_object_plate.working import action
        legacy = oobb_get_items_oobb.get_plate(**kwargs)
        folder = action(**kwargs)
        is_eq, diff = compare_outputs(legacy, folder)
        self.assertTrue(is_eq, f"plate→l mismatch: {diff}")

class TestHolderRouter(unittest.TestCase):
    def test_holder_dispatch(self):
        """holder extra dispatches to sub-type via discovery."""
        result = oobb_base.get_thing_from_dict(
            {"type": "holder", "extra": "motor_tt_01", "size": "oobb",
             "width": 3, "height": 3, "thickness": 12})
        self.assertIsInstance(result, dict)

class TestWheelRouter(unittest.TestCase):
    def test_wheel_dispatch(self):
        """wheel dispatches to oobb_get_items_oobb_wheel via folder."""
        result = oobb_base.get_thing_from_dict(
            {"type": "wheel", "extra": "", "size": "oobb",
             "diameter": 3, "thickness": 3})
        self.assertIsInstance(result, dict)

class TestNoGetattr(unittest.TestCase):
    def test_circle_folder_has_no_getattr(self):
        """Migrated circle folder must not use getattr/importlib.reload."""
        import inspect
        from part_calls.objects.oobb_object_circle.working import action
        source = inspect.getsource(action)
        self.assertNotIn("importlib.reload", source)
        self.assertNotIn("getattr(sys.modules", source)

    def test_plate_folder_has_no_getattr(self):
        import inspect
        from part_calls.objects.oobb_object_plate.working import action
        source = inspect.getsource(action)
        self.assertNotIn("importlib.reload", source)
        self.assertNotIn("getattr(sys.modules", source)

class TestLegacyForwarders(unittest.TestCase):
    def test_all_router_forwarders(self):
        for func_name, kwargs in [
            ("get_circle", {"type": "circle", "diameter": 3, "thickness": 3, "size": "oobb"}),
            ("get_plate", {"type": "plate", "width": 3, "height": 2, "thickness": 3, "size": "oobb"}),
        ]:
            with self.subTest(func=func_name):
                func = getattr(oobb_get_items_oobb, func_name)
                result = func(**kwargs)
                self.assertIsInstance(result, dict)
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step08_router_migration.py` (10 new tests) pass.

## Rollback

1. Restore original router function bodies in `oobb_get_items_oobb.py`
2. Restore original `working.py` files in the 7 folders
3. Delete `tests/test_step08_router_migration.py`
