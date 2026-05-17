"""Output comparison harness for migration parity checks."""

from __future__ import annotations

import copy
import json
from typing import Any


_VOLATILE_KEYS = {"file_path", "timestamp", "build_time"}


def capture_legacy_output(module: Any, function_name: str, kwargs: dict[str, Any]) -> Any:
    """Call a legacy ``get_*`` function and return its output."""
    func = getattr(module, function_name)
    return func(**copy.deepcopy(kwargs))


def capture_folder_output(folder_module: Any, kwargs: dict[str, Any]) -> Any:
    """Call a folder ``working.py`` ``action()`` and return its output."""
    return folder_module.action(**copy.deepcopy(kwargs))


def _normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in sorted(value.items(), key=lambda kv: str(kv[0])):
            if key in _VOLATILE_KEYS:
                continue
            cleaned[key] = _normalize_value(item)
        return cleaned
    if isinstance(value, list):
        return [_normalize_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_normalize_value(item) for item in value)
    if isinstance(value, float):
        return round(value, 10)
    return value


def normalize_thing_for_comparison(thing: Any) -> Any:
    """Normalize nested structures for stable deterministic comparison."""
    return _normalize_value(thing)


def compare_outputs(legacy_output: Any, folder_output: Any) -> tuple[bool, str]:
    """Compare two outputs and return ``(equal, diff_summary)``."""
    norm_legacy = normalize_thing_for_comparison(legacy_output)
    norm_folder = normalize_thing_for_comparison(folder_output)

    legacy_json = json.dumps(norm_legacy, sort_keys=True, default=str)
    folder_json = json.dumps(norm_folder, sort_keys=True, default=str)

    if legacy_json == folder_json:
        return True, ""

    max_len = min(len(legacy_json), len(folder_json))
    first_diff = 0
    while first_diff < max_len and legacy_json[first_diff] == folder_json[first_diff]:
        first_diff += 1

    context = 50
    start = max(0, first_diff - context)
    end_legacy = min(len(legacy_json), first_diff + context)
    end_folder = min(len(folder_json), first_diff + context)

    diff = (
        f"First diff at char {first_diff}:\n"
        f"  legacy: ...{legacy_json[start:end_legacy]}...\n"
        f"  folder: ...{folder_json[start:end_folder]}..."
    )
    if len(legacy_json) != len(folder_json):
        diff += f"\nLength mismatch: legacy={len(legacy_json)}, folder={len(folder_json)}"

    return False, diff


def assert_migration_equivalent(
    test_case: Any,
    module: Any,
    function_name: str,
    folder_module: Any,
    test_kwargs_list: list[dict[str, Any]],
) -> None:
    """Assert parity for a set of kwargs cases in a unittest test case."""
    for kwargs in test_kwargs_list:
        legacy = capture_legacy_output(module, function_name, kwargs)
        folder = capture_folder_output(folder_module, kwargs)
        equal, diff = compare_outputs(legacy, folder)
        test_case.assertTrue(equal, f"Output mismatch for {function_name}({kwargs}):\n{diff}")
