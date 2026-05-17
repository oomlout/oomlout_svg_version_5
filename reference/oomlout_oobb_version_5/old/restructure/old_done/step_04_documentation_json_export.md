# Step 4 — Documentation Data Model & JSON Export

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 3 (Wire Object Discovery into oobb_base Dispatch) must be complete and all tests passing  
> **Blocks:** Step 5

---

## Goal

Build the documentation generation system that collects `define()` metadata from all discovered objects and part sets, and exports structured JSON. This is the foundation for all documentation outputs (JSON, HTML, Markdown) and mirrors roboclick's `get_all_actions_documentation()` and `export_actions_documentation_json()`.

**Documentation generation is the most important feature of this migration** — it turns the folder-per-object pattern from a code organization exercise into a self-documenting system.

---

## Background — The Roboclick Documentation Pattern

Roboclick's `oomlout_roboclick.py` defines:

```python
def get_all_actions_documentation(actions_root=None) -> list[dict]:
    docs = []
    discovered = discover_actions(actions_root=actions_root)
    for action_name in sorted(discovered.keys()):
        action_info = discovered[action_name]
        metadata = action_info.metadata
        # Extract and normalize:
        #   command, name_long, name_short_options, description, summary,
        #   variables (list of {name, description, type, default}),
        #   variable_names, category, returns, aliases
        docs.append({...})
    return docs

def export_actions_documentation_json(output_file, actions_root=None):
    docs = get_all_actions_documentation(actions_root=actions_root)
    payload = {
        "actions": docs,
        "generated_date": str(date.today()),
        "total_actions": len(docs),
    }
    json.dump(payload, ...)
```

The output `documentation_data.json` contains ~2400 lines of structured metadata that drives the searchable HTML documentation page.

### OOBB adaptation

OOBB has two entity types instead of one, so the JSON structure will be:

```json
{
  "objects": [...],
  "part_sets": [...],
  "generated_date": "2026-03-27",
  "total_objects": 3,
  "total_part_sets": 3
}
```

---

## Deliverables

### 1. `part_calls/documentation.py`

New file containing:

#### Core documentation collection functions

```python
def get_all_objects_documentation(objects_root=None) -> list[dict]:
    """Collect define() metadata from all discovered objects.
    
    Returns a sorted list of dicts, each with:
    - command: folder name (e.g. "oobb_object_circle")
    - name_long: human-readable name
    - name_short_options: list of aliases
    - description: what it does
    - summary: auto-generated one-liner (from description or variable names)
    - variables: list of {name, description, type, default}
    - variable_names: list of just the variable name strings
    - category: grouping string
    - returns: what the function returns
    - aliases: same as name_short_options
    """

def get_all_part_sets_documentation(sets_root=None) -> list[dict]:
    """Collect define() metadata from all discovered part sets.
    
    Same structure as objects documentation.
    """
```

#### JSON export function

```python
def export_documentation_json(output_file, objects_root=None, sets_root=None):
    """Write documentation_data.json with all objects + sets.
    
    Output structure:
    {
        "objects": [...],
        "part_sets": [...],
        "generated_date": "YYYY-MM-DD",
        "total_objects": N,
        "total_part_sets": M
    }
    """
```

#### Helper functions (modeled on roboclick)

```python
def _coerce_text(value) -> str:
    """Normalize a value to a cleaned string."""

def _extract_variable_names(raw_variables) -> list[str]:
    """Extract just the name strings from a variables list."""

def _build_summary(description, variable_names, returns_text) -> str:
    """Auto-generate a one-line summary from available metadata.
    
    Priority:
    1. First sentence of description
    2. "Inputs: var1, var2, ..." from variable names
    3. "Returns: ..." from returns text
    4. "No summary available."
    """

def _normalize_variables(raw_variables) -> list[dict]:
    """Ensure each variable entry is a dict with name, description, type, default.
    
    Handles both dict-style and string-style variable definitions:
    - {"name": "diameter", "description": "...", "type": "number", "default": 3}
    - "diameter" → {"name": "diameter", "description": "", "type": "", "default": ""}
    """
```

