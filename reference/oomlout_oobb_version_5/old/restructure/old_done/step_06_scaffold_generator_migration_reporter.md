# Step 6 — Enhanced Scaffold Generator & Migration Reporter

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 5 (Documentation HTML & Markdown Export) must be complete and all tests passing  
> **Blocks:** Step 7, Step 8, Step 9

---

## Goal

Build the tooling that makes bulk migration (Steps 7–9) fast and accurate:

1. **Scaffold Generator**: Given a legacy `get_*()` function, auto-generate the `part_calls/objects/<name>/working.py` file with `define()`, `action()`, and `test()` stubs
2. **Migration Status Reporter**: Scan all legacy `get_*()` functions and report which ones have been migrated to per-folder objects (and which part sets have been migrated to per-folder sets)

These tools will be used by the agent (or a human developer) during Steps 7–9 to systematically migrate every object and set.

---

## Background — What Currently Exists

### Existing scaffold generator (sets only)
`oobb_arch/catalog/part_set_scaffold_generator.py` generates `part_calls/sets/<name>/working.py` from a legacy set getter function. It already works for the 3 migrated sets (`bearing_circles`, `jigs`, `others`).

### Existing migration reporter (sets only)
`oobb_arch/catalog/migration_status.py` scans `oobb_make_sets.py` for `get_*()` functions and cross-references with `discover_part_sets()` to report migrated vs. pending.

This step extends both tools to also handle **objects** (Tier 1).

---

## Deliverables

### 1. `oobb_arch/catalog/object_scaffold_generator.py`

New file that generates object working.py files:

```python
def generate_object_scaffold(
    type_name: str,
    source_module: str,
    legacy_function_name: str,
    output_dir: str | Path | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    """Generate a working.py file for an object type.
    
    Args:
        type_name: The object type name (e.g. "circle", "bolt")
        source_module: The legacy module name (e.g. "oobb_get_items_oobb")
        legacy_function_name: The full get_* function name (e.g. "get_circle")
        output_dir: Override output directory (default: part_calls/objects)
        overwrite: If True, overwrite existing working.py
    
    Returns:
        Path to the generated working.py file
    
    The generated file:
    - Folder: part_calls/objects/oobb_object_<type_name>/working.py
    - define() returns metadata dict with:
        - name: "oobb_object_<type_name>"
        - name_short: ["<type_name>"]
        - name_long: "OOBB Object: <Type Name>"
        - description: "Auto-generated scaffold for <type_name>. EDIT THIS."
        - category: auto-detected from source_module
        - variables: [] (to be filled in manually or by introspection)
        - source_module: "<source_module>"
    - action(**kwargs) delegates to source_module.legacy_function_name(**kwargs)
    - test(**kwargs) calls action() with minimal kwargs and checks for dict + "components"
    """
```

#### Auto-detection of metadata

The scaffold generator should try to extract useful information from the legacy function:

```python
def _introspect_legacy_function(module_name: str, func_name: str) -> dict:
    """Try to inspect the legacy function for parameter info.
    
    Attempts to:
    1. Load the module (with try/except for circular import issues)
    2. Get the function's signature via inspect.signature()
    3. Extract parameter names, defaults, and annotations
    4. Build a variables list from the parameters
    
    Falls back to empty variables list if introspection fails.
    """
```

#### Category mapping

```python
_SOURCE_MODULE_CATEGORY = {
    "oobb_get_items_oobb": "OOBB Geometry",
    "oobb_get_items_oobb_old": "OOBB Geometry (Legacy)",
    "oobb_get_items_oobb_wire": "OOBB Wire",
    "oobb_get_items_oobb_holder": "OOBB Holder",
    "oobb_get_items_oobb_other": "OOBB Other",
    "oobb_get_items_oobb_bearing_plate": "OOBB Bearing Plate",
    "oobb_get_items_other": "Hardware",
    "oobb_get_items_test": "OOBB Test",
}
```

### 2. `oobb_arch/catalog/migration_status.py` — enhance for objects

Extend the existing file (or replace) to report **both** tiers:

