from __future__ import annotations

from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Callable
import warnings


@dataclass(frozen=True)
class DiscoveredObject:
    name: str
    path: Path
    metadata: dict[str, Any]
    action_fn: Callable[..., Any]
    test_fn: Callable[..., Any] | None
    aliases: tuple[str, ...] = ()


def resolve_objects_root(objects_root: str | Path | None = None) -> Path:
    if objects_root is not None:
        return Path(objects_root).resolve()
    return (Path(__file__).resolve().parents[2] / "components").resolve()


def _load_module_from_file(file_path: Path, object_name: str) -> ModuleType:
    module_name = f"oobb_object_{object_name}_{abs(hash(str(file_path)))}"
    spec = spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {file_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extract_aliases(metadata: dict[str, Any]) -> list[str]:
    description = metadata.get("description", "")
    if isinstance(description, str) and description.strip().startswith("Auto-generated scaffold"):
        return []

    raw_aliases: list[str] = []
    value = metadata.get("name_short")
    if isinstance(value, str):
        raw_aliases.append(value)
    elif isinstance(value, list):
        raw_aliases.extend([item for item in value if isinstance(item, str)])

    cleaned: list[str] = []
    seen: set[str] = set()
    for alias in raw_aliases:
        normal = alias.strip()
        if not normal or normal in seen:
            continue
        seen.add(normal)
        cleaned.append(normal)
    return cleaned


def discover_objects(objects_root: str | Path | None = None) -> dict[str, DiscoveredObject]:
    root = resolve_objects_root(objects_root)
    discovered: dict[str, DiscoveredObject] = {}
    if not root.exists():
        return discovered

    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        if not entry.is_dir():
            continue
        working_file = entry / "working.py"
        if not working_file.is_file():
            continue

        try:
            module = _load_module_from_file(working_file, entry.name)
        except Exception as exc:
            warnings.warn(f"Skipping object '{entry.name}': unable to load module ({exc})")
            continue

        define_fn = getattr(module, "define", None)
        action_fn = getattr(module, "action", None)
        test_fn = getattr(module, "test", None)

        if not callable(define_fn):
            warnings.warn(f"Skipping object '{entry.name}': missing callable define()")
            continue
        if not callable(action_fn):
            warnings.warn(f"Skipping object '{entry.name}': missing callable action()")
            continue

        metadata_raw = define_fn()
        metadata = metadata_raw if isinstance(metadata_raw, dict) else {}
        metadata.setdefault("name", entry.name)
        metadata.setdefault("description", "")
        metadata.setdefault("category", "Objects")
        metadata.setdefault("variables", [])

        declared_name = metadata.get("name", entry.name)
        if declared_name != entry.name:
            metadata["name"] = entry.name

        discovered[entry.name] = DiscoveredObject(
            name=entry.name,
            path=working_file,
            metadata=metadata,
            action_fn=action_fn,
            test_fn=test_fn if callable(test_fn) else None,
            aliases=tuple(_extract_aliases(metadata)),
        )

    return discovered


def build_object_lookup(objects_root: str | Path | None = None) -> dict[str, DiscoveredObject]:
    objects = discover_objects(objects_root=objects_root)
    lookup: dict[str, DiscoveredObject] = {}
    for object_name, discovered_object in objects.items():
        lookup[object_name] = discovered_object

    for object_name, discovered_object in objects.items():
        for alias in discovered_object.aliases:
            if alias not in lookup:
                lookup[alias] = discovered_object

    return lookup
