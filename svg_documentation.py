"""
svg_documentation.py  —  Documentation generator for the SVG pipeline.

Crawls svg_components/*/working.py (via define()) and parts/*/working.yaml
to produce documentation_data.json and documentation.html.

Usage
-----
    python svg_documentation.py                   # HTML + JSON → project root
    python svg_documentation.py --json-only       # JSON only
    python svg_documentation.py --out docs/       # custom output folder
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalise_variables(raw: Any) -> list[dict]:
    if not isinstance(raw, list):
        return []
    result = []
    for item in raw:
        if isinstance(item, dict):
            name = _coerce_text(item.get("name"))
            if not name:
                continue
            result.append({
                "name":        name,
                "description": _coerce_text(item.get("description", "")),
                "type":        _coerce_text(item.get("type", "")),
                "default":     item.get("default", ""),
            })
        elif isinstance(item, str):
            name = item.strip()
            if name:
                result.append({"name": name, "description": "", "type": "", "default": ""})
    return result


def _load_component_module(working_py: Path):
    module_name = f"_svg_doc_component_{working_py.parent.name}"
    spec   = importlib.util.spec_from_file_location(module_name, working_py)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _read_sample_svg(component_dir: Path) -> str:
    sample = component_dir / "sample.svg"
    if sample.exists():
        return sample.read_text(encoding="utf-8").strip()
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Data extraction
# ─────────────────────────────────────────────────────────────────────────────

def get_all_components_documentation(components_root: str = "svg_components") -> list[dict]:
    """
    Crawl svg_components/*/working.py, call define() on each, return list of dicts.
    """
    root = Path(components_root)
    docs = []

    if not root.is_dir():
        return docs

    for entry in sorted(root.iterdir()):
        working_py = entry / "working.py"
        if not entry.is_dir() or not working_py.exists():
            continue

        try:
            module = _load_component_module(working_py)
            meta   = module.define()
        except Exception as exc:
            print(f"[svg_documentation] warning: could not load {working_py}: {exc}")
            continue

        docs.append({
            "name":          _coerce_text(meta.get("name",          entry.name)),
            "name_long":     _coerce_text(meta.get("name_long",     entry.name)),
            "description":   _coerce_text(meta.get("description",   "")),
            "category":      _coerce_text(meta.get("category",      "General")),
            "shape_aliases": meta.get("shape_aliases", []),
            "returns":       _coerce_text(meta.get("returns",       "")),
            "variables":     _normalise_variables(meta.get("variables", [])),
            "sample_svg":    _read_sample_svg(entry),
        })

    return docs


def get_all_parts_documentation(parts_root: str = "parts") -> list[dict]:
    """
    Crawl parts/*/working.yaml, return list of part summary dicts.
    Only includes parts that have an svg_details section.
    """
    root = Path(parts_root)
    docs = []

    if not root.is_dir():
        return docs

    for entry in sorted(root.iterdir()):
        working_yaml = entry / "working.yaml"
        if not entry.is_dir() or not working_yaml.exists():
            continue

        try:
            with open(working_yaml, encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception:
            continue

        if not isinstance(data, dict):
            continue

        svg_details = data.get("svg_details")
        if not isinstance(svg_details, dict):
            continue

        docs.append({
            "id":               _coerce_text(data.get("id",               entry.name)),
            "oobb_name":        _coerce_text(data.get("oobb_name",        "")),
            "svg_name":         _coerce_text(svg_details.get("svg_name",  "")),
            "classification":   _coerce_text(data.get("classification",   "")),
            "description_main": _coerce_text(data.get("description_main", "")),
            "size":             _coerce_text(data.get("size",             "")),
            "folder":           str(entry),
        })

    return docs


# ─────────────────────────────────────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────────────────────────────────────

def export_documentation_json(
    output_path: str | Path = "documentation_data.json",
    components_root: str = "svg_components",
    parts_root: str = "parts",
) -> dict:
    """Write documentation_data.json and return the payload dict."""
    components = get_all_components_documentation(components_root)
    parts      = get_all_parts_documentation(parts_root)

    payload = {
        "generated_date":    str(date.today()),
        "total_components":  len(components),
        "total_parts":       len(parts),
        "components":        components,
        "parts":             parts,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(f"saved json: {output_path}")
    return payload


def export_documentation_html(
    template_path: str | Path = "templates/svg_documentation_template.html",
    output_path:   str | Path = "documentation.html",
    components_root: str = "svg_components",
    parts_root: str = "parts",
) -> None:
    """Inject documentation JSON into the HTML template and write output."""
    template_path = Path(template_path)
    output_path   = Path(output_path)

    if not template_path.exists():
        print(f"[svg_documentation] template not found: {template_path}")
        return

    components = get_all_components_documentation(components_root)
    parts      = get_all_parts_documentation(parts_root)

    payload = {
        "generated_date":   str(date.today()),
        "total_components": len(components),
        "total_parts":      len(parts),
        "components":       components,
        "parts":            parts,
    }

    script_tag = (
        "<script>\n"
        "window.DOCUMENTATION_DATA = "
        + json.dumps(payload, indent=2, ensure_ascii=False, default=str)
        + ";\n</script>"
    )

    template = template_path.read_text(encoding="utf-8")
    output   = template.replace("<!-- DOCUMENTATION_DATA_PLACEHOLDER -->", script_tag)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(f"saved html: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate SVG pipeline documentation.")
    parser.add_argument("--json-only", action="store_true",
                        help="Write JSON data file only, skip HTML generation.")
    parser.add_argument("--out", default=".",
                        help="Output folder (default: project root).")
    parser.add_argument("--components-root", default="svg_components")
    parser.add_argument("--parts-root",      default="parts")
    parser.add_argument("--template",
                        default="templates/svg_documentation_template.html")
    args = parser.parse_args()

    out = Path(args.out)

    export_documentation_json(
        output_path     = out / "documentation_data.json",
        components_root = args.components_root,
        parts_root      = args.parts_root,
    )

    if not args.json_only:
        export_documentation_html(
            template_path   = args.template,
            output_path     = out / "documentation.html",
            components_root = args.components_root,
            parts_root      = args.parts_root,
        )


if __name__ == "__main__":
    main()