```python
def get_all_legacy_object_functions() -> list[dict]:
    """Scan all get_items_* modules and collect every get_*() function.
    
    Returns list of:
    {
        "type_name": "circle",
        "function_name": "get_circle",
        "source_module": "oobb_get_items_oobb",
        "full_name": "oobb_object_circle"
    }
    
    Modules to scan:
    - oobb_get_items_oobb (+ sub-modules via star import: 
        oobb_get_items_oobb_old, oobb_get_items_oobb_wire,
        oobb_get_items_oobb_holder, oobb_get_items_oobb_other,
        oobb_get_items_oobb_bearing_plate)
    - oobb_get_items_other
    - oobb_get_items_test
    """

def get_all_legacy_set_functions() -> list[dict]:
    """Scan oobb_make_sets.py for all get_*() functions.
    
    Returns list of:
    {
        "set_name": "circles",
        "function_name": "get_circles",
        "source_module": "oobb_make_sets"
    }
    """

def get_migration_status(objects_root=None, sets_root=None) -> dict:
    """Return comprehensive migration status.
    
    Returns:
    {
        "objects": {
            "total_legacy": N,
            "total_migrated": M,
            "migrated": ["circle", "bolt", "test_gear"],
            "pending": ["plate", "gear", "wheel", ...],
            "percentage": M/N * 100
        },
        "sets": {
            "total_legacy": X,
            "total_migrated": Y,
            "migrated": ["bearing_circles", "jigs", "others"],
            "pending": ["circles", "gears", ...],
            "percentage": Y/X * 100
        }
    }
    """

def print_migration_report(objects_root=None, sets_root=None):
    """Print a human-readable migration status report.
    
    Output format:
    ════════════════════════════════════════════
     OOBB Migration Status Report
    ════════════════════════════════════════════
    
    OBJECTS: 3 / 60 migrated (5.0%)
    ✓ circle (oobb_get_items_oobb.get_circle)
    ✓ bolt (oobb_get_items_other.get_bolt)
    ✓ test_gear (oobb_get_items_test.get_test_gear)
    ✗ plate (oobb_get_items_oobb.get_plate)
    ✗ gear (oobb_get_items_oobb.get_gear)
    ...
    
    SETS: 3 / 25 migrated (12.0%)
    ✓ bearing_circles
    ✓ jigs
    ✓ others
    ✗ circles
    ✗ gears
    ...
    """
```

### 3. `tests/test_object_scaffold_generator.py`

Four test cases:

#### `test_scaffold_generates_valid_working_py`
- Call `generate_object_scaffold("test_type", "oobb_get_items_test", "get_test_gear", output_dir=temp)`
- Assert `<temp>/oobb_object_test_type/working.py` was created
- Load the generated module (spec_from_file_location)
- Assert it has `define`, `action`, `test` callables
- Assert `define()` returns metadata with correct `name` and `source_module`

#### `test_scaffold_respects_overwrite_flag`
- Generate a scaffold
- Try to generate again with `overwrite=False` → assert it raises or returns existing path
- Generate again with `overwrite=True` → assert it succeeds

#### `test_scaffold_auto_detects_category`
- Generate scaffold with `source_module="oobb_get_items_oobb"`
- Assert `define()` metadata `category` is `"OOBB Geometry"`
- Generate scaffold with `source_module="oobb_get_items_other"`
- Assert category is `"Hardware"`

#### `test_scaffold_generates_discoverable_object`
- Generate scaffold in a temp objects root
- Call `discover_objects(temp_root)`
- Assert the generated object is discovered
- Assert the `action_fn` is callable

### 4. `tests/test_migration_status_enhanced.py`

Three test cases:

#### `test_get_all_legacy_object_functions`
- Call `get_all_legacy_object_functions()`
- Assert return is a non-empty list
- Assert each entry has `type_name`, `function_name`, `source_module`
- Known entries: assert `"circle"` is in the type_names, `"bolt"` is in the type_names

#### `test_migration_status_reports_migrated`
- Call `get_migration_status()`
- Assert `objects["migrated"]` contains `"circle"`, `"bolt"`, `"test_gear"`
- Assert `objects["pending"]` does NOT contain `"circle"`
- Assert `sets["migrated"]` contains `"bearing_circles"`, `"jigs"`, `"others"`

#### `test_migration_status_percentages`
- Call `get_migration_status()`
- Assert `objects["percentage"]` > 0
- Assert `sets["percentage"]` > 0
- Assert `objects["total_legacy"]` > `objects["total_migrated"]` (since most aren't migrated yet)

---

## Files Created/Modified

| File | Change |
|------|--------|
| `oobb_arch/catalog/object_scaffold_generator.py` | **NEW** — scaffold generation for object working.py |
| `oobb_arch/catalog/migration_status.py` | Enhanced with object scanning + comprehensive reporting |
| `tests/test_object_scaffold_generator.py` | **NEW** — 4 test cases |
| `tests/test_migration_status_enhanced.py` | **NEW** — 3 test cases |

---

## Test Contract

**All of the following must pass before proceeding to Step 7:**

```powershell
# New tests
python -m unittest tests.test_object_scaffold_generator -v
python -m unittest tests.test_migration_status_enhanced -v

# Step 4-5 tests
python -m unittest tests.test_documentation_generation -v

# Step 1-3 tests
python -m unittest tests.test_object_discovery tests.test_object_working_files tests.test_object_dispatch_integration -v

# Pre-existing tests
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery tests.test_make_sets_discovery_integration -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] `generate_object_scaffold()` produces a valid working.py that is discoverable
- [ ] Generated scaffolds delegate to the correct legacy function
- [ ] Category is auto-detected from source module name
- [ ] `overwrite=False` prevents clobbering existing files
- [ ] `get_all_legacy_object_functions()` finds functions from all legacy modules (including sub-modules like `oobb_get_items_oobb_old`)
- [ ] `get_migration_status()` reports correct counts and percentages
- [ ] `print_migration_report()` produces readable output
- [ ] All 7 new tests pass
- [ ] All pre-existing tests still pass

---

## Estimated Scope

- ~120 lines in `object_scaffold_generator.py`
- ~120 lines in `migration_status.py` (extended)
- ~80 lines in `test_object_scaffold_generator.py`
- ~60 lines in `test_migration_status_enhanced.py`
- No changes to any existing production code
