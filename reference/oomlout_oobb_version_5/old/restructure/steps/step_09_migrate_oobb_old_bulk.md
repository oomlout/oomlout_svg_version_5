# Step 09 — Migrate `oobb_get_items_oobb_old.py` + Satellite Modules

## Objective

Move the geometry code for all functions in the large legacy modules into their folder `working.py` files:
- `oobb_get_items_oobb_old.py` (73 functions, ~4,900 lines)
- `oobb_get_items_oobb_holder.py` (18 functions, ~828 lines)
- `oobb_get_items_oobb_holder_electronic.py` (9 functions, ~295 lines)
- `oobb_get_items_oobb_bearing_plate.py` (9 functions, ~820 lines)
- `oobb_get_items_oobb_wire.py` (16 functions, ~200 lines)
- `oobb_get_items_oobb_other.py` (8 functions, ~620 lines)
- `oobb_get_items_oobb_wheel.py` (4 functions, ~160 lines)

This is the largest step but follows the exact same pattern established in Steps 03–08.

## Prerequisite

- Steps 01–08 completed
- All router functions migrated
- All tests pass

## Total Functions: ~137

This step is broken into **7 waves**, one per source module. Each wave is an atomic sub-commit.

### Wave 1: `oobb_get_items_oobb_wheel.py` (4 functions — smallest)

| Function | Folder |
|----------|--------|
| `get_wheel_no_tire` | `oobb_object_wheel_no_tire` |
| `get_wheel` | `oobb_object_wheel` (already has router — move wheel code here) |
| `get_wheel_bearing` | `oobb_object_wheel_bearing` |
| `get_wheel_bearing_twenty_twenty_aluminium_extrusion` | `oobb_object_wheel_bearing_twenty_twenty_aluminium_extrusion` |

### Wave 2: `oobb_get_items_oobb_other.py` (8 functions)

| Function | Folder |
|----------|--------|
| `get_other_bolt_stacker` | `oobb_object_other_bolt_stacker` |
| `get_other_bolt_stacker_cylinder` | `oobb_object_other_bolt_stacker_cylinder` |
| `get_other_corner_cube` | `oobb_object_other_corner_cube` |
| `get_other_corner_cube_basic` | `oobb_object_other_corner_cube_basic` (create new folder) |
| `get_other_corner_cube_relief` | `oobb_object_other_corner_cube_relief` |
| `get_other_ptfe_tube_holder` | `oobb_object_other_ptfe_tube_holder` (create new folder) |
| `get_other_ptfe_tube_holder_ninety_degree` | `oobb_object_other_ptfe_tube_holder_ninety_degree` (create new folder) |
| `get_other_timing_belt_clamp_gt2` | `oobb_object_other_timing_belt_clamp_gt2` (create new folder) |

### Wave 3: `oobb_get_items_oobb_wire.py` (16 functions)

All `get_wire_*` functions and `get_oobb_wire_base`. Note: `get_plate_nut_dict` is a helper — move it to `oobb_arch/helpers/`.

### Wave 4: `oobb_get_items_oobb_holder_electronic.py` (9 functions)

All `get_holder_electronic_*` functions. Note: `get_plate_cutout_dict` and `get_plate_screw_dict` are helpers — move them to `oobb_arch/helpers/`.

### Wave 5: `oobb_get_items_oobb_holder.py` (18 functions)

All `get_holder_motor_*` and `get_holder_electronic_*` forwarder functions.

### Wave 6: `oobb_get_items_oobb_bearing_plate.py` (9 functions)

`get_bearing_plate` and its sub-functions (`_connecting_screw_center`, `_connecting_screw_perimeter`, `_hole_center`, etc.).

**Note:** The sub-functions like `get_bearing_plate_connecting_screw_center(thing, **kwargs)` take a `thing` as first arg — these are internal helpers, not dispatched objects. They should move WITH `get_bearing_plate` into the same folder as private functions.

### Wave 7: `oobb_get_items_oobb_old.py` (73 functions — largest)

This is the bulk. Categories:

| Category | Functions | Count |
|----------|-----------|-------|
| Bearing | `bearing_circle`, `bearing_wheel`, `bearing_plate_old`, `bearing_plate_shim`, `bearing_plate_jack`, `bearing_plate_jack_basic` | 6 |
| Bracket | `bracket_2020_aluminium_extrusion` | 1 |
| Bunting | `bunting_alphabet` | 1 |
| Circle | `circle_old_1`, `circle_captive`, `ci_holes_center` | 3 |
| Holders (motor) | `holder_old`, `holder_fan_120_mm`, `holder_motor_building_block_*` (4), `holder_motor_gearmotor_*` (3), `holder_motor_servo_*` (5), `holder_motor_stepper_*` (3), `holder_powerbank_*` (1) | ~17 |
| Holders (electronics) | `holder_electronics_*` (6) | 6 |
| Jack | `jack`, `jack_basic` | 2 |
| Jig | `jig`, `jig_tray_03_03`, `jig_screw_sorter_m3_03_03` | 3 |
| Mounting plate | `mounting_plate`, `mounting_plate_side`, `mounting_plate_top`, `mounting_plate_generic`, `mounting_plate_u` | 5 |
| Plate | `plate_old` | 1 |
| Shaft | `shaft_coupler`, `shaft` | 2 |
| SMD magazine | `smd_magazine*` (7 variants) | 7 |
| Soldering jig | `soldering_jig*` (2) | 2 |
| Tool holder | `tool_holder*` (4) | 4 |
| Tray | `tray*` (7 variants) | 7 |
| Other | `wheel_old_1`, `wire_old`, `ziptie_holder*` (2) | 4 |

