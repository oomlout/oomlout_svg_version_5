# Step 7 — Bulk OOBB Core Object Migration (~20 objects)

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 6 (Scaffold Generator & Migration Reporter) must be complete and all tests passing  
> **Blocks:** Step 10

---

## Goal

Use the scaffold generator from Step 6 to migrate all `get_*()` functions from `oobb_get_items_oobb.py` and its sub-modules to per-folder `working.py` files. After this step, every OOBB core geometry builder lives in `part_calls/objects/oobb_object_<type>/working.py`.

---

## Background — OOBB Core Object Inventory

The following `get_*()` functions exist in the OOBB core modules. Each becomes one folder:

### `oobb_get_items_oobb.py` (main module)

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| 1 | `get_circle` | `oobb_object_circle` | OOBB Geometry |
| 2 | `get_circle_base` | `oobb_object_circle_base` | OOBB Geometry |
| 3 | `get_gear` | `oobb_object_gear` | OOBB Geometry |
| 4 | `get_gear_double_stack` | `oobb_object_gear_double_stack` | OOBB Geometry |
| 5 | `get_holder` | `oobb_object_holder` | OOBB Geometry |
| 6 | `get_other` | `oobb_object_other` | OOBB Geometry |
| 7 | `get_plate` | `oobb_object_plate` | OOBB Geometry |
| 8 | `get_plate_base` | `oobb_object_plate_base` | OOBB Geometry |
| 9 | `get_plate_l` | `oobb_object_plate_l` | OOBB Geometry |
| 10 | `get_plate_label` | `oobb_object_plate_label` | OOBB Geometry |
| 11 | `get_plate_ninety_degree` | `oobb_object_plate_ninety_degree` | OOBB Geometry |
| 12 | `get_plate_t` | `oobb_object_plate_t` | OOBB Geometry |
| 13 | `get_plate_u` | `oobb_object_plate_u` | OOBB Geometry |
| 14 | `get_plate_u_double` | `oobb_object_plate_u_double` | OOBB Geometry |
| 15 | `get_pulley_gt2` | `oobb_object_pulley_gt2` | OOBB Geometry |
| 16 | `get_pulley_gt2_shield_double` | `oobb_object_pulley_gt2_shield_double` | OOBB Geometry |
| 17 | `get_shaft_center` | `oobb_object_shaft_center` | OOBB Geometry |
| 18 | `get_test` | `oobb_object_test` | OOBB Test |
| 19 | `get_wheel` | `oobb_object_wheel` | OOBB Geometry |

### `oobb_get_items_oobb_old.py` (star-imported into oobb)

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| 20 | `get_bearing_circle` | `oobb_object_bearing_circle` | OOBB Geometry (Legacy) |
| 21 | `get_bearing_wheel` | `oobb_object_bearing_wheel` | OOBB Geometry (Legacy) |
| 22 | `get_bearing_plate_old` | `oobb_object_bearing_plate_old` | OOBB Geometry (Legacy) |
| 23 | `get_bearing_plate_shim` | `oobb_object_bearing_plate_shim` | OOBB Geometry (Legacy) |
| 24 | `get_bearing_plate_jack` | `oobb_object_bearing_plate_jack` | OOBB Geometry (Legacy) |
| 25 | `get_bracket_2020` | `oobb_object_bracket_2020` | OOBB Geometry (Legacy) |
| 26 | `get_bunting_alphabet` | `oobb_object_bunting_alphabet` | OOBB Geometry (Legacy) |
| 27 | `get_circle_old_1` | `oobb_object_circle_old_1` | OOBB Geometry (Legacy) |
| 28 | `get_circle_captive` | `oobb_object_circle_captive` | OOBB Geometry (Legacy) |
| 29 | `get_holder_*` (multiple) | `oobb_object_holder_*` | OOBB Geometry (Legacy) |
| 30 | `get_smd_magazine_*` | `oobb_object_smd_magazine_*` | OOBB Geometry (Legacy) |
| 31 | `get_shaft` | `oobb_object_shaft` | OOBB Geometry (Legacy) |
| 32 | `get_tray_*` (multiple) | `oobb_object_tray_*` | OOBB Geometry (Legacy) |

