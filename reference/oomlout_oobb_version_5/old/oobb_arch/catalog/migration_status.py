from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from .object_discovery import discover_objects
from .part_set_discovery import discover_part_sets


# Maps singular legacy type names to their plural component folder names.
_MERGE_MAP: dict[str, str] = {
    "bearing": "bearings", "bearing_circle": "bearing_circles",
    "bearing_plate": "bearing_plates", "circle": "circles",
    "gear": "gears", "holder": "holders", "jack": "jacks",
    "jig": "jigs", "mounting_plate": "mounting_plates", "nut": "nuts",
    "other": "others", "plate": "plates", "pulley_gt2": "pulleys",
    "shaft": "shafts", "shaft_coupler": "shaft_couplers",
    "smd_magazine": "smd_magazines", "soldering_jig": "soldering_jigs",
    "test": "tests", "tool_holder": "tool_holders", "tray": "trays",
    "wheel": "wheels", "wire": "wires", "ziptie_holder": "ziptie_holders",
    "bunting_alphabet": "buntings",
}


_OBJECT_SOURCE_FILES = [
    ("oobb_get_items_oobb", "oobb_get_items_oobb.py"),
    ("oobb_get_items_oobb_old", "oobb_get_items_oobb_old.py"),
    ("oobb_get_items_oobb_wire", "oobb_get_items_oobb_wire.py"),
    ("oobb_get_items_oobb_holder", "oobb_get_items_oobb_holder.py"),
    ("oobb_get_items_oobb_other", "oobb_get_items_oobb_other.py"),
    ("oobb_get_items_oobb_bearing_plate", "oobb_get_items_oobb_bearing_plate.py"),
    ("oobb_get_items_other", "oobb_get_items_other.py"),
    ("oobb_get_items_test", "oobb_get_items_test.py"),
]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _parse_get_functions(file_path: Path) -> list[str]:
    if not file_path.is_file():
        return []
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("get_"):
            names.append(node.name)
    return names


def get_all_legacy_object_functions() -> list[dict[str, str]]:
    root = _project_root()
    items: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for module_name, relative_file in _OBJECT_SOURCE_FILES:
        file_path = root / relative_file
        for function_name in _parse_get_functions(file_path):
            type_name = function_name[4:]
            key = (type_name, function_name)
            if key in seen:
                continue
            seen.add(key)
            items.append(
                {
                    "type_name": type_name,
                    "function_name": function_name,
                    "source_module": module_name,
                    "full_name": f"oobb_object_{type_name}",
                }
            )

    return sorted(items, key=lambda item: item["type_name"])


def get_all_legacy_set_functions() -> list[dict[str, str]]:
    file_path = _project_root() / "oobb_make_sets.py"
    items: list[dict[str, str]] = []
    for function_name in _parse_get_functions(file_path):
        set_name = function_name[4:]
        if set_name == "set_items_discovered":
            continue
        items.append(
            {
                "set_name": set_name,
                "function_name": function_name,
                "source_module": "oobb_make_sets",
            }
        )
    return sorted(items, key=lambda item: item["set_name"])


def _safe_percentage(migrated: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((migrated / total) * 100.0, 1)


def get_migration_status(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
) -> dict[str, Any]:
    legacy_objects = get_all_legacy_object_functions()
    legacy_object_names = sorted({item["type_name"] for item in legacy_objects})

    discovered_objects = discover_objects(objects_root=objects_root)
    discovered_object_names = {name.replace("oobb_object_", "") for name in discovered_objects.keys()}

    # Also consider merge-map aliases (singular → plural folder names).
    def _object_is_migrated(name: str) -> bool:
        if name in discovered_object_names:
            return True
        mapped = _MERGE_MAP.get(name)
        return mapped is not None and mapped in discovered_object_names

    migrated_objects = sorted([name for name in legacy_object_names if _object_is_migrated(name)])
    pending_objects = sorted([name for name in legacy_object_names if not _object_is_migrated(name)])

    legacy_sets = get_all_legacy_set_functions()
    legacy_set_names = sorted({item["set_name"] for item in legacy_sets})

    discovered_sets = discover_part_sets(sets_root=sets_root)
    discovered_set_names = set(discovered_sets.keys())

    migrated_sets = sorted([name for name in legacy_set_names if name in discovered_set_names])
    pending_sets = sorted([name for name in legacy_set_names if name not in discovered_set_names])

    return {
        "objects": {
            "total_legacy": len(legacy_object_names),
            "total_migrated": len(migrated_objects),
            "migrated": migrated_objects,
            "pending": pending_objects,
            "percentage": _safe_percentage(len(migrated_objects), len(legacy_object_names)),
        },
        "sets": {
            "total_legacy": len(legacy_set_names),
            "total_migrated": len(migrated_sets),
            "migrated": migrated_sets,
            "pending": pending_sets,
            "percentage": _safe_percentage(len(migrated_sets), len(legacy_set_names)),
        },
    }


def print_migration_report(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    status = get_migration_status(objects_root=objects_root, sets_root=sets_root)
    objects = status["objects"]
    sets = status["sets"]

    print("=" * 44)
    print(" OOBB Migration Status Report")
    print("=" * 44)
    print("")
    print(
        f"OBJECTS: {objects['total_migrated']} / {objects['total_legacy']} migrated ({objects['percentage']}%)"
    )
    for name in objects["migrated"]:
        print(f"✓ {name}")
    for name in objects["pending"]:
        print(f"✗ {name}")
    print("")
    print(f"SETS: {sets['total_migrated']} / {sets['total_legacy']} migrated ({sets['percentage']}%)")
    for name in sets["migrated"]:
        print(f"✓ {name}")
    for name in sets["pending"]:
        print(f"✗ {name}")
