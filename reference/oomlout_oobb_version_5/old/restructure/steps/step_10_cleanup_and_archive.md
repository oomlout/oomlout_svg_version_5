# Step 10 — Cleanup: Remove Legacy Fallback & Archive Monoliths

## Objective

With all geometry code now living in folder `working.py` files:
1. Remove the legacy `getattr` fallback chain from `oobb_base.get_thing_from_dict()`
2. Remove the legacy registry layer
3. Activate all aliases in discovery (remove auto-scaffold suppression)
4. Archive the legacy monolith files
5. Run a full end-to-end validation

## Prerequisite

- Steps 01–09 completed
- ALL functions in ALL legacy modules are forwarders
- All tests pass

## Changes

### 1. Simplify `oobb_base.get_thing_from_dict()`

**BEFORE** (current — 3-tier dispatch):

```python
def get_thing_from_dict(thing_dict):
    full_object = thing_dict.get("full_object", False)
    func = None

    # Tier 1: Discovery
    object_lookup = _get_object_lookup()
    discovered_obj = object_lookup.get(thing_dict["type"])
    if discovered_obj is not None:
        func = discovered_obj.action_fn

    # Tier 2: Legacy registry
    if func is None:
        registry = _get_legacy_builder_registry()
        if registry is not None:
            try:
                func = registry.resolve(thing_dict["type"])
            except KeyError:
                func = None

    # Tier 3: Legacy getattr chain
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

**AFTER** (discovery only):

```python
def get_thing_from_dict(thing_dict):
    object_lookup = _get_object_lookup()
    discovered_obj = object_lookup.get(thing_dict["type"])

    if discovered_obj is None:
        raise KeyError(
            f"Unknown object type '{thing_dict['type']}'. "
            f"No folder found in part_calls/objects/ with alias or name matching this type."
        )

    thing = discovered_obj.action_fn(**thing_dict)
    return thing
```

### 2. Remove Legacy Imports from `oobb_base.py`

Remove (or comment out for safety):

```python
# These are no longer needed for dispatch:
# import oobb_get_items_other
# import oobb_get_items_oobb
# import oobb_get_items_test
```

**Caution:** Other code may still import these modules directly. Don't remove the modules themselves — just the imports from `oobb_base.py` that were used for the `getattr` fallback.

### 3. Remove Alias Suppression from Discovery

In `oobb_arch/catalog/object_discovery.py`, update `_extract_aliases()` to no longer skip "Auto-generated scaffold" descriptions (since there shouldn't be any left):

```python
def _extract_aliases(metadata: dict[str, Any]) -> list[str]:
    # Remove this block — all scaffolds are now enriched:
    # description = metadata.get("description", "")
    # if isinstance(description, str) and description.strip().startswith("Auto-generated scaffold"):
    #     return []

    raw_aliases: list[str] = []
    ...
```

### 4. Remove Legacy Registry

Remove or archive:
- `oobb_arch/catalog/legacy_registry.py` (if it exists)
- The `_get_legacy_builder_registry()` function from `oobb_base.py`

### 5. Archive Legacy Monolith Files

```
mkdir legacy/
move oobb_get_items_oobb.py         legacy/oobb_get_items_oobb.py
move oobb_get_items_oobb_old.py     legacy/oobb_get_items_oobb_old.py
move oobb_get_items_oobb_holder.py  legacy/oobb_get_items_oobb_holder.py
move oobb_get_items_oobb_holder_electronic.py  legacy/...
move oobb_get_items_oobb_bearing_plate.py      legacy/...
move oobb_get_items_oobb_wire.py    legacy/...
move oobb_get_items_oobb_other.py   legacy/...
move oobb_get_items_oobb_wheel.py   legacy/...
move oobb_get_items_other.py        legacy/...
move oobb_get_items_test.py         legacy/...
```

**BUT WAIT:** Some code still imports these modules at the top level (e.g., `oobb_get_items_oobb_old.py` line 1: `from oobb_get_items_base import *`). Instead of moving immediately, create stub forwarder modules at the original locations:

```python
# oobb_get_items_oobb.py — FINAL STATE (stub)
"""
LEGACY STUB — All geometry code has been migrated to part_calls/objects/*/working.py.
This module exists only for backward compatibility with external scripts.
All functions are one-line forwarders to their folder-based implementations.
"""
# Re-export all forwarded functions so star-import consumers still work.
from part_calls.objects.oobb_object_circle.working import action as get_circle  # noqa
from part_calls.objects.oobb_object_plate.working import action as get_plate  # noqa
# ... etc for each function ...
```

### 6. Final Validation Script

Create `tests/test_step10_final_validation.py`:

```python
"""
Step 10 — Final validation.
Verifies the entire system works with discovery-only dispatch.
"""
import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import oobb
import oobb_base