### `oobb_get_items_oobb_wire.py`

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| 33 | `get_wire_basic` | `oobb_object_wire_basic` | OOBB Wire |
| 34 | `get_wire_motor` | `oobb_object_wire_motor` | OOBB Wire |
| 35 | `get_wire_spacer` | `oobb_object_wire_spacer` | OOBB Wire |
| 36 | `get_wire_spacer_long` | `oobb_object_wire_spacer_long` | OOBB Wire |
| 37 | `get_wire_spacer_u` | `oobb_object_wire_spacer_u` | OOBB Wire |

### `oobb_get_items_oobb_holder.py`

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| 38+ | `get_holder_electronic_*` | `oobb_object_holder_electronic_*` | OOBB Holder |
| | `get_holder_motor_servo_*` | `oobb_object_holder_motor_servo_*` | OOBB Holder |
| | `get_holder_motor_stepper_*` | `oobb_object_holder_motor_stepper_*` | OOBB Holder |
| | `get_holder_motor_tt_01` | `oobb_object_holder_motor_tt_01` | OOBB Holder |
| | `get_holder_motor_generic` | `oobb_object_holder_motor_generic` | OOBB Holder |

### `oobb_get_items_oobb_other.py`

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| | `get_other_bolt_stacker` | `oobb_object_other_bolt_stacker` | OOBB Other |
| | `get_other_corner_cube` | `oobb_object_other_corner_cube` | OOBB Other |
| | `get_other_ptfe_tube_holder` | `oobb_object_other_ptfe_tube_holder` | OOBB Other |
| | `get_other_timing_belt_clamp_gt2` | `oobb_object_other_timing_belt_clamp_gt2` | OOBB Other |

### `oobb_get_items_oobb_bearing_plate.py`

| # | Function | Folder Name | Category |
|---|----------|-------------|----------|
| | `get_bearing_plate` | `oobb_object_bearing_plate` | OOBB Bearing Plate |

---

## Execution Strategy

### Phase A: Auto-scaffold all objects

Use the scaffold generator to create all working.py files at once:

```python
import oobb_get_items_oobb

# Get all get_* functions from the module (includes star imports)
for name in dir(oobb_get_items_oobb):
    if name.startswith("get_") and callable(getattr(oobb_get_items_oobb, name)):
        type_name = name[4:]  # strip "get_"
        # Determine source module
        source = _determine_source_module(name, oobb_get_items_oobb)
        generate_object_scaffold(type_name, source, name)
```

### Phase B: Enhance metadata

For the most important/frequently used objects (circle, plate, gear, holder), manually enhance the `define()` metadata:
- Add descriptive `description` text
- Add detailed `variables` with types and defaults
- Add accurate `name_long`

Less important objects can keep the auto-generated stub metadata.

### Phase C: Test & verify

1. Run `discover_objects()` and verify count matches expected
2. Run `get_migration_status()` and verify all OOBB objects show as migrated
3. Run existing capability/snapshot tests to verify no regressions

**Note**: `oobb_object_circle` already exists from Step 2 — skip it during auto-scaffolding (use `overwrite=False`).

---

## Sub-module Source Detection

