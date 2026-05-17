# Step 2 — First Object Working.py Files (3 objects)

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 1 (Object Discovery Runtime) must be complete and all tests passing  
> **Blocks:** Step 3

---

## Goal

Create the first three `part_calls/objects/*/working.py` files — one from **each legacy source module** — to prove the full contract works across all three dispatch pathways:

1. `oobb_get_items_oobb.py` → `oobb_object_circle`
2. `oobb_get_items_other.py` → `oobb_object_bolt`
3. `oobb_get_items_test.py` → `oobb_object_test_gear`

Each file must have rich `define()` metadata, a working `action()` that delegates to the legacy function, and a `test()` smoke check.

---

## Background — The Three Source Modules

OOBB currently dispatches object types via `oobb_base.get_thing_from_dict()` through a priority chain:

```python
try:
    func = getattr(oobb_get_items_oobb, "get_" + thing_dict["type"])
except:
    try:
        func = getattr(oobb_get_items_other, "get_" + thing_dict["type"])
    except:
        func = getattr(oobb_get_items_test, "get_" + thing_dict["type"])
```

Each source module has different conventions:

| Module | Example Function | Signature | Returns |
|--------|-----------------|-----------|---------|
| `oobb_get_items_oobb` | `get_circle(**kwargs)` | Keyword args: diameter, thickness, size, extra, shaft | Thing dict with `components` list |
| `oobb_get_items_other` | `get_bolt(**kwargs)` | Keyword args: radius_name, depth | Thing dict with `components` list |
| `oobb_get_items_test` | `get_test_gear(**kwargs)` | Keyword args: style, pos, full_object | Thing dict with test geometry |

By creating one working.py from each module, we validate that:
- The discovery runtime (Step 1) works with real objects
- The `define()` → `action()` → `test()` contract is practical
- Legacy delegation pattern works for all three module types

---

## Deliverables

### 1. `part_calls/objects/oobb_object_circle/working.py`

```python
d = {}


def define():
    """Return metadata describing the circle object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_circle",
            "name_short": ["circle"],
            "name_long": "OOBB Object: Circle",
            "description": "Generates circular OOBB plates with optional doughnut, shaft, and bearing features.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "diameter", "description": "Circle diameter in grid units.", "type": "number", "default": 3},
                {"name": "thickness", "description": "Plate thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb or oobe).", "type": "string", "default": "oobb"},
                {"name": "shaft", "description": "Optional shaft type (e.g. coupler_flanged, m3).", "type": "string", "default": ""},
                {"name": "extra", "description": "Extra feature (e.g. doughnut_5).", "type": "string", "default": ""},
                {"name": "both_holes", "description": "Whether to include both oobb and oobe hole patterns.", "type": "boolean", "default": True},
            ],
            "returns": "Thing dict with components list for OpenSCAD generation.",
            "source_module": "oobb_get_items_oobb",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the circle thing dict."""
    import oobb_get_items_oobb
    return oobb_get_items_oobb.get_circle(**kwargs)


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(diameter=3, thickness=3, size="oobb", type="circle")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
```

### 2. `part_calls/objects/oobb_object_bolt/working.py`

```python
d = {}


def define():
    """Return metadata describing the bolt object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_bolt",
            "name_short": ["bolt"],
            "name_long": "OOBB Object: Bolt",
            "description": "Generates a bolt (hex-head fastener) with specified radius and depth.",
            "category": "Hardware",
            "variables": [
                {"name": "radius_name", "description": "Bolt size designation (e.g. m5, m6).", "type": "string", "default": "m6"},
                {"name": "depth", "description": "Bolt length in mm.", "type": "number", "default": 20},
            ],
            "returns": "Thing dict with components list for OpenSCAD generation.",
            "source_module": "oobb_get_items_other",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the bolt thing dict."""
    import oobb_get_items_other
    return oobb_get_items_other.get_bolt(**kwargs)


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(radius_name="m6", depth=20, type="bolt", size="hardware")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
```

### 3. `part_calls/objects/oobb_object_test_gear/working.py`

