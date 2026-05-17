# OOBB Object-Per-Folder Architecture Plan

## 1. Vision

Every OOBB entity — every **object type** (the geometry builders like `circle`, `gear`, `plate`, `bearing_plate`, …) and every **part set** (the catalog lists like `get_circles()`, `get_gears()`, …) — lives in its own folder with a `working.py` file, exactly like the roboclick sample architecture where each action is `actions/<name>/working.py`.

Critically, **documentation generation is a first-class citizen**: every `working.py` carries rich metadata via `define()`, and the system auto-generates JSON, HTML, and Markdown documentation from that metadata — just like roboclick's `export_actions_documentation_json/html`.

## 2. Two-Tier Folder Model

The project manages two distinct kinds of entities that both get the folder treatment:

### Tier 1 — Object Types (geometry builders)

These are the functions today scattered across `oobb_get_items_oobb.py`, `oobb_get_items_other.py`, `oobb_get_items_test.py`, and their sub-files. Each one takes a part dict and returns a "thing" (3D object description).

```
part_calls/
  objects/
    oobb_object_circle/
      working.py          # define() + action(**kwargs) + test()
    oobb_object_gear/
      working.py
    oobb_object_plate/
      working.py
    oobb_object_bearing_plate/
      working.py
    oobb_object_bolt/
      working.py
    oobb_object_nut/
      working.py
    oobb_object_tray/
      working.py
    oobb_object_wheel/
      working.py
    oobb_object_wire_basic/
      working.py
    oobb_object_test_gear/
      working.py
    ...
```

**Contract for each `working.py`:**

```python
d = {}

def define():
    """Return metadata dict describing this object type."""
    global d
    if not d:
        d = {
            "name": "oobb_object_circle",            # must match folder name
            "name_short": ["circle"],                 # aliases for dispatch
            "name_long": "OOBB Object: Circle",       # human-readable
            "description": "Generates circular OOBB plates with optional doughnut, shaft, and bearing features.",
            "category": "OOBB Geometry",
            "variables": [
                {"name": "diameter", "description": "Circle diameter in grid units.", "type": "number", "default": 3},
                {"name": "thickness", "description": "Plate thickness in mm.", "type": "number", "default": 3},
                {"name": "size", "description": "Grid system (oobb or oobe).", "type": "string", "default": "oobb"},
                {"name": "shaft", "description": "Optional shaft type.", "type": "string", "default": ""},
                {"name": "extra", "description": "Extra feature (e.g. doughnut_5).", "type": "string", "default": ""},
            ],
            "returns": "Thing dict with parts list for OpenSCAD generation.",
            "source_module": "oobb_get_items_oobb",   # provenance tracking
        }
    return dict(d)

def action(**kwargs):
    """Build and return the thing dict — the actual geometry builder."""
    # Initially delegates to legacy code; eventually contains the logic directly
    import oobb_get_items_oobb
    return oobb_get_items_oobb.get_circle(**kwargs)

def test(**kwargs):
    """Smoke test: call action with minimal args, verify return structure."""
    result = action(diameter=3, thickness=3, size="oobb")
    return isinstance(result, dict) and "parts" in result
```

### Tier 2 — Part Sets (catalog lists)

These are the functions today in `oobb_make_sets.py` like `get_circles()`, `get_gears()`, etc. Each returns a list of part dicts.

```
part_calls/
  sets/
    bearing_circles/
      working.py          # define() + items() + test()
    bearing_plates/
      working.py
    circles/
      working.py
    gears/
      working.py
    plates/
      working.py
    trays/
      working.py
    ...
```

**Contract (already established from previous migration):**

```python
def define():
    """Return metadata dict describing this part set."""
    return {
        "name": "circles",
        "name_short": ["cs"],
        "name_long": "OOBB Part Set: Circles",
        "description": "All circular plate variants including doughnuts and shaft options.",
        "category": "Part Sets",
        "variables": [
            {"name": "size", "description": "Grid system.", "type": "string", "default": "oobb"},
        ],
    }

def items(size="oobb", **kwargs):
    """Return list of part dicts for this set."""
    circles = []
    # ... build the list ...
    return circles

def test(**kwargs):
    result = items(**kwargs)
    return isinstance(result, list) and len(result) >= 1
```

