# Step 9 — Bulk Part Set Migration (22 remaining sets)

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 8 (Bulk Other + Test Object Migration) must be complete and all tests passing  
> **Blocks:** Step 10

---

## Goal

Migrate all remaining `get_*()` part set functions from `oobb_make_sets.py` to per-folder `part_calls/sets/<name>/working.py` files. After this step, every part set has its own folder.

---

## Background — Part Set Inventory

`oobb_make_sets.py` contains ~25 `get_*()` functions. Three are already migrated from the earlier working.py migration:

### Already Migrated (3)

| Set | Folder | Status |
|-----|--------|--------|
| `bearing_circles` | `part_calls/sets/bearing_circles/working.py` | ✅ Complete |
| `jigs` | `part_calls/sets/jigs/working.py` | ✅ Complete |
| `others` | `part_calls/sets/others/working.py` | ✅ Complete |

### Remaining to Migrate (22)

| # | Function in `oobb_make_sets.py` | Folder Name |
|---|--------------------------------|-------------|
| 1 | `get_bearing_plates()` | `bearing_plates` |
| 2 | `get_buntings()` | `buntings` |
| 3 | `get_circles()` | `circles` |
| 4 | `get_gears()` | `gears` |
| 5 | `get_holders()` | `holders` |
| 6 | `get_jacks()` | `jacks` |
| 7 | `get_mounting_plates()` | `mounting_plates` |
| 8 | `get_plates()` | `plates` |
| 9 | `get_pulleys()` | `pulleys` |
| 10 | `get_shaft_couplers()` | `shaft_couplers` |
| 11 | `get_shafts()` | `shafts` |
| 12 | `get_soldering_jigs()` | `soldering_jigs` |
| 13 | `get_smd_magazines()` | `smd_magazines` |
| 14 | `get_tool_holders()` | `tool_holders` |
| 15 | `get_trays()` | `trays` |
| 16 | `get_ziptie_holders()` | `ziptie_holders` |
| 17 | `get_nuts()` | `nuts` |
| 18 | `get_wires()` | `wires` |
| 19 | `get_wheels()` | `wheels` |
| 20 | `get_screws()` | `screws` |
| 21 | `get_bearings()` | `bearings` |
| 22 | `get_tests()` | `tests_set` |

### Existing Scaffold Generator for Sets

The existing `oobb_arch/catalog/part_set_scaffold_generator.py` already generates `part_calls/sets/<name>/working.py` files with the correct contract:

```python
def define():
    return {"name": "<set_name>", "name_short": [...], ...}

def items(size="oobb", **kwargs):
    # delegates to legacy getter
    return oobb_make_sets.get_<set_name>(**kwargs)

def test(**kwargs):
    result = items()
    return isinstance(result, list) and len(result) > 0
```

---

## Execution Strategy

### Phase A: Auto-scaffold all remaining sets

For each unmatched `get_*()` function in `oobb_make_sets.py`:

```python
# Pseudo-code for the migration script
from oobb_arch.catalog.part_set_scaffold_generator import generate_set_scaffold

ALREADY_MIGRATED = {"bearing_circles", "jigs", "others"}

# List all get_* functions in oobb_make_sets
import oobb_make_sets
for name in dir(oobb_make_sets):
    if name.startswith("get_") and callable(getattr(oobb_make_sets, name)):
        set_name = name[4:]  # strip "get_"
        if set_name not in ALREADY_MIGRATED and set_name != "set_items_discovered":
            generate_set_scaffold(set_name, overwrite=False)
```

**Special case — `get_tests()`**: The set name would be `tests` but that conflicts with the `tests/` directory. Use `tests_set` as the folder name.

### Phase B: Verify define() metadata quality

Each generated `define()` should have:
- `name`: set name
- `name_short`: list of aliases (from the set name split)
- `name_long`: human-readable title (e.g. "OOBB Part Set: Bearing Plates")
- `description`: what this set contains
- `category`: derived from set contents (OOBB Geometry, Hardware, Test)
- `variables`: the `size` parameter and any other set-specific params

For the most important sets (circles, plates, gears, holders), manually enhance descriptions:
- **circles**: "All circular OOBB plate variants across standard sizes."
- **plates**: "Rectangular OOBB plates in all size combinations."
- **gears**: "Parametric gear plates with various tooth counts and configurations."
- **holders**: "Electronic component holders, motor mounts, and cable management."

### Phase C: Wire into discovery

The existing `oobb_make_sets.make_all()` is already wired through `discover_part_sets()` with legacy fallback. Adding more `working.py` files will automatically include them in the discovery.

Verify:
```python
from oobb_arch.catalog.part_set_discovery import discover_part_sets
sets = discover_part_sets()
assert len(sets) >= 25  # All sets discovered
```

---

## Part Set Working.py Contract Reminder

Each `working.py` must follow the set contract:

```python
d = {}

def define():
    """Return metadata describing this part set."""
    global d
    if not d:
        d = {
            "name": "circles",
            "name_short": ["circles"],
            "name_long": "OOBB Part Set: Circles",
            "description": "All circular OOBB plate variants across standard sizes.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "size", "description": "Grid system.", "type": "string", "default": "oobb"},
            ],
        }
    return dict(d)


def items(size="oobb", **kwargs):
    """Return the list of part specification dicts for this set.
    
    Each item is a dict like:
    {"type": "circle", "size": "oobb", "diameter": 3, "thickness": 3, ...}
    """
    import oobb_make_sets
    return oobb_make_sets.get_circles(size=size, **kwargs)


def test(**kwargs):
    """Verify items() returns a non-empty list of dicts."""
    try:
        result = items()
        return isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict)
    except Exception:
        return False
```

