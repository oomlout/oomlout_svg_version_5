# Step 8 — Bulk Other + Test Object Migration (~24 objects)

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 7 (Bulk OOBB Core Object Migration) must be complete and all tests passing  
> **Blocks:** Step 10

---

## Goal

Use the scaffold generator to migrate all remaining `get_*()` functions from `oobb_get_items_other.py` and `oobb_get_items_test.py` to per-folder `working.py` files. After this step, **every object type** in the codebase lives in `part_calls/objects/oobb_object_<type>/working.py`.

---

## Background — Remaining Object Inventory

### `oobb_get_items_other.py` (9 functions)

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| 1 | `get_bolt` | `oobb_object_bolt` | Hardware |
| 2 | `get_nut` | `oobb_object_nut` | Hardware |
| 3 | `get_nut_m3` | `oobb_object_nut_m3` | Hardware |
| 4 | `get_screw_countersunk` | `oobb_object_screw_countersunk` | Hardware |
| 5 | `get_screw_self_tapping` | `oobb_object_screw_self_tapping` | Hardware |
| 6 | `get_screw_socket_cap` | `oobb_object_screw_socket_cap` | Hardware |
| 7 | `get_standoff` | `oobb_object_standoff` | Hardware |
| 8 | `get_threaded_insert` | `oobb_object_threaded_insert` | Hardware |
| 9 | `get_bearing` | `oobb_object_bearing` | Hardware |

**Note**: `oobb_object_bolt` already exists from Step 2 — skip with `overwrite=False`.

### `oobb_get_items_test.py` (15 functions)

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| 1 | `get_test_gear` | `oobb_object_test_gear` | OOBB Test |
| 2 | `get_test_hole` | `oobb_object_test_hole` | OOBB Test |
| 3 | `get_test_rotation` | `oobb_object_test_rotation` | OOBB Test |
| 4 | `get_test_motor_tt_01` | `oobb_object_test_motor_tt_01` | OOBB Test |
| 5 | `get_test_motor_tt_01_shaft` | `oobb_object_test_motor_tt_01_shaft` | OOBB Test |
| 6 | `get_test_motor_n20_shaft` | `oobb_object_test_motor_n20_shaft` | OOBB Test |
| 7 | `get_test_oobb_motor_servo_standard_01` | `oobb_object_test_oobb_motor_servo_standard_01` | OOBB Test |
| 8 | `get_test_oobb_nut` | `oobb_object_test_oobb_nut` | OOBB Test |
| 9 | `get_test_oobb_screw_socket_cap` | `oobb_object_test_oobb_screw_socket_cap` | OOBB Test |
| 10 | `get_test_oobb_screw_countersunk` | `oobb_object_test_oobb_screw_countersunk` | OOBB Test |
| 11 | `get_test_oobb_screw_self_tapping` | `oobb_object_test_oobb_screw_self_tapping` | OOBB Test |
| 12 | `get_test_oobb_screw` | `oobb_object_test_oobb_screw` | OOBB Test |
| 13 | `get_test_oobb_shape_slot` | `oobb_object_test_oobb_shape_slot` | OOBB Test |
| 14 | `get_test_oobb_wire` | `oobb_object_test_oobb_wire` | OOBB Test |
| 15 | `get_test_oobb_screw_socket_cap_old_1` | `oobb_object_test_oobb_screw_socket_cap_old_1` | OOBB Test |

**Note**: `oobb_object_test_gear` already exists from Step 2 — skip with `overwrite=False`.

---

## Execution Strategy

### Phase A: Auto-scaffold Other objects

```python
import oobb_get_items_other

for name in dir(oobb_get_items_other):
    if name.startswith("get_") and callable(getattr(oobb_get_items_other, name)):
        type_name = name[4:]
        generate_object_scaffold(
            type_name, "oobb_get_items_other", name,
            overwrite=False  # Don't overwrite bolt from Step 2
        )
```

### Phase B: Auto-scaffold Test objects

```python
import oobb_get_items_test

for name in dir(oobb_get_items_test):
    if name.startswith("get_") and callable(getattr(oobb_get_items_test, name)):
        type_name = name[4:]
        generate_object_scaffold(
            type_name, "oobb_get_items_test", name,
            overwrite=False  # Don't overwrite test_gear from Step 2
        )
```

### Phase C: Enrich key metadata

For the most commonly used Hardware objects, manually enhance descriptions:

- **bolt**: "Generates a hex-head bolt with specified thread size and length."
- **nut**: "Generates a hex nut matching the specified thread size."
- **screw_socket_cap**: "Generates a socket head cap screw."
- **bearing**: "Generates a bearing (608ZZ etc.) for rotational applications."

For test objects, the auto-generated descriptions are acceptable since they're primarily used for development validation.

### Phase D: Verify completeness

```python
# After scaffolding, run migration status:
from oobb_arch.catalog.migration_status import get_migration_status

status = get_migration_status()
assert len(status["objects"]["pending"]) == 0, f"Still pending: {status['objects']['pending']}"
```

---

## Files Created

