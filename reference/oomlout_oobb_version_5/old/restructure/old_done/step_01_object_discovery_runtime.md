# Step 1 — Object Discovery Runtime

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** None (first step)  
> **Blocks:** Step 2, Step 3, Step 4, Step 5, Step 6, Step 7, Step 8

---

## Goal

Build the `discover_objects()` and `build_object_lookup()` functions that scan `part_calls/objects/*/working.py` and produce a typed lookup of all discovered object types. This is the Tier 1 (geometry builder) counterpart to the existing `discover_part_sets()` in `oobb_arch/catalog/part_set_discovery.py`.

The discovery runtime is the foundation of the entire object-per-folder architecture. Every subsequent step depends on it.

---

## Background — The Pattern

The roboclick sample architecture (`sample architecture/oomlout_roboclick.py`) defines:

```python
@dataclass(frozen=True)
class DiscoveredAction:
    name: str
    path: Path
    metadata: dict[str, Any]
    action_fn: Callable[..., Any]
    test_fn: Callable[..., Any]
    aliases: tuple[str, ...] = ()
```

And `discover_actions()` scans `actions/*/working.py`, validates each module has `define()` and `action()` callables, extracts metadata, and builds a name→DiscoveredAction dict.

The OOBB project already has this pattern for **part sets** in `oobb_arch/catalog/part_set_discovery.py` with `DiscoveredPartSet`. This step creates the parallel for **object types**.

### Key differences between sets and objects

| Aspect | Part Set (`sets/*/working.py`) | Object Type (`objects/*/working.py`) |
|--------|-------------------------------|--------------------------------------|
| Primary callable | `items(size, **kwargs) → list[dict]` | `action(**kwargs) → dict` (thing) |
| What it returns | List of part specification dicts | Single "thing" dict with `components` |
| Used by | `oobb_make_sets.make_all()` | `oobb_base.get_thing_from_dict()` |
| Folder name pattern | `<set_name>` (e.g. `circles`) | `oobb_object_<type>` (e.g. `oobb_object_circle`) |

---

## Deliverables

### 1. `oobb_arch/catalog/object_discovery.py`

New file containing:

```python
from __future__ import annotations

from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


@dataclass(frozen=True)
class DiscoveredObject:
    """A single discovered object type from part_calls/objects/*/working.py."""
    name: str                           # folder name, e.g. "oobb_object_circle"
    path: Path                          # absolute path to working.py
    metadata: dict[str, Any]            # result of define()
    action_fn: Callable[..., Any]       # the action(**kwargs) callable
    test_fn: Callable[..., Any] | None  # the test(**kwargs) callable (optional)
    aliases: tuple[str, ...] = ()       # from name_short in metadata


def resolve_objects_root(objects_root: str | Path | None = None) -> Path:
    """Return the root directory for object type folders.
    
    Default: <project>/part_calls/objects
    """


def discover_objects(objects_root: str | Path | None = None) -> dict[str, DiscoveredObject]:
    """Scan objects_root/*/working.py and return a dict of folder_name → DiscoveredObject.
    
    Validation rules:
    - Folder must contain working.py
    - Module must expose callable define()
    - Module must expose callable action()
    - test() is optional but recommended
    - If define() or action() missing → skip with warning (not error)
    - If test() missing → set test_fn to None
    """


def build_object_lookup(objects_root: str | Path | None = None) -> dict[str, DiscoveredObject]:
    """Discover all objects and build a lookup that includes alias entries.
    
    For each discovered object, if define() metadata contains 'name_short',
    those values are added as additional keys in the lookup (unless they conflict
    with an existing entry).
    
    Example:
        folder "oobb_object_circle" with name_short=["circle"]
        → lookup["oobb_object_circle"] = <DiscoveredObject>
        → lookup["circle"] = <DiscoveredObject>  (alias)
    """
```

**Implementation notes:**
- Mirror the structure of `part_set_discovery.py` closely (same `_load_module_from_file`, same `_extract_aliases`)
- The key difference: require `action()` instead of `items()` as the primary callable
- `test()` should be optional (print warning if missing, but still include in discovery)
- Use `spec_from_file_location` for module loading (avoids circular import issues)

### 2. Update `oobb_arch/catalog/__init__.py`

Add exports:
```python
from .object_discovery import (
    DiscoveredObject,
    discover_objects,
    build_object_lookup,
    resolve_objects_root,
)
```

### 3. `tests/test_object_discovery.py`

Four test cases:

#### `test_discover_objects_contract`
- Create a temp directory with a valid `working.py`:
  ```python
  d = {}
  def define():
      return {"name": "test_obj", "name_short": ["tobj"], "description": "Test", "category": "Test", "variables": []}
  def action(**kwargs):
      return {"type": "test", "parts": []}
  def test(**kwargs):
      return True
  ```
- Call `discover_objects(temp_dir)`
- Assert the folder name is in the returned dict
- Assert `metadata["name"]` matches folder name
- Assert `action_fn` is callable
- Assert `test_fn` is callable

#### `test_discover_objects_skips_invalid`
- Create a temp directory with a `working.py` that has `define()` but NO `action()`:
  ```python
  def define():
      return {"name": "bad"}
  ```
- Call `discover_objects(temp_dir)`
- Assert the returned dict is empty (folder was skipped)

#### `test_build_object_lookup_aliases`
- Create a temp directory with a valid `working.py` whose `define()` returns `name_short: ["alias1", "alias2"]`
- Call `build_object_lookup(temp_dir)`
- Assert `"alias1"` is in the lookup
- Assert `"alias2"` is in the lookup
- Assert both resolve to the same `DiscoveredObject`

#### `test_discover_objects_empty_dir`
- Create an empty temp directory
- Call `discover_objects(temp_dir)`
- Assert the returned dict is empty (no crash, no error)

---

## Files Modified

| File | Change |
|------|--------|
| `oobb_arch/catalog/object_discovery.py` | **NEW** — discovery runtime |
| `oobb_arch/catalog/__init__.py` | Add exports for new discovery functions |
| `tests/test_object_discovery.py` | **NEW** — 4 test cases |

---

## Test Contract

**All of the following must pass before proceeding to Step 2:**

```powershell
python -m unittest tests.test_object_discovery -v
python -m unittest tests.test_architecture_scaffold -v
python -m unittest tests.test_part_set_discovery -v
python -m unittest tests.test_make_sets_discovery_integration -v
python -m unittest tests.test_part_set_scaffold_generator -v
python -m unittest tests.test_part_set_migration_status -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests.test_dump_json_and_load_json_round_trip -v
```

**Gate command (run all at once):**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] `oobb_arch/catalog/object_discovery.py` exists and is importable
- [ ] `DiscoveredObject` dataclass has fields: name, path, metadata, action_fn, test_fn, aliases
- [ ] `resolve_objects_root()` defaults to `<project>/part_calls/objects`
- [ ] `discover_objects()` loads valid `working.py` files with `define()` + `action()`
- [ ] Invalid folders (missing `action()`) are **skipped with a warning**, not an exception
- [ ] `test()` is optional — discovery succeeds without it (test_fn is None)
- [ ] `build_object_lookup()` adds alias entries from `name_short`
- [ ] Empty directories return empty dict (no crash)
- [ ] All 4 new tests pass
- [ ] All pre-existing tests still pass (zero regressions)

---

## Estimated Scope

- ~120 lines of new code in `object_discovery.py` (closely mirrors `part_set_discovery.py`)
- ~80 lines of test code
- ~5 lines of `__init__.py` changes
- No behavior changes to any existing code