```python
d = {}


def define():
    """Return metadata describing the test_gear object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_test_gear",
            "name_short": ["test_gear"],
            "name_long": "OOBB Object: Test Gear",
            "description": "Generates a parametric gear test plate exploring pressure_angle, clearance, and backlash variations.",
            "category": "OOBB Test",
            "variables": [
                {"name": "style", "description": "Gear style variant.", "type": "string", "default": "socket_cap"},
                {"name": "pos", "description": "Position offset [x, y, z].", "type": "array", "default": [0, 0, 0]},
                {"name": "full_object", "description": "Whether to return full thing dict or just components.", "type": "boolean", "default": True},
            ],
            "returns": "Thing dict with test gear components for OpenSCAD generation.",
            "source_module": "oobb_get_items_test",
        }
    return dict(d)


def action(**kwargs):
    """Build and return the test_gear thing dict."""
    import oobb_get_items_test
    return oobb_get_items_test.get_test_gear(**kwargs)


def test(**kwargs):
    """Smoke test: verify action() returns a well-formed thing dict."""
    try:
        result = action(type="test", size="oobb", extra="gear")
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
```

### 4. `tests/test_object_working_files.py`

Seven test cases:

#### Metadata tests (3)
- **`test_circle_define_metadata`**: Import and call `define()` on the circle working.py. Assert returned dict contains all required keys: `name`, `name_short`, `name_long`, `description`, `category`, `variables`. Assert `variables` is a list of dicts each with `name`, `description`, `type`, `default`.
- **`test_bolt_define_metadata`**: Same for bolt. Assert `category` is `"Hardware"`.
- **`test_test_gear_define_metadata`**: Same for test_gear. Assert `category` is `"OOBB Test"`.

#### Discovery tests (3)
- **`test_circle_discovered`**: Call `discover_objects()` with real `part_calls/objects` root. Assert `"oobb_object_circle"` is in the returned dict.
- **`test_bolt_discovered`**: Assert `"oobb_object_bolt"` is in the returned dict.
- **`test_test_gear_discovered`**: Assert `"oobb_object_test_gear"` is in the returned dict.

#### Alias test (1)
- **`test_circle_alias_dispatch`**: Call `build_object_lookup()`. Assert `"circle"` is a key in the lookup. Assert `lookup["circle"].name == "oobb_object_circle"`.

**Note on test isolation**: These tests must load the working.py modules using `spec_from_file_location` (like the existing `test_part_set_discovery.py`) to avoid circular import issues from `oobb_base` → `oobb_get_items_*` → `oobb` → `oobb_variables` chains.

---

## Files Created

| File | Purpose |
|------|---------|
| `part_calls/objects/oobb_object_circle/working.py` | Circle geometry builder wrapper |
| `part_calls/objects/oobb_object_bolt/working.py` | Bolt geometry builder wrapper |
| `part_calls/objects/oobb_object_test_gear/working.py` | Test gear geometry builder wrapper |
| `tests/test_object_working_files.py` | 7 test cases for the 3 working.py files |

---

## Test Contract

**All of the following must pass before proceeding to Step 3:**

```powershell
# New tests
python -m unittest tests.test_object_working_files -v

# Step 1 tests (must still pass)
python -m unittest tests.test_object_discovery -v

# Pre-existing tests (must still pass)
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery -v
python -m unittest tests.test_make_sets_discovery_integration -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] `part_calls/objects/oobb_object_circle/working.py` exists with `define()`, `action()`, `test()`
- [ ] `part_calls/objects/oobb_object_bolt/working.py` exists with `define()`, `action()`, `test()`
- [ ] `part_calls/objects/oobb_object_test_gear/working.py` exists with `define()`, `action()`, `test()`
- [ ] Each `define()` returns rich metadata with structured `variables` list
- [ ] Each `action()` delegates to the correct legacy `get_*()` function
- [ ] Each `test()` returns `True` when called
- [ ] `discover_objects()` finds all three folders
- [ ] `build_object_lookup()` maps alias `"circle"` → `oobb_object_circle`
- [ ] All 7 new tests pass
- [ ] All pre-existing tests still pass

---

## Estimated Scope

- ~40 lines per working.py × 3 = ~120 lines of object code
- ~100 lines of test code
- No changes to any existing files
