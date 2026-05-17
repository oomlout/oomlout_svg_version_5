# Step 02 — Shared Helpers Extraction

## Objective

Extract pure utility functions that are used by multiple object types into `oobb_arch/helpers/`, so that migrated folder `working.py` files can import helpers directly without depending on the legacy monolith modules.

## Prerequisite

- Step 01 completed (output comparison harness available)
- All tests pass

## Analysis: Which Functions Are Helpers?

### From `oobb_get_items_oobb.py` (lines 11–38)

| Function | Lines | Used By | Purpose |
|----------|-------|---------|---------|
| `get_plate_dict(**kwargs)` | 11–22 | `oobb_get_items_oobb_wire`, `oobb_get_items_oobb_holder_electronic` | Builds a plate component dict |
| `get_plate_hole_dict(**kwargs)` | 24–38 | `oobb_get_items_oobb_wire`, `oobb_get_items_oobb_holder_electronic` | Builds a plate-hole component dict |

### From `oobb_get_items_oobb.py` (lines 359–428)

| Function | Lines | Used By | Purpose |
|----------|-------|---------|---------|
| `add_oobb_shaft(**kwargs)` | 359–395 | `get_gear()` | Adds shaft cutout to a thing |
| `get_shaft_center(thing, **kwargs)` | 1402–1435 | `get_circle_base()` | Adds shaft center features |

### From `oobb_get_items_oobb_holder_electronic.py` (lines 261–295)

| Function | Lines | Used By | Purpose |
|----------|-------|---------|---------|
| `get_plate_cutout_dict(**kwargs)` | 261–275 | Multiple holder electronic functions | Builds cutout component dict |
| `get_plate_screw_dict(**kwargs)` | 277–295 | Multiple holder electronic functions | Builds screw component dict |

### From `oobb_get_items_oobb_wire.py` (line 137)

| Function | Lines | Used By | Purpose |
|----------|-------|---------|---------|
| `get_plate_nut_dict(**kwargs)` | 137+ | Wire functions | Builds nut plate component dict |

## What Gets Created

### 1. `oobb_arch/helpers/__init__.py`

```python
from oobb_arch.helpers.plate_helpers import (
    get_plate_dict,
    get_plate_hole_dict,
)
from oobb_arch.helpers.shaft_helpers import (
    add_oobb_shaft,
    get_shaft_center,
)
```

### 2. `oobb_arch/helpers/plate_helpers.py`

Code copied verbatim from `oobb_get_items_oobb.py` lines 11–38:

```python
"""Shared plate component helper functions."""
import copy

def get_plate_dict(**kwargs):
    # ... exact code from oobb_get_items_oobb.py lines 11-22 ...

def get_plate_hole_dict(**kwargs):
    # ... exact code from oobb_get_items_oobb.py lines 24-38 ...
```

### 3. `oobb_arch/helpers/shaft_helpers.py`

Code copied verbatim:

```python
"""Shared shaft/center helper functions."""
import copy
import oobb_base

def add_oobb_shaft(**kwargs):
    # ... exact code from oobb_get_items_oobb.py add_oobb_shaft ...

def get_shaft_center(thing, **kwargs):
    # ... exact code from oobb_get_items_oobb.py get_shaft_center ...
```

## What Gets Modified

### 4. `oobb_get_items_oobb.py` — Replace helper function bodies with imports

The original functions become forwarders:

```python
# At top of file, add:
from oobb_arch.helpers.plate_helpers import get_plate_dict, get_plate_hole_dict
from oobb_arch.helpers.shaft_helpers import add_oobb_shaft, get_shaft_center

# Delete the original function bodies (lines 11-38) and replace with:
# (functions are now imported above — no forwarder body needed since they're
#  re-exported via the import. Star-import consumers still see them.)
```

**Key insight:** Since `oobb_get_items_oobb.py` uses `from oobb_get_items_oobb_old import *` and other files do `from oobb_get_items_oobb import *`, we can either:
- (A) Keep the function definitions but have them call the helper, OR
- (B) Import the helpers at module level so they're available in the namespace

Option (B) is cleaner. The `import` at module level means `get_plate_dict` is in `oobb_get_items_oobb`'s namespace, so star-import consumers still find it.

### Important: Do NOT modify the calling code yet

- `oobb_get_items_oobb_wire.py` still calls `oobb_get_items_oobb.get_plate_dict()` — this keeps working because the import re-exports the name.
- `oobb_get_items_oobb_holder_electronic.py` still calls `oobb_get_items_oobb.get_plate_dict()` — same.

## Tests

### 5. `tests/test_shared_helpers.py`

```python
"""Tests for shared helpers extraction."""
import unittest

class TestPlateHelpers(unittest.TestCase):
    def test_get_plate_dict_returns_dict(self):
        from oobb_arch.helpers.plate_helpers import get_plate_dict
        result = get_plate_dict(size="oobb", thickness=3, pos_plate=[0,0,0])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["type"], "positive")
        self.assertEqual(result["shape"], "oobb_plate")

    def test_get_plate_hole_dict_returns_dict(self):
        from oobb_arch.helpers.plate_helpers import get_plate_hole_dict
        result = get_plate_hole_dict(size="oobb", pos_plate=[0,0,0])
        self.assertIsInstance(result, dict)
        self.assertEqual(result["type"], "p")
        self.assertEqual(result["shape"], "oobb_holes")

    def test_helpers_match_legacy_plate_dict(self):
        """Verify helper output matches legacy module output."""
        import oobb
        import oobb_get_items_oobb
        from oobb_arch.helpers.plate_helpers import get_plate_dict
        from oobb_arch.testing.output_compare import compare_outputs

        kwargs = {"size": "oobb", "thickness": 3, "pos_plate": [0,0,0]}
        legacy = oobb_get_items_oobb.get_plate_dict(**kwargs)
        helper = get_plate_dict(**kwargs)
        is_eq, diff = compare_outputs(legacy, helper)
        self.assertTrue(is_eq, f"Mismatch: {diff}")

    def test_helpers_match_legacy_plate_hole_dict(self):
        import oobb
        import oobb_get_items_oobb
        from oobb_arch.helpers.plate_helpers import get_plate_hole_dict
        from oobb_arch.testing.output_compare import compare_outputs

        kwargs = {"size": "oobb", "pos_plate": [0,0,0], "hole_sides": ["left","right","top"]}
        legacy = oobb_get_items_oobb.get_plate_hole_dict(**kwargs)
        helper = get_plate_hole_dict(**kwargs)
        is_eq, diff = compare_outputs(legacy, helper)
        self.assertTrue(is_eq, f"Mismatch: {diff}")

    def test_legacy_module_still_exports_helpers(self):
        """After migration, oobb_get_items_oobb.get_plate_dict still works."""
        import oobb
        import oobb_get_items_oobb
        self.assertTrue(hasattr(oobb_get_items_oobb, "get_plate_dict"))
        self.assertTrue(hasattr(oobb_get_items_oobb, "get_plate_hole_dict"))
        result = oobb_get_items_oobb.get_plate_dict(size="oobb", thickness=3, pos_plate=[0,0,0])
        self.assertIsInstance(result, dict)
```

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_shared_helpers.py` (5 new tests) pass.

## Rollback

1. Restore original function bodies in `oobb_get_items_oobb.py`
2. Delete `oobb_arch/helpers/`
3. Delete `tests/test_shared_helpers.py`
