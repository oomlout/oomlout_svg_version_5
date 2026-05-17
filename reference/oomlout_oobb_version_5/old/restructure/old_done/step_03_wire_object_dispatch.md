# Step 3 — Wire Object Discovery into oobb_base Dispatch

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 2 (First Object Working.py Files) must be complete and all tests passing  
> **Blocks:** Step 7, Step 8

---

## Goal

Update `oobb_base.get_thing_from_dict()` to check the object discovery lookup **before** falling back to the legacy `getattr` chain across `oobb_get_items_oobb`, `oobb_get_items_other`, and `oobb_get_items_test`. This is the critical integration point that routes production dispatch through the new folder-based objects.

---

## Background — Current Dispatch

`oobb_base.get_thing_from_dict()` currently has two layers:

1. **Registry layer** (added in Phase 1 architecture scaffold): tries `_get_legacy_builder_registry().resolve(type)` — this is a static registry built from the three legacy modules
2. **Legacy getattr chain**: tries `oobb_get_items_oobb.get_<type>()` → `oobb_get_items_other.get_<type>()` → `oobb_get_items_test.get_<type>()`

This step adds a **third layer at the top** — the discovery lookup — making the priority:

```
1. Discovered objects (part_calls/objects/*/working.py)  ← NEW
2. Legacy builder registry
3. Legacy getattr chain (oobb → other → test)
```

### Safety requirements

- The import of `build_object_lookup` must be wrapped in `try/except` so that if `oobb_arch` is missing, the code degrades gracefully
- The lookup cache must be lazily initialized (same pattern as existing `_LEGACY_BUILDER_REGISTRY`)
- If a type is found in both discovery and legacy, **discovery wins** (this is the migration path — discovered objects take precedence)

---

## Deliverables

### 1. Modify `oobb_base.py`

**Add import (with safety guard):**
```python
try:
    from oobb_arch.catalog.object_discovery import build_object_lookup
except Exception:
    build_object_lookup = None
```

**Add cache + lazy initializer:**
```python
_OBJECT_LOOKUP = None

def _get_object_lookup():
    global _OBJECT_LOOKUP
    if _OBJECT_LOOKUP is None and build_object_lookup is not None:
        try:
            _OBJECT_LOOKUP = build_object_lookup()
        except Exception:
            _OBJECT_LOOKUP = {}
    return _OBJECT_LOOKUP or {}
```

**Update `get_thing_from_dict()` — add discovery check at the top:**
```python
def get_thing_from_dict(thing_dict):
    full_object = thing_dict.get("full_object", False)

    func = None

    # 1. Try discovered objects first (part_calls/objects/*/working.py)
    object_lookup = _get_object_lookup()
    discovered_obj = object_lookup.get(thing_dict["type"])
    if discovered_obj is not None:
        func = discovered_obj.action_fn

    # 2. Try legacy builder registry
    if func is None:
        registry = _get_legacy_builder_registry()
        if registry is not None:
            try:
                func = registry.resolve(thing_dict["type"])
            except KeyError:
                func = None

    # 3. Legacy getattr chain
    if func is None:
        try:
            func = getattr(oobb_get_items_oobb, "get_"+thing_dict["type"])
        except:
            try:
                func = getattr(oobb_get_items_other, "get_"+thing_dict["type"])
            except:
                func = getattr(oobb_get_items_test, "get_"+thing_dict["type"])

    thing = func(**thing_dict)
    return thing
```

### 2. `tests/test_object_dispatch_integration.py`

Three test cases:

#### `test_dispatch_prefers_discovered`
- Create a temp `working.py` that returns a unique sentinel value from `action()`
- Patch `_get_object_lookup()` to return a lookup containing this test object
- Call `get_thing_from_dict({"type": "<test_type>"})`
- Assert the sentinel value is returned (proving discovery took precedence)

#### `test_dispatch_falls_back_to_legacy`
- Ensure `_OBJECT_LOOKUP` is empty (or has no entry for the test type)
- Call `get_thing_from_dict()` with a type known to exist in legacy (e.g. `"plate"`)
- Assert it returns a valid thing dict (legacy chain still works)

#### `test_dispatch_circle_via_discovery`
- Use real `part_calls/objects/oobb_object_circle/working.py` (created in Step 2)
- Call `get_thing_from_dict({"type": "circle", "diameter": 3, "thickness": 3, "size": "oobb"})`
- Assert it returns a valid thing dict with `"components"` key
- This proves the real end-to-end path works

**Note on test approach**: Use `importlib.util.spec_from_file_location` to load `oobb_base.py` in isolation, or use `unittest.mock.patch` to control the discovery cache. The circular import pattern means standard `import oobb_base` may not work cleanly in test files.

### 3. Verify existing tests

Run the full `test_file_generation.py` suite to ensure no snapshot/capability regressions. Since discovered objects delegate to the same legacy functions, the output should be identical.

---

## Files Modified

| File | Change |
|------|--------|
| `oobb_base.py` | Add object discovery import, cache, and dispatch logic |
| `tests/test_object_dispatch_integration.py` | **NEW** — 3 integration tests |

---

## Test Contract

**All of the following must pass before proceeding to Step 4:**

```powershell
# New tests
python -m unittest tests.test_object_dispatch_integration -v

# Step 2 tests (must still pass)
python -m unittest tests.test_object_working_files -v

# Step 1 tests (must still pass)
python -m unittest tests.test_object_discovery -v

# Pre-existing tests (must still pass — critical for regression detection)
python -m unittest tests.test_architecture_scaffold -v
python -m unittest tests.test_part_set_discovery -v
python -m unittest tests.test_make_sets_discovery_integration -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests.test_dump_json_and_load_json_round_trip -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] `oobb_base.py` imports `build_object_lookup` with `try/except` safety
- [ ] `_get_object_lookup()` lazily initializes and caches the lookup
- [ ] `get_thing_from_dict({"type": "circle", ...})` routes through discovered object's `action_fn`
- [ ] `get_thing_from_dict({"type": "plate", ...})` still works via legacy (not yet migrated)
- [ ] `get_thing_from_dict({"type": "bolt", ...})` routes through discovered object
- [ ] `get_thing_from_dict({"type": "test_gear", ...})` routes through discovered object
- [ ] Missing `oobb_arch` package → graceful degradation (legacy-only dispatch)
- [ ] All 3 new tests pass
- [ ] All pre-existing tests still pass (zero regressions)
- [ ] Snapshot/capability tests produce identical output

---

## Risk Notes

- **Circular imports**: `oobb_base.py` already imports `oobb_get_items_oobb` etc. at module level. The new `build_object_lookup` import must be at module level with try/except, but the actual discovery (which loads working.py files that themselves import legacy modules) only happens lazily on first call. This avoids circular import at import time.
- **Cache invalidation**: Once `_OBJECT_LOOKUP` is populated, it is never refreshed during a process lifetime. This is acceptable because the discovery root doesn't change at runtime.
- **Performance**: Discovery scans the filesystem on first call. For the initial 3 objects this is negligible. At scale (Step 7/8 with 60+ objects), the cached lookup ensures this is a one-time cost.

---

## Estimated Scope

- ~20 lines of changes in `oobb_base.py`
- ~80 lines of test code
- No new files created (only modifications + new test file)
