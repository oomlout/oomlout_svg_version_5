from __future__ import annotations

from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


@dataclass(frozen=True)
class DiscoveredPartSet:
    name: str
    path: Path
    metadata: dict[str, Any]
    items_fn: Callable[..., list[dict[str, Any]]]
    test_fn: Callable[..., Any] | None
    aliases: tuple[str, ...] = ()


def resolve_part_sets_root(sets_root: str | Path | None = None) -> Path:
    if sets_root is not None:
        return Path(sets_root).resolve()
    return (Path(__file__).resolve().parents[2] / "components").resolve()


def _load_module_from_file(file_path: Path, set_name: str) -> ModuleType:
    module_name = f"oobb_part_set_{set_name}_{abs(hash(str(file_path)))}"
    spec = spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {file_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extract_aliases(metadata: dict[str, Any]) -> list[str]:
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


def discover_part_sets(sets_root: str | Path | None = None) -> dict[str, DiscoveredPartSet]:
    root = resolve_part_sets_root(sets_root)
    discovered: dict[str, DiscoveredPartSet] = {}
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
        except Exception:
            continue

        define_fn = getattr(module, "define", None)
        items_fn = getattr(module, "items", None)
        test_fn = getattr(module, "test", None)
        if not callable(define_fn) or not callable(items_fn):
            continue

        metadata_raw = define_fn()
        metadata = metadata_raw if isinstance(metadata_raw, dict) else {}
        metadata.setdefault("name", entry.name)
        metadata.setdefault("description", "")
        metadata.setdefault("category", "Part Sets")
        metadata.setdefault("variables", ["size"])

        declared_name = metadata.get("name", entry.name)
        if declared_name != entry.name:
            metadata["name"] = entry.name

        discovered[entry.name] = DiscoveredPartSet(
            name=entry.name,
            path=working_file,
            metadata=metadata,
            items_fn=items_fn,
            test_fn=test_fn if callable(test_fn) else None,
            aliases=tuple(_extract_aliases(metadata)),
        )

    return discovered


def build_part_set_lookup(sets_root: str | Path | None = None) -> dict[str, DiscoveredPartSet]:
    sets = discover_part_sets(sets_root=sets_root)
    lookup: dict[str, DiscoveredPartSet] = {}
    for set_name, discovered_set in sets.items():
        lookup[set_name] = discovered_set

    for set_name, discovered_set in sets.items():
        for alias in discovered_set.aliases:
            if alias not in lookup:
                lookup[alias] = discovered_set

    return lookup