### 2. `tests/test_documentation_generation.py`

Five test cases:

#### `test_get_all_objects_documentation_returns_list`
- Call `get_all_objects_documentation()` (using real `part_calls/objects` root with the 3 objects from Step 2)
- Assert return value is a list
- Assert length ≥ 3 (at least the three objects created in Step 2)
- Assert each entry is a dict

#### `test_object_doc_entry_has_required_keys`
- Get documentation list
- For each entry, assert it contains: `command`, `name_long`, `description`, `variables`, `category`, `summary`
- Assert `command` is a non-empty string
- Assert `variables` is a list

#### `test_get_all_part_sets_documentation_returns_list`
- Call `get_all_part_sets_documentation()` (using real `part_calls/sets` root with 3 sets from previous migration)
- Assert return value is a list with ≥ 3 entries

#### `test_export_json_creates_file`
- Call `export_documentation_json(temp_file)`
- Assert the file was created
- Load and parse as JSON
- Assert top-level keys: `objects`, `part_sets`, `generated_date`, `total_objects`, `total_part_sets`
- Assert `total_objects` ≥ 3
- Assert `total_part_sets` ≥ 3

#### `test_documentation_variable_structure`
- Get documentation list for objects
- Find an entry that has variables (e.g. circle)
- Assert each variable dict has keys: `name`, `description`, `type`, `default`
- Assert `name` is a non-empty string

---

## Documentation Entry Schema

Each entry in the `objects` or `part_sets` array follows this schema:

```json
{
  "command": "oobb_object_circle",
  "name_long": "OOBB Object: Circle",
  "name_short_options": ["circle"],
  "description": "Generates circular OOBB plates with optional doughnut, shaft, and bearing features.",
  "summary": "Generates circular OOBB plates with optional doughnut, shaft, and bearing features.",
  "variables": [
    {
      "name": "diameter",
      "description": "Circle diameter in grid units.",
      "type": "number",
      "default": 3
    },
    {
      "name": "thickness",
      "description": "Plate thickness in mm.",
      "type": "number",
      "default": 3
    }
  ],
  "variable_names": ["diameter", "thickness", "size", "shaft", "extra", "both_holes"],
  "category": "OOBB Geometry",
  "returns": "Thing dict with components list for OpenSCAD generation.",
  "aliases": ["circle"]
}
```

---

## Files Created/Modified

| File | Change |
|------|--------|
| `part_calls/documentation.py` | **NEW** — documentation collection and JSON export |
| `tests/test_documentation_generation.py` | **NEW** — 5 test cases |

---

## Test Contract

**All of the following must pass before proceeding to Step 5:**

```powershell
# New tests
python -m unittest tests.test_documentation_generation -v

# Step 3 tests (must still pass)
python -m unittest tests.test_object_dispatch_integration -v

# Step 2 tests (must still pass)
python -m unittest tests.test_object_working_files -v

# Step 1 tests (must still pass)
python -m unittest tests.test_object_discovery -v

# Pre-existing tests
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] `part_calls/documentation.py` exists and is importable
- [ ] `get_all_objects_documentation()` returns a list of dicts with all required keys
- [ ] `get_all_part_sets_documentation()` returns a list of dicts with all required keys
- [ ] `export_documentation_json()` creates a valid JSON file with expected structure
- [ ] Variable metadata is structured: each has `name`, `description`, `type`, `default`
- [ ] Summary is auto-generated from description (first sentence) or variable names
- [ ] JSON output contains entries for all 3 discovered objects and 3 discovered sets
- [ ] All 5 new tests pass
- [ ] All pre-existing tests still pass

---

## Estimated Scope

- ~150 lines of code in `documentation.py`
- ~80 lines of test code
- No changes to any existing files
