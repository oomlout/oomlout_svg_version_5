from __future__ import annotations

import inspect
from importlib import import_module
from pathlib import Path
from typing import Any


_SOURCE_MODULE_CATEGORY = {
    "oobb_get_items_oobb": "OOBB Geometry",
    "oobb_get_items_oobb_old": "OOBB Geometry (Legacy)",
    "oobb_get_items_oobb_wire": "OOBB Wire",
    "oobb_get_items_oobb_holder": "OOBB Holder",
    "oobb_get_items_oobb_other": "OOBB Other",
    "oobb_get_items_oobb_bearing_plate": "OOBB Bearing Plate",
    "oobb_get_items_other": "Hardware",
    "oobb_get_items_test": "OOBB Test",
}


def _title_from_type_name(type_name: str) -> str:
    return type_name.replace("_", " ").title()


def _introspect_legacy_function(module_name: str, func_name: str) -> list[dict[str, Any]]:
    try:
        module = import_module(module_name)
        func = getattr(module, func_name)
        signature = inspect.signature(func)
    except Exception:
        return []

    variables: list[dict[str, Any]] = []
    for parameter in signature.parameters.values():
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue
        default_value = "" if parameter.default is inspect._empty else parameter.default
        annotation = "" if parameter.annotation is inspect._empty else str(parameter.annotation)
        variables.append(
            {
                "name": parameter.name,
                "description": "",
                "type": annotation,
                "default": default_value,
            }
        )
    return variables


def _build_template(type_name: str, source_module: str, legacy_function_name: str) -> str:
    folder_name = type_name
    category = _SOURCE_MODULE_CATEGORY.get(source_module, "General")
    variables = _introspect_legacy_function(source_module, legacy_function_name)
    variables_repr = repr(variables)

    return f'''d = {{}}


def define():
    """Return metadata describing this object type."""
    global d
    if not d:
        d = {{
            "name": "{folder_name}",
            "name_short": ["{type_name}"],
            "name_long": "OOBB Object: {_title_from_type_name(type_name)}",
            "description": "Auto-generated scaffold for {type_name}. EDIT THIS.",
            "category": "{category}",
            "variables": {variables_repr},
            "source_module": "{source_module}",
        }}
    return dict(d)


def action(**kwargs):
    """Build and return the thing dict for this object type."""
    import {source_module}

    return {source_module}.{legacy_function_name}(**kwargs)


def test(**kwargs):
    """Smoke test for object generation."""
    try:
        result = action(type="{type_name}", **kwargs)
        return isinstance(result, dict) and "components" in result
    except Exception:
        return False
'''


def generate_object_scaffold(
    type_name: str,
    source_module: str,
    legacy_function_name: str,
    output_dir: str | Path | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    if not type_name or not type_name.strip():
        raise ValueError("type_name must be a non-empty string")
    if not source_module or not source_module.strip():
        raise ValueError("source_module must be a non-empty string")
    if not legacy_function_name or not legacy_function_name.strip():
        raise ValueError("legacy_function_name must be a non-empty string")

    root = Path(output_dir) if output_dir is not None else (Path(__file__).resolve().parents[2] / "components")
    folder_name = type_name.strip()
    target_dir = root / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    working_file = target_dir / "working.py"

    if working_file.exists() and not overwrite:
        return working_file

    template = _build_template(type_name.strip(), source_module.strip(), legacy_function_name.strip())
    working_file.write_text(template, encoding="utf-8")
    return working_file
