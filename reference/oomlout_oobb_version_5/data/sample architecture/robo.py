from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from oomlout_roboclick import check_key_pressed, delay, robo_delay, scroll_lock_toggled

__all__ = [
    "check_key_pressed",
    "delay",
    "robo_delay",
    "scroll_lock_toggled",
]

_legacy_robo_module = None


def _load_legacy_robo_module():
    global _legacy_robo_module
    if _legacy_robo_module is not None:
        return _legacy_robo_module

    legacy_path = Path(__file__).resolve().parent / "old" / "robo.py"
    if not legacy_path.is_file():
        _legacy_robo_module = False
        return None

    spec = spec_from_file_location("roboclick_legacy_robo", str(legacy_path))
    if spec is None or spec.loader is None:
        _legacy_robo_module = False
        return None

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    _legacy_robo_module = module
    return module


def __getattr__(name):
    legacy_module = _load_legacy_robo_module()
    if legacy_module and hasattr(legacy_module, name):
        return getattr(legacy_module, name)
    raise AttributeError(f"module 'robo' has no attribute '{name}'")
