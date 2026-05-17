# Step 01 — Output Comparison Harness

## Objective

Build reusable test infrastructure that captures the output of any `get_*` function via the **legacy path** and compares it against the **folder path** after migration. This harness is used by every subsequent step as the correctness contract.

## Prerequisite

- All existing tests pass: `python -m unittest discover -s tests -p "test_*.py"`

## What Gets Created

### 1. `oobb_arch/testing/__init__.py`
Empty package init.

### 2. `oobb_arch/testing/output_compare.py`

Core comparison utilities:

```python
"""
Output comparison harness for code migration.

Captures the result of calling a builder function through the legacy
path and compares it to calling through the folder-based path.
Ensures byte-for-byte equivalence of the thing dict structure.
"""
import json
import copy

def capture_legacy_output(module, function_name, kwargs):
    """Call a legacy get_* function and return its output dict."""
    func = getattr(module, function_name)
    return func(**copy.deepcopy(kwargs))

def capture_folder_output(folder_module, kwargs):
    """Call a folder working.py action() and return its output dict."""
    return folder_module.action(**copy.deepcopy(kwargs))

def normalize_thing_for_comparison(thing):
    """
    Deep-normalize a thing dict for stable comparison.
    - Strips volatile keys (file paths, timestamps)
    - Sorts component lists by deterministic key
    - Converts floats to fixed precision
    """
    if not isinstance(thing, dict):
        return thing
    cleaned = {}
    skip_keys = {"file_path", "timestamp", "build_time"}
    for key, value in sorted(thing.items()):
        if key in skip_keys:
            continue
        cleaned[key] = _normalize_value(value)
    return cleaned

def _normalize_value(value):
    if isinstance(value, dict):
        return normalize_thing_for_comparison(value)
    elif isinstance(value, list):
        return [_normalize_value(v) for v in value]
    elif isinstance(value, float):
        return round(value, 10)
    return value

def compare_outputs(legacy_output, folder_output):
    """
    Compare two thing dicts. Returns (is_equal, diff_summary).
    diff_summary is empty string if equal, otherwise describes first difference.
    """
    norm_legacy = normalize_thing_for_comparison(legacy_output)
    norm_folder = normalize_thing_for_comparison(folder_output)

    legacy_json = json.dumps(norm_legacy, sort_keys=True, default=str)
    folder_json = json.dumps(norm_folder, sort_keys=True, default=str)

    if legacy_json == folder_json:
        return True, ""

    # Find first difference
    for i, (a, b) in enumerate(zip(legacy_json, folder_json)):
        if a != b:
            context = 50
            start = max(0, i - context)
            end = min(len(legacy_json), i + context)
            return False, (
                f"First diff at char {i}:\n"
                f"  legacy: ...{legacy_json[start:end]}...\n"
                f"  folder: ...{folder_json[start:end]}..."
            )

    return False, f"Length mismatch: legacy={len(legacy_json)}, folder={len(folder_json)}"


def assert_migration_equivalent(test_case, module, function_name, folder_module, test_kwargs_list):
    """
    High-level assertion for use in unittest.TestCase subclasses.

    test_kwargs_list: list of kwargs dicts to test with.
    Calls both legacy and folder paths for each, asserts outputs match.
    """
    for kwargs in test_kwargs_list:
        legacy = capture_legacy_output(module, function_name, kwargs)
        folder = capture_folder_output(folder_module, kwargs)
        is_equal, diff = compare_outputs(legacy, folder)
        test_case.assertTrue(
            is_equal,
            f"Output mismatch for {function_name}({kwargs}):\n{diff}"
        )
```

### 3. `oobb_arch/testing/forwarder_check.py`

Utility to verify a legacy function has been replaced with a proper forwarder:

```python
"""
Verify that a legacy function is now a forwarder to a folder working.py.
"""
import inspect

def is_forwarder(module, function_name):
    """
    Check if a function body is a one-line forwarder.
    Returns (True, target_module_path) or (False, reason).
    """
    func = getattr(module, function_name, None)
    if func is None:
        return False, f"{function_name} not found in module"

    source = inspect.getsource(func)
    lines = [l.strip() for l in source.split("\n") if l.strip() and not l.strip().startswith("#") and not l.strip().startswith('"""')]

    # Should have: def line, from...import line, return line
    if "from part_calls" in source and "return action(" in source:
        return True, source
    return False, f"Does not look like a forwarder:\n{source[:200]}"
```

### 4. `tests/test_output_comparison_harness.py`

```python
"""Tests for the output comparison harness itself."""
import unittest
import copy

class TestNormalization(unittest.TestCase):
    def test_normalize_strips_volatile_keys(self):
        from oobb_arch.testing.output_compare import normalize_thing_for_comparison
        thing = {"id": "test", "file_path": "/tmp/foo", "components": []}
        result = normalize_thing_for_comparison(thing)
        self.assertNotIn("file_path", result)
        self.assertIn("id", result)

    def test_normalize_rounds_floats(self):
        from oobb_arch.testing.output_compare import normalize_thing_for_comparison
        thing = {"value": 3.1415926535897932384626}
        result = normalize_thing_for_comparison(thing)
        self.assertEqual(result["value"], round(3.1415926535897932384626, 10))

    def test_compare_identical(self):
        from oobb_arch.testing.output_compare import compare_outputs
        a = {"id": "test", "components": [{"type": "p", "pos": [0, 0, 0]}]}
        b = copy.deepcopy(a)
        is_eq, diff = compare_outputs(a, b)
        self.assertTrue(is_eq)
        self.assertEqual(diff, "")

    def test_compare_different(self):
        from oobb_arch.testing.output_compare import compare_outputs
        a = {"id": "test", "components": [{"type": "p"}]}
        b = {"id": "test", "components": [{"type": "n"}]}
        is_eq, diff = compare_outputs(a, b)
        self.assertFalse(is_eq)
        self.assertIn("First diff", diff)

    def test_compare_ignores_volatile(self):
        from oobb_arch.testing.output_compare import compare_outputs
        a = {"id": "test", "timestamp": "2024-01-01", "components": []}
        b = {"id": "test", "timestamp": "2025-12-31", "components": []}
        is_eq, _ = compare_outputs(a, b)
        self.assertTrue(is_eq)

    def test_end_to_end_legacy_capture(self):
        """Verify capture_legacy_output works with a real module."""
        import oobb
        import oobb_get_items_other
        from oobb_arch.testing.output_compare import capture_legacy_output
        result = capture_legacy_output(
            oobb_get_items_other, "get_bolt",
            {"type": "bolt", "radius_name": "m3", "depth": 10}
        )
        self.assertIsInstance(result, dict)
        self.assertIn("components", result)
```

## Files Modified

None — this step only adds new files.

## Test Gate

Run tests, confirm they pass, then proceed. Do not review diffs.

**Contract:** All existing tests PLUS `test_output_comparison_harness.py` (6 new tests) pass.

## Rollback

Delete `oobb_arch/testing/` and `tests/test_output_comparison_harness.py`.