## Migration Pattern (same as all previous steps)

For each function:

1. **Copy** function body into folder `working.py` `action(**kwargs)`
2. **Replace** legacy function body with one-line forwarder
3. **Update** `define()` metadata (remove "Auto-generated scaffold")
4. **Verify** output matches via comparison harness

### New Folders Needed

Some functions in `oobb_old` don't have folders yet. The scaffold generator from the previous migration created most, but a few may be missing. For any missing folder:

```python
# Create: part_calls/objects/oobb_object_{name}/working.py
d = {}
def define():
    global d
    if not d:
        d = {
            "name": "oobb_object_{name}",
            "name_short": ["{name}"],
            "name_long": "OOBB Object: {Name}",
            "description": "...",
            "category": "...",
            "source_module": "oobb_get_items_oobb_old",
        }
    return dict(d)

def action(**kwargs):
    # ... moved code ...

def test(**kwargs):
    try:
        result = action(type="{name}", ...)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
```

### Special: `bearing_plate` Sub-Functions

`get_bearing_plate_connecting_screw_center(thing, **kwargs)` etc. are internal helpers — they take `thing` as a first argument and are called only by `get_bearing_plate`. Move them into the `oobb_object_bearing_plate/working.py` file as module-level functions (not `action()`):

```python
# part_calls/objects/oobb_object_bearing_plate/working.py
def _connecting_screw_center(thing, **kwargs):
    # ... moved code ...

def _connecting_screw_perimeter(thing, **kwargs):
    # ... moved code ...

def action(**kwargs):
    # ... main bearing_plate code, calls _connecting_screw_center etc. ...
```

## Tests

### `tests/test_step09_old_bulk_migration.py`

```python
"""
Step 09 — Verify bulk migration of oobb_old and satellite modules.
Tests a representative sample from each wave.
"""
import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_base
from oobb_arch.testing.output_compare import compare_outputs

class TestWave1Wheel(unittest.TestCase):
    def test_wheel_no_tire(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "wheel_no_tire", "diameter": 3, "thickness": 3,
             "size": "oobb", "shaft": "m6"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

class TestWave2OobbOther(unittest.TestCase):
    def test_other_bolt_stacker(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "other_bolt_stacker", "radius_name": "m3",
             "width": 3, "height": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)

class TestWave3Wire(unittest.TestCase):
    def test_wire_basic(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "wire", "extra": "basic", "size": "oobb",
             "width": 3, "height": 1, "thickness": 3})
        self.assertIsInstance(result, dict)

class TestWave6BearingPlate(unittest.TestCase):
    def test_bearing_plate(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "bearing_plate", "width": 3, "height": 3,
             "thickness": 12, "bearing": "606", "size": "oobb"})
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)

class TestWave7OobbOld(unittest.TestCase):
    def test_bearing_circle(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "bearing_circle", "diameter": 3, "thickness": 6,
             "bearing_type": "606", "size": "oobb"})
        self.assertIsInstance(result, dict)

    def test_tray(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "tray", "width": 3, "height": 3, "thickness": 3,
             "size": "oobb"})
        self.assertIsInstance(result, dict)

    def test_mounting_plate(self):
        result = oobb_base.get_thing_from_dict(
            {"type": "mounting_plate", "width": 3, "height": 3,
             "thickness": 3, "size": "oobb"})
        self.assertIsInstance(result, dict)

class TestAllLegacyForwarders(unittest.TestCase):
    def test_oobb_old_has_forwarders(self):
        """Spot-check that legacy functions are now forwarders."""
        from oobb_arch.testing.forwarder_check import is_forwarder
        import oobb_get_items_oobb_old
        for func_name in ["get_bearing_circle", "get_tray", "get_mounting_plate"]:
            with self.subTest(func=func_name):
                is_fwd, info = is_forwarder(oobb_get_items_oobb_old, func_name)
                self.assertTrue(is_fwd, f"{func_name} is not a forwarder: {info}")

    def test_oobb_holder_has_forwarders(self):
        import oobb_get_items_oobb_holder
        for func_name in ["get_holder_motor_tt_01", "get_holder_motor_servo_standard_01_top"]:
            with self.subTest(func=func_name):
                is_fwd, info = is_forwarder(oobb_get_items_oobb_holder, func_name)
                self.assertTrue(is_fwd, f"{func_name} is not a forwarder: {info}")

class TestMigrationCount(unittest.TestCase):
    def test_all_old_functions_are_forwarders(self):
        """Every get_* function in oobb_old should be a forwarder."""
        from oobb_arch.testing.forwarder_check import is_forwarder
        import oobb_get_items_oobb_old
        import inspect
        members = inspect.getmembers(oobb_get_items_oobb_old, inspect.isfunction)
        get_functions = [(n, f) for n, f in members
                         if n.startswith("get_") and f.__module__ == "oobb_get_items_oobb_old"]
        non_forwarders = []
        for name, func in get_functions:
            is_fwd, _ = is_forwarder(oobb_get_items_oobb_old, name)
            if not is_fwd:
                non_forwarders.append(name)
        self.assertEqual(non_forwarders, [],
                         f"These functions are not yet forwarders: {non_forwarders}")
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_step09_old_bulk_migration.py` (10 new tests) pass.

## Rollback

Per-wave rollback: restore the original function bodies in each source module and restore the original `working.py` wrappers.
