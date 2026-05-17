"""Utilities for checking whether legacy functions are forwarders."""

from __future__ import annotations

import inspect
from typing import Any


def is_forwarder(module: Any, function_name: str) -> tuple[bool, str]:
    """Return ``(is_forwarder, details)`` for a function in ``module``."""
    func = getattr(module, function_name, None)
    if func is None:
        return False, f"{function_name} not found in module {getattr(module, '__name__', module)}"

    try:
        source = inspect.getsource(func)
    except (OSError, TypeError) as exc:
        return False, f"Unable to inspect source for {function_name}: {exc}"

    if "from part_calls.objects" in source and "return action(" in source:
        return True, source

    if "return" in source and ".working import action" in source:
        return True, source

    return False, f"Does not look like a forwarder:\n{source[:400]}"