## 3. Discovery Runtime

Modeled directly on roboclick's `discover_actions()` pattern:

```python
@dataclass(frozen=True)
class DiscoveredObject:
    name: str           # folder name
    path: Path          # path to working.py
    metadata: dict      # result of define()
    action_fn: Callable # the action() or items() callable
    test_fn: Callable   # the test() callable
    aliases: tuple[str, ...]  # from name_short in metadata

def discover_objects(objects_root: Path) -> dict[str, DiscoveredObject]:
    """Scan objects_root/*/working.py, validate define()+action()+test(), return lookup."""

def discover_part_sets(sets_root: Path) -> dict[str, DiscoveredPartSet]:
    """Scan sets_root/*/working.py, validate define()+items()+test(), return lookup."""

def build_object_lookup(objects_root=None) -> dict[str, DiscoveredObject]:
    """Discover + add alias entries."""

def build_part_set_lookup(sets_root=None) -> dict[str, DiscoveredPartSet]:
    """Discover + add alias entries."""
```

### Dispatch integration

In `oobb_base.get_thing_from_dict()`:

```python
def get_thing_from_dict(thing_dict):
    # 1. Try discovered objects first
    obj = object_lookup.get(thing_dict["type"])
    if obj is not None:
        return obj.action_fn(**thing_dict)

    # 2. Legacy fallback (oobb → other → test modules)
    ...
```

In `oobb_make_sets.make_all()`:

```python
def make_all(filter=""):
    # 1. Try discovered part sets first
    for set_name in typs:
        discovered = set_lookup.get(set_name)
        if discovered:
            all_things.extend(discovered.items_fn(size="oobb"))
        else:
            # 2. Legacy fallback
            func = globals()["get_" + set_name]
            all_things.extend(func())
```

## 4. Documentation Generation (First-Class)

This is the most important addition. Following roboclick's pattern:

### 4a. Structured documentation data

```python
def get_all_objects_documentation(objects_root=None) -> list[dict]:
    """Collect define() metadata from all discovered objects into structured list."""

def get_all_part_sets_documentation(sets_root=None) -> list[dict]:
    """Collect define() metadata from all discovered part sets into structured list."""
```

Each entry contains:
- `command` / `name`: folder name
- `name_long`: human-readable name
- `name_short_options`: aliases
- `description`: what it does
- `summary`: auto-generated one-liner
- `variables`: list of `{name, description, type, default}`
- `category`: grouping
- `returns`: what the function returns

### 4b. JSON export

```python
def export_documentation_json(output_file: str, objects_root=None, sets_root=None):
    """Write documentation_data.json with all objects + sets."""
    payload = {
        "objects": get_all_objects_documentation(objects_root),
        "part_sets": get_all_part_sets_documentation(sets_root),
        "generated_date": str(date.today()),
        "total_objects": ...,
        "total_part_sets": ...,
    }
    json.dump(payload, ...)
```

### 4c. HTML export

