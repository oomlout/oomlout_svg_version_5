"""
generate_samples.py  —  Render a default sample SVG for every svg_component.

For each svg_components/<name>/working.py:
  1. Load define() to get default variable values.
  2. Call action(**defaults) to get shape descriptors.
  3. Render via opsvg.opsvg_get_svg() with a white background.
  4. Write to svg_components/<name>/sample.svg.

Usage
-----
    python generate_samples.py              # all components
    python generate_samples.py rect         # single component by name
    python generate_samples.py --force      # overwrite existing samples
"""

import importlib.util
import os
import sys
from pathlib import Path


# Ensure project root is on the path so opsvg imports cleanly.
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import opsvg
import svg_variables as _sv


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _load_module(working_py: Path):
    name = f"_sample_gen_{working_py.parent.name}"
    spec   = importlib.util.spec_from_file_location(name, working_py)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _build_default_kwargs(variables: list) -> dict:
    """Build a kwargs dict from the defaults declared in define()["variables"]."""
    kwargs = {}
    for v in variables:
        if not isinstance(v, dict):
            continue
        key     = v.get("name", "")
        default = v.get("default", "")
        if key and default not in ("", None):
            kwargs[key] = default
    return kwargs


# ─────────────────────────────────────────────────────────────────────────────
# Per-component sample generation
# ─────────────────────────────────────────────────────────────────────────────

#overrides for components whose raw defaults look bad as standalone samples
_SAMPLE_OVERRIDES = {
    "oobb_plate":  {"width": 2, "height": 2, "color": "#333333"},
    "oobb_holes":  {"width": 2, "height": 2, "color": "#333333"},
    "oobb_circle": {"diameter": 3, "color": "#333333"},
    "circle":      {"r": 8.0,  "color": "#333333"},
    "slot":        {"r": 4.0, "w": 20.0, "color": "#333333"},
    "rect":        {"size": [30, 20, 3], "color": "#333333"},
    "rounded_rectangle": {"size": [30, 20, 3], "r": 4.0, "color": "#333333"},
    "polygon":     {"points": [[0, 10], [-10, -8], [10, -8]], "color": "#333333"},
    "text":        {"text": "Sample", "size": 10.0, "font": "sans-serif",
                    "halign": "center", "valign": "center", "color": "#333333"},
}


def generate_sample(component_name: str,
                    components_root: str = "svg_components",
                    force: bool = False) -> bool:
    """
    Generate sample.svg for one component. Returns True on success.
    """
    component_dir = Path(components_root) / component_name
    working_py    = component_dir / "working.py"
    sample_svg    = component_dir / "sample.svg"

    if not working_py.exists():
        print(f"  [skip] {component_name} — no working.py")
        return False

    if sample_svg.exists() and not force:
        print(f"  [exists] {component_name}")
        return True

    try:
        module = _load_module(working_py)
        meta   = module.define()
    except Exception as exc:
        print(f"  [error] {component_name} — define() failed: {exc}")
        return False

    kwargs = _build_default_kwargs(meta.get("variables", []))
    kwargs.setdefault("pos",   [0, 0, 0])
    kwargs.setdefault("color", "#333333")

    #apply per-component overrides
    overrides = _SAMPLE_OVERRIDES.get(component_name, {})
    kwargs.update(overrides)

    try:
        descriptors = module.action(**kwargs)
    except Exception as exc:
        print(f"  [error] {component_name} — action() failed: {exc}")
        return False

    if not descriptors:
        print(f"  [warn]  {component_name} — action() returned empty list")
        return False

    try:
        svg = opsvg.opsvg_get_svg(
            descriptors,
            padding  = _sv.PADDING_MM,
            fill     = "#333333",
        )
    except Exception as exc:
        print(f"  [error] {component_name} — render failed: {exc}")
        return False

    sample_svg.write_text(svg, encoding="utf-8")
    print(f"  [done]  {component_name} -> {sample_svg}")
    return True


def generate_all(components_root: str = "svg_components", force: bool = False):
    root = Path(components_root)
    if not root.is_dir():
        print(f"components root not found: {root}")
        return

    names = sorted(
        e.name for e in root.iterdir()
        if e.is_dir() and (e / "working.py").exists()
    )

    print(f"generating {len(names)} samples…")
    ok = 0
    for name in names:
        if generate_sample(name, components_root=components_root, force=force):
            ok += 1
    print(f"done — {ok}/{len(names)} samples written")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate sample SVGs for svg_components.")
    parser.add_argument("component", nargs="?", default=None,
                        help="Single component name to regenerate (omit for all).")
    parser.add_argument("--force",  action="store_true",
                        help="Overwrite existing sample.svg files.")
    parser.add_argument("--components-root", default="svg_components")
    args = parser.parse_args()

    if args.component:
        generate_sample(args.component,
                        components_root=args.components_root,
                        force=args.force)
    else:
        generate_all(components_root=args.components_root, force=args.force)