---

## Files Created

| File | Purpose |
|------|---------|
| `part_calls/sets/bearing_plates/working.py` | Bearing plate set |
| `part_calls/sets/buntings/working.py` | Bunting alphabet set |
| `part_calls/sets/circles/working.py` | Circle plates set |
| `part_calls/sets/gears/working.py` | Gear plates set |
| `part_calls/sets/holders/working.py` | Holder devices set |
| `part_calls/sets/jacks/working.py` | Jack/bracket set |
| `part_calls/sets/mounting_plates/working.py` | Mounting plates set |
| `part_calls/sets/plates/working.py` | Rectangular plates set |
| `part_calls/sets/pulleys/working.py` | Pulley set |
| `part_calls/sets/shaft_couplers/working.py` | Shaft coupler set |
| `part_calls/sets/shafts/working.py` | Shaft set |
| `part_calls/sets/soldering_jigs/working.py` | Soldering jig set |
| `part_calls/sets/smd_magazines/working.py` | SMD magazine set |
| `part_calls/sets/tool_holders/working.py` | Tool holder set |
| `part_calls/sets/trays/working.py` | Tray set |
| `part_calls/sets/ziptie_holders/working.py` | Ziptie holder set |
| `part_calls/sets/nuts/working.py` | Nuts hardware set |
| `part_calls/sets/wires/working.py` | Wire set |
| `part_calls/sets/wheels/working.py` | Wheel set |
| `part_calls/sets/screws/working.py` | Screw hardware set |
| `part_calls/sets/bearings/working.py` | Bearing hardware set |
| `part_calls/sets/tests_set/working.py` | Test shapes set |

**22 new folders**

---

## Tests

### `tests/test_part_set_bulk_migration.py`

Five test cases:

#### `test_all_make_sets_functions_have_folders`
- Parse `oobb_make_sets.py` for all `get_*()` function names (excluding helpers like `get_set_items_discovered`)
- For each, assert corresponding `part_calls/sets/<name>/working.py` exists

#### `test_all_sets_discovered`
- Call `discover_part_sets()` on real `part_calls/sets` root
- Assert count ≥ 25 (all sets including the 3 previously migrated)

#### `test_zero_pending_sets`
- Call `get_migration_status()`
- Assert `sets["pending"]` is empty
- Assert `sets["percentage"] == 100.0`

#### `test_key_sets_have_rich_metadata`
- Load working.py for `circles`, `plates`, `gears`, `holders`
- Assert `define()` returns metadata with non-stub `description`
- Assert `name_long` is set

#### `test_make_all_still_works`
- This is the critical regression test
- Call `oobb_make_sets.make_all(sizes=["oobb"])` (or mock the build step)
- Assert it completes without error
- Assert it returns a non-empty list

---

## Test Contract

**All of the following must pass before proceeding to Step 10:**

```powershell
# New tests
python -m unittest tests.test_part_set_bulk_migration -v

# Step 8 tests
python -m unittest tests.test_other_test_object_migration -v

# Step 7 tests
python -m unittest tests.test_oobb_core_object_migration -v

# Documentation tests (must now reflect all sets too)
python -m unittest tests.test_documentation_generation -v

# Pre-existing tests (CRITICAL)
python -m unittest tests.test_make_sets_discovery_integration -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests.test_dump_json_and_load_json_round_trip -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] Every `get_*()` function in `oobb_make_sets.py` has a corresponding `part_calls/sets/<name>/working.py`
- [ ] `get_migration_status()` reports 100% set migration
- [ ] `sets["pending"]` is empty
- [ ] `discover_part_sets()` discovers all ≥25 sets
- [ ] Key sets (circles, plates, gears, holders) have enriched descriptions
- [ ] `oobb_make_sets.make_all()` still works correctly (discovery + legacy fallback)
- [ ] Previously migrated sets (bearing_circles, jigs, others) are NOT overwritten
- [ ] Documentation JSON export now includes all sets
- [ ] All 5 new tests pass
- [ ] All pre-existing tests still pass

---

## Estimated Scope

- ~22 generated working.py files × ~35 lines = ~770 lines (mostly auto-generated)
- Manual enrichment of 4–5 key sets = ~80 lines
- ~60 lines of test code
- No changes to any existing production code

---

## Risk Notes

- **`get_tests()` naming conflict**: The set is named `tests` but there's a `tests/` directory at root. Using `tests_set` as the folder name avoids the conflict. The alias `"tests"` in `name_short` ensures discovery can still find it.
- **`make_all()` compatibility**: The existing `make_all()` function iterates through `get_*()` functions and calls them. Since the new `working.py` files delegate back to the same functions, there's no behavior change. But `make_all()` should also be enhanced to discover sets from folders (this was already partially done in the earlier migration).
- **Set-specific parameters**: Some sets have extra parameters beyond `size` (e.g. `get_holders()` might accept filtering args). The scaffold generator should preserve **kwargs pass-through to handle this.