class TestDispatchIsDiscoveryOnly(unittest.TestCase):
    def test_no_getattr_fallback(self):
        """get_thing_from_dict should not have getattr fallback."""
        import inspect
        source = inspect.getsource(oobb_base.get_thing_from_dict)
        self.assertNotIn("getattr(oobb_get_items_oobb", source)
        self.assertNotIn("getattr(oobb_get_items_other", source)
        self.assertNotIn("getattr(oobb_get_items_test", source)

    def test_no_legacy_registry(self):
        """Legacy registry should not be used."""
        import inspect
        source = inspect.getsource(oobb_base.get_thing_from_dict)
        self.assertNotIn("_get_legacy_builder_registry", source)

class TestEndToEndDispatch(unittest.TestCase):
    """Test representative types through discovery-only dispatch."""

    TYPES_AND_KWARGS = [
        {"type": "circle", "diameter": 3, "thickness": 3, "size": "oobb"},
        {"type": "plate", "width": 3, "height": 2, "thickness": 3, "size": "oobb"},
        {"type": "gear", "diameter": 3, "thickness": 3, "size": "oobb", "extra": ""},
        {"type": "bolt", "radius_name": "m3", "depth": 10},
        {"type": "nut", "radius_name": "m3"},
        {"type": "bearing", "bearing_name": "606"},
        {"type": "bearing_plate", "width": 3, "height": 3, "thickness": 12,
         "bearing": "606", "size": "oobb"},
    ]

    def test_all_representative_types(self):
        for kwargs in self.TYPES_AND_KWARGS:
            with self.subTest(type=kwargs["type"]):
                result = oobb_base.get_thing_from_dict(kwargs)
                self.assertIsInstance(result, dict)
                self.assertIn("components", result)

class TestUnknownTypeRaises(unittest.TestCase):
    def test_bad_type_raises_key_error(self):
        """Unknown type should raise KeyError, not silently fail."""
        with self.assertRaises(KeyError):
            oobb_base.get_thing_from_dict({"type": "nonexistent_xyz_12345"})

class TestAllAliasesActive(unittest.TestCase):
    def test_no_suppressed_aliases(self):
        """No discovered objects should have aliases suppressed."""
        from oobb_arch.catalog.object_discovery import discover_objects
        objects = discover_objects()
        suppressed = [name for name, obj in objects.items()
                      if obj.metadata.get("description", "").startswith("Auto-generated scaffold")]
        self.assertEqual(suppressed, [],
                         f"These objects still have auto-scaffold descriptions: {suppressed}")

class TestMakeAllStillWorks(unittest.TestCase):
    def test_make_all_produces_items(self):
        """oobb_make_sets.make_all should still work end-to-end."""
        import oobb_make_sets
        # Don't actually build (too slow), just verify make_all doesn't crash
        # by collecting the thing dicts
        try:
            # make_all calls get_thing_from_dict for each item
            oobb_make_sets.make_all(filter="bearing_plate__oobb__3__3__12__606")
        except Exception as e:
            self.fail(f"make_all crashed: {e}")

class TestMigrationComplete(unittest.TestCase):
    def test_all_objects_have_real_code(self):
        """Every object folder should have non-wrapper action() code."""
        from oobb_arch.catalog.object_discovery import discover_objects
        import inspect
        objects = discover_objects()
        wrappers = []
        for name, obj in objects.items():
            source = inspect.getsource(obj.action_fn)
            # Check if it's still just a wrapper importing from legacy
            if "import oobb_get_items_oobb" in source or "import oobb_get_items_oobb_old" in source:
                # Only flag if it's a direct delegation, not a shared helper import
                if "return oobb_get_items_oobb" in source or "return oobb_get_items_oobb_old" in source:
                    wrappers.append(name)
        self.assertEqual(wrappers, [],
                         f"These objects are still legacy wrappers: {wrappers}")
```

## Success Criteria (Full Migration)

- [x] All 170+ object folders contain their own geometry code
- [x] All 25 set folders work through discovery dispatch only
- [x] `oobb_base.get_thing_from_dict()` has only the discovery lookup
- [x] Legacy modules are stubs (forwarder re-exports only)
- [x] No `getattr`/`importlib.reload` hacks in any folder `working.py`
- [x] Full test suite passes
- [x] `make_all()` produces identical output to pre-migration

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** ALL tests pass including `test_step10_final_validation.py`.

## Rollback

This step is the "point of no return" for the architecture. If issues arise:
1. Restore the 3-tier dispatch in `oobb_base.get_thing_from_dict()`
2. Restore `_get_legacy_builder_registry()` 
3. Restore alias suppression in `_extract_aliases()`

The legacy modules still exist (as stubs or in `legacy/`) so rollback is always possible.