When auto-scaffolding, we need to determine which sub-module a function actually comes from (since they're star-imported into `oobb_get_items_oobb`):

```python
def _determine_source_module(func_name, parent_module):
    """Determine which sub-module a function originates from.
    
    Check in order:
    1. oobb_get_items_oobb_bearing_plate
    2. oobb_get_items_oobb_holder
    3. oobb_get_items_oobb_wire
    4. oobb_get_items_oobb_other
    5. oobb_get_items_oobb_old
    6. oobb_get_items_oobb (defined directly)
    """
```

---

## Files Created

| File | Purpose |
|------|---------|
| `part_calls/objects/oobb_object_<type>/working.py` × ~50 | Per-object folder working files |

## Files Modified

| File | Change |
|------|--------|
| None | This step only creates new folders/files |

---

## Tests

### `tests/test_oobb_core_object_migration.py`

Five test cases:

#### `test_all_oobb_get_items_oobb_functions_have_folders`
- Import `oobb_get_items_oobb` and list all `get_*` functions
- For each function, assert `part_calls/objects/oobb_object_<type>/working.py` exists

#### `test_all_migrated_objects_are_discoverable`
- Call `discover_objects()` on real `part_calls/objects` root
- For each `get_*` function from `oobb_get_items_oobb`, assert corresponding type is in discovered dict

#### `test_migration_status_shows_oobb_complete`
- Call `get_migration_status()`
- Assert every OOBB-sourced object is in `migrated` (not in `pending`)

#### `test_key_objects_have_rich_metadata`
- Load working.py for `oobb_object_circle`, `oobb_object_plate`, `oobb_object_gear`
- Assert `define()` returns metadata with non-empty `description` (not the auto-stub text)
- Assert `variables` list has at least 2 entries

#### `test_dispatching_still_works`
- Quick sanity: call `get_thing_from_dict({"type": "plate", ...minimal args...})` 
- Assert it returns a valid thing dict
- This ensures the newly-discovered objects work through the dispatch chain

---

## Test Contract

**All of the following must pass before proceeding to Step 8:**

```powershell
# New tests
python -m unittest tests.test_oobb_core_object_migration -v

# Step 6 tests (scaffold & migration reporter)
python -m unittest tests.test_object_scaffold_generator tests.test_migration_status_enhanced -v

# Documentation tests
python -m unittest tests.test_documentation_generation -v

# Steps 1-3 tests
python -m unittest tests.test_object_discovery tests.test_object_working_files tests.test_object_dispatch_integration -v

# Pre-existing tests (CRITICAL — snapshot/capability must not regress)
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests.test_dump_json_and_load_json_round_trip -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] Every `get_*()` function in `oobb_get_items_oobb` (and star-imported sub-modules) has a corresponding `part_calls/objects/oobb_object_<type>/working.py`
- [ ] Each generated file has `define()`, `action()`, `test()` callables
- [ ] `action()` delegates to the correct legacy function in the correct source module
- [ ] Key objects (circle, plate, gear, holder) have enriched metadata with descriptions and variables
- [ ] Auto-generated scaffolds have correct `source_module` field in metadata
- [ ] `discover_objects()` discovers all created folders
- [ ] `get_migration_status()` shows all OOBB core objects as migrated
- [ ] `get_thing_from_dict()` dispatch still works correctly for all OOBB types
- [ ] No snapshot/capability test regressions
- [ ] All 5 new tests pass

---

## Estimated Scope

- ~50 generated working.py files × ~40 lines each = ~2000 lines (mostly auto-generated)
- Manual enrichment of 5–10 key objects = ~200 lines of hand-edited metadata
- ~80 lines of test code
- No changes to any existing production code

---

## Risk Notes

- **Star imports**: `oobb_get_items_oobb.py` uses `from oobb_get_items_oobb_old import *` etc. The scaffold generator must trace the actual source module (see `_determine_source_module` above). If tracing fails, defaulting to `"oobb_get_items_oobb"` is safe since the function is accessible from there.
- **Duplicate names**: Some functions may have the same name across sub-modules (unlikely but possible). The `overwrite=False` default prevents clobbering.
- **Large scope**: ~50 objects is a lot of files, but since they're auto-generated, the actual coding effort is small. The risk is in metadata quality (auto-stub descriptions aren't useful until enriched).