| File | Purpose |
|------|---------|
| `part_calls/objects/oobb_object_nut/working.py` | Nut builder |
| `part_calls/objects/oobb_object_nut_m3/working.py` | M3 nut builder |
| `part_calls/objects/oobb_object_screw_countersunk/working.py` | Countersunk screw |
| `part_calls/objects/oobb_object_screw_self_tapping/working.py` | Self-tapping screw |
| `part_calls/objects/oobb_object_screw_socket_cap/working.py` | Socket cap screw |
| `part_calls/objects/oobb_object_standoff/working.py` | Standoff |
| `part_calls/objects/oobb_object_threaded_insert/working.py` | Threaded insert |
| `part_calls/objects/oobb_object_bearing/working.py` | Bearing |
| `part_calls/objects/oobb_object_test_hole/working.py` | Test hole |
| `part_calls/objects/oobb_object_test_rotation/working.py` | Test rotation |
| `part_calls/objects/oobb_object_test_motor_tt_01/working.py` | Test motor TT-01 |
| `part_calls/objects/oobb_object_test_motor_tt_01_shaft/working.py` | Test motor shaft |
| `part_calls/objects/oobb_object_test_motor_n20_shaft/working.py` | Test N20 motor |
| `part_calls/objects/oobb_object_test_oobb_motor_servo_standard_01/working.py` | Test servo |
| `part_calls/objects/oobb_object_test_oobb_nut/working.py` | Test nut |
| `part_calls/objects/oobb_object_test_oobb_screw_socket_cap/working.py` | Test screw |
| `part_calls/objects/oobb_object_test_oobb_screw_countersunk/working.py` | Test countersunk |
| `part_calls/objects/oobb_object_test_oobb_screw_self_tapping/working.py` | Test self-tapping |
| `part_calls/objects/oobb_object_test_oobb_screw/working.py` | Test screw generic |
| `part_calls/objects/oobb_object_test_oobb_shape_slot/working.py` | Test slot shape |
| `part_calls/objects/oobb_object_test_oobb_wire/working.py` | Test wire |
| `part_calls/objects/oobb_object_test_oobb_screw_socket_cap_old_1/working.py` | Test screw old |

**~22 new folders** (8 Other + 14 Test, excluding bolt and test_gear from Step 2)

---

## Tests

### `tests/test_other_test_object_migration.py`

Five test cases:

#### `test_all_other_functions_have_folders`
- Import `oobb_get_items_other` and list all `get_*` functions
- For each, assert `part_calls/objects/oobb_object_<type>/working.py` exists

#### `test_all_test_functions_have_folders`
- Import `oobb_get_items_test` and list all `get_*` functions
- For each, assert `part_calls/objects/oobb_object_<type>/working.py` exists

#### `test_zero_pending_objects`
- Call `get_migration_status()`
- Assert `objects["pending"]` is empty
- Assert `objects["total_migrated"] == objects["total_legacy"]`
- Assert `objects["percentage"] == 100.0`

#### `test_hardware_objects_have_enhanced_metadata`
- Load working.py for `oobb_object_nut`, `oobb_object_screw_socket_cap`, `oobb_object_bearing`
- Assert `define()` returns metadata with non-stub `description`

#### `test_all_discovered_objects_have_action_fn`
- Call `discover_objects()`
- For each discovered object, assert `action_fn` is callable
- Assert total discovered count ≥ 60 (all three source modules combined)

---

## Test Contract

**All of the following must pass before proceeding to Step 9:**

```powershell
# New tests
python -m unittest tests.test_other_test_object_migration -v

# Step 7 tests
python -m unittest tests.test_oobb_core_object_migration -v

# Documentation tests (must now reflect all objects)
python -m unittest tests.test_documentation_generation -v

# Steps 1-3 tests
python -m unittest tests.test_object_discovery tests.test_object_working_files tests.test_object_dispatch_integration -v

# Pre-existing tests
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] Every `get_*()` function in `oobb_get_items_other` has a corresponding folder
- [ ] Every `get_*()` function in `oobb_get_items_test` has a corresponding folder
- [ ] `get_migration_status()` reports 100% object migration
- [ ] `objects["pending"]` is empty
- [ ] Hardware objects (nut, screw_socket_cap, bearing) have enriched descriptions
- [ ] `discover_objects()` discovers all folders (count ≥ 60)
- [ ] All discovered objects have callable `action_fn`
- [ ] No snapshot/capability test regressions
- [ ] All 5 new tests pass
- [ ] All pre-existing tests still pass

---

## Estimated Scope

- ~22 generated working.py files × ~40 lines = ~880 lines (mostly auto-generated)
- Manual enrichment of 4–5 key Hardware objects = ~100 lines
- ~60 lines of test code
- No changes to any existing production code

---

## Risk Notes

- **oobb_get_items_test.py import chain**: This module imports `oobb_get_items_oobb` and `oobb_get_items_other` for test geometry composition. The scaffold's `action()` doing `import oobb_get_items_test` will trigger these imports at call time, which is fine since all modules are available.
- **Long function names**: Some test functions have very long names (e.g. `get_test_oobb_screw_socket_cap_old_1`). The corresponding folder name will be `oobb_object_test_oobb_screw_socket_cap_old_1` — long but consistent.
- **Pre-existing circle/bolt/test_gear**: The `overwrite=False` flag ensures the enriched working.py files from Step 2 are preserved.
