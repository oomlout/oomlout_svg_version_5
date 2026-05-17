from __future__ import annotations

from pathlib import Path


def _template(set_name: str) -> str:
    title = set_name.replace("_", " ").title()
    return f'''d = {{}}


def define():
    global d
    if not d:
        d = {{
            "name": "{set_name}",
            "name_short": [],
            "name_long": "OOBB Part Set: {title}",
            "description": "{set_name} part-set definitions.",
            "category": "Part Sets",
            "variables": ["size"],
        }}
    return dict(d)


def items(size="oobb", **kwargs):
    import oobb_make_sets

    getter = getattr(oobb_make_sets, "get_{set_name}")
    try:
        return getter(size=size, **kwargs)
    except TypeError:
        return getter(**kwargs)


def test(**kwargs):
    return isinstance(items(**kwargs), list)
'''


def create_set_scaffold(set_name: str, sets_root: str | Path | None = None, overwrite: bool = False) -> Path:
    if not set_name or not set_name.strip():
        raise ValueError("set_name must be a non-empty string")

    root = Path(sets_root) if sets_root is not None else (Path(__file__).resolve().parent / "sets")
    target_dir = root / set_name.strip()
    target_dir.mkdir(parents=True, exist_ok=True)
    working_file = target_dir / "working.py"

    if working_file.exists() and not overwrite:
        return working_file

    working_file.write_text(_template(set_name=set_name.strip()), encoding="utf-8")
    return working_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a part set working.py scaffold")
    parser.add_argument("set_name", help="Folder/name of the part set")
    parser.add_argument("--sets-root", default=None, help="Optional custom sets root")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing working.py")
    args = parser.parse_args()

    path = create_set_scaffold(set_name=args.set_name, sets_root=args.sets_root, overwrite=args.overwrite)
    print(path)