Using a template (like roboclick's `documentation_template.html`):
- Searchable, filterable page showing all objects and part sets
- Grouped by category
- Variables table for each entry
- Pastel-colored cards with descriptions

### 4d. Markdown export (README generation)

Auto-generate:
- `part_calls/objects/README.md` — index of all object types with links
- `part_calls/sets/README.md` — index of all part sets with links
- Each folder gets its own `README.md` auto-generated from `define()` metadata
- The project-level `parts/README.md` continues to be generated from `details.json` (existing `oobb_markdown.py`)

### 4e. CLI for documentation

```
python -m oobb_documentation --json documentation_data.json
python -m oobb_documentation --html-template templates/doc_template.html --html-output documentation.html
python -m oobb_documentation --markdown
```

## 5. Test Framework

### Per-folder tests

Every `working.py` has a `test()` callable. Additionally, each folder may contain:
- `oomlout_test.py` — extended tests (like roboclick's pattern)
- Test results written to `test_result/` within the folder or centrally

### Global test runner

A `run_tests.py` (like roboclick's) that:
1. Discovers all `working.py` files in both `objects/` and `sets/`
2. Runs each `test()` function
3. Produces a markdown report and JSON results
4. Returns exit code 0 only if all pass

### Integration with existing tests

- `tests/test_file_generation.py` — snapshot/capability tests (unchanged)
- `tests/test_architecture_scaffold.py` — architecture layer tests (unchanged)
- `tests/test_part_set_discovery.py` — discovery contract tests (evolve)
- `tests/test_object_discovery.py` — NEW: object discovery contract tests
- `tests/test_documentation_generation.py` — NEW: documentation output tests

### Test contract between steps

**No step is considered complete until:**
1. All new tests for that step pass
2. All pre-existing tests still pass
3. `python -m unittest discover -s tests -p "test_*.py"` returns 0

## 6. Scaffold Generator

Enhanced from the current `generate_set_scaffold.py`:

```
python part_calls/generate_scaffold.py --tier object --name circle
python part_calls/generate_scaffold.py --tier set --name circles
```

Generates:
- Folder with `working.py` containing correct `define()`/`action()`/`test()` template
- Pre-filled metadata from existing code analysis where possible
- `README.md` placeholder

## 7. Migration Status Reporter

Enhanced from the current `report_migration_status.py`:

```
python part_calls/report_migration_status.py
```

Output:
```
=== Object Types ===
Discovered: 5 / 60  (8.3%)
  ✓ oobb_object_circle
  ✓ oobb_object_gear
  ...
  ✗ oobb_object_plate (legacy only)
  ✗ oobb_object_bolt (legacy only)

=== Part Sets ===
Discovered: 3 / 25  (12.0%)
  ✓ bearing_circles
  ✓ jigs
  ✓ others
  ✗ circles (legacy only)
  ...
```

## 8. Compatibility Strategy

### During migration (incremental)
- Both legacy modules and discovered folders coexist
- Discovery takes precedence; legacy is fallback
- `make_all()` and `get_thing_from_dict()` both use discovery-first pattern
- No existing entrypoint signatures change

### After migration (complete)
- Legacy `oobb_get_items_*.py` files can be archived
- Legacy `oobb_make_sets.py` `get_*` functions can be thin wrappers
- All dispatch goes through discovery
- Documentation is auto-generated from the living code

## 9. Naming Convention

Following roboclick's verbose naming:

| Entity | Folder Name Pattern | Example |
|--------|-------------------|---------|
| Object type | `oobb_object_<type>` | `oobb_object_circle` |
| Object type (other/hardware) | `oobb_object_<type>` | `oobb_object_bolt` |
| Object type (test) | `oobb_object_test_<name>` | `oobb_object_test_gear` |
| Part set | `<set_name>` | `circles`, `bearing_plates` |

The `name_short` in `define()` provides aliases for backward-compatible dispatch:
- `oobb_object_circle` → aliases: `["circle"]`
- `oobb_object_bolt` → aliases: `["bolt"]`

## 10. File Layout Summary

```
part_calls/
  objects/                           # Tier 1: geometry builders
    oobb_object_circle/
      working.py
      README.md                      # auto-generated
    oobb_object_gear/
      working.py
      README.md
    ...
    README.md                        # auto-generated index
  sets/                              # Tier 2: catalog lists
    bearing_circles/
      working.py
      README.md
    circles/
      working.py
      README.md
    ...
    README.md                        # auto-generated index
  generate_scaffold.py               # scaffold generator (both tiers)
  report_migration_status.py         # status reporter (both tiers)
  documentation.py                   # documentation generator
  run_tests.py                       # per-folder test runner
  documentation_data.json            # generated
  documentation.html                 # generated
templates/
  oobb_documentation_template.html   # HTML doc template
```
