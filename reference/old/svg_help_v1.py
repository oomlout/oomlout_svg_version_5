"""
svg_help.py  —  SVG pipeline orchestrator, analogous to scad_help.py.

Owns the full lifecycle of a single part:
  1. Build the 'thing' dict (get_default_thing)
  2. Dispatch to the builder function in working_svg.py
  3. Write output files to  parts/<id>/
       working.svg   — the SVG
       working.yaml  — kwargs only (for re-running)
       thing.yaml    — full thing dict (archive)
  4. Optionally export  working.png  and/or  working.pdf

No dependency on oobb.  Only stdlib + svg_variables + opsvg + pyyaml.
cairosvg and inkscape are optional: used for PNG/PDF export when available.

Usage
-----
    import svg_help

    # single part
    svg_help.make_svg_generic(part, save_type="all", output_formats=["png","pdf"])

    # many parts
    svg_help.make_parts(parts=get_parts(), filter="label", output_formats=["png"])
"""

import copy
import os
import sys

import yaml

import opsvg
import svg_variables as _sv


# ─────────────────────────────────────────────────────────────────────────────
# Thing dict builder  (mirrors oobb.get_default_thing)
# ─────────────────────────────────────────────────────────────────────────────

def get_default_thing(**kwargs):
    """
    Create and return the base 'thing' dict for a part.

    This mirrors oobb.get_default_thing() but has zero oobb dependency.
    Builder functions in working_svg.py populate thing["svg_components"]
    by calling opsvg.se(thing, **p3).

    Parameters accepted (all optional, sensible defaults provided)
    -----------------
    oobb_name        : str   builder function suffix (get_<oobb_name>)
    type             : str   part type string
    description      : str   human-readable name
    classification   : str   catalogue classification (default "svg")
    size             : str   size identifier for catalogue
    color            : str   colour code
    description_main : str   primary catalogue description component
    description_extra: str   secondary catalogue description component
    width            : int   OOBB-unit width  (or 1)
    height           : int   OOBB-unit height (or 1)
    depth            : float part depth in mm (or 3)
    extra            : str   extra variant tag
    """
    thing = {
        # identification
        "oobb_name":         kwargs.get("oobb_name",         ""),
        "type":              kwargs.get("type",              ""),
        "description":       kwargs.get("description",       ""),
        "classification":    kwargs.get("classification",    "svg"),
        "size":              kwargs.get("size",              ""),
        "color":             kwargs.get("color",             ""),
        "description_main":  kwargs.get("description_main",  ""),
        "description_extra": kwargs.get("description_extra", ""),

        # geometry scalars
        "width":   kwargs.get("width",  1),
        "height":  kwargs.get("height", 1),
        "depth":   kwargs.get("depth",  3),
        "extra":   kwargs.get("extra",  ""),

        # computed mm values
        "width_mm":  kwargs.get("width",  1) * _sv.OSP - _sv.OSP_MINUS,
        "height_mm": kwargs.get("height", 1) * _sv.OSP - _sv.OSP_MINUS,
        "depth_mm":  kwargs.get("depth",  3),

        # SVG component list — populated by the builder
        "svg_components": [],
    }
    return thing


# ─────────────────────────────────────────────────────────────────────────────
# ID construction  (mirrors oomp_id logic in scad_help.make_scad_generic)
# ─────────────────────────────────────────────────────────────────────────────

def id_from_part(part):
    """
    Build a filesystem-safe ID string from the part descriptor dict.

    Uses the same field priority as scad_help.py:
        classification + type + size + color + description_main + description_extra

    Falls back to oobb_name if no metadata fields are populated.
    Dots are replaced with underscores.
    """
    oomp_keys = [
        "classification", "type", "size",
        "color", "description_main", "description_extra",
    ]
    oomp_id = part.get("id", "")
    if not oomp_id:
        for key in oomp_keys:
            val = str(part.get(key, "")).replace(".", "_").strip()
            if val:
                oomp_id += f"{val}_"
        oomp_id = oomp_id.rstrip("_")
    if not oomp_id:
        oomp_id = part.get("oobb_name", "unnamed")
    return oomp_id


# ─────────────────────────────────────────────────────────────────────────────
# PNG / PDF export
# ─────────────────────────────────────────────────────────────────────────────

def _converter():
    """
    Return a string indicating which converter is available:
    "cairosvg", "inkscape", or "none".
    Cached after the first call.
    """
    if not hasattr(_converter, "_cached"):
        try:
            import cairosvg  # noqa: F401
            _converter._cached = "cairosvg"
        except ImportError:
            # Try inkscape CLI
            rc = os.system("inkscape --version >nul 2>&1" if os.name == "nt"
                           else "inkscape --version >/dev/null 2>&1")
            _converter._cached = "inkscape" if rc == 0 else "none"
    return _converter._cached


def svg_to_png(svg_path, png_path, dpi=150):
    """
    Convert an SVG file to PNG.

    Uses cairosvg if installed, otherwise falls back to the Inkscape CLI.
    Prints a warning and skips if neither is available.

    Parameters
    ----------
    svg_path : str   path to source SVG
    png_path : str   path for output PNG
    dpi      : int   output resolution (default 150)
    """
    conv = _converter()
    if conv == "cairosvg":
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, dpi=dpi)
        print(f"saved png: {png_path}")
    elif conv == "inkscape":
        cmd = (f'inkscape "{svg_path}" --export-type=png '
               f'--export-dpi={dpi} --export-filename="{png_path}"')
        os.system(cmd)
        print(f"saved png: {png_path}")
    else:
        print(
            f"[svg_help] PNG export skipped — install cairosvg or Inkscape:\n"
            f"    pip install cairosvg"
        )


def svg_to_pdf(svg_path, pdf_path):
    """
    Convert an SVG file to PDF.

    Uses cairosvg if installed, otherwise falls back to the Inkscape CLI.
    Prints a warning and skips if neither is available.

    Parameters
    ----------
    svg_path : str   path to source SVG
    pdf_path : str   path for output PDF
    """
    conv = _converter()
    if conv == "cairosvg":
        import cairosvg
        cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
        print(f"saved pdf: {pdf_path}")
    elif conv == "inkscape":
        cmd = (f'inkscape "{svg_path}" --export-type=pdf '
               f'--export-filename="{pdf_path}"')
        os.system(cmd)
        print(f"saved pdf: {pdf_path}")
    else:
        print(
            f"[svg_help] PDF export skipped — install cairosvg or Inkscape:\n"
            f"    pip install cairosvg"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Per-part pipeline  (mirrors scad_help.make_scad_generic)
# ─────────────────────────────────────────────────────────────────────────────

def make_svg_generic(part, save_type="all", overwrite=True, output_formats=None):
    """
    Full pipeline for a single part descriptor dict.

    Steps
    -----
    1. Extract oobb_name + kwargs from part.
    2. Build thing dict via get_default_thing().
    3. Dispatch to working_svg.get_<oobb_name>(thing, **kwargs).
    4. If save_type == "all":
         Write  parts/<id>/working.svg
         Write  parts/<id>/working.yaml  (kwargs — for re-running)
         Write  parts/<id>/thing.yaml    (full archive)
         If "png" in output_formats: write  parts/<id>/working.png
         If "pdf" in output_formats: write  parts/<id>/working.pdf
    5. Return thing (useful when called programmatically).

    Parameters
    ----------
    part           : dict   part descriptor (see get_parts() in working_svg.py)
    save_type      : str    "all" writes files; "none" is a dry-run
    overwrite      : bool   regenerate existing files when True
    output_formats : list   e.g. ["png", "pdf"] — additional export formats
    """
    if output_formats is None:
        output_formats = []

    oobb_name    = part.get("oobb_name",    "default")
    project_name = part.get("project_name", "svg_project")
    kwargs       = copy.deepcopy(part.get("kwargs", {}))

    # Inject type so get_default_thing builds a useful id
    kwargs["type"]      = kwargs.get("type",      f"{project_name}_{oobb_name}")
    kwargs["oobb_name"] = oobb_name

    thing = get_default_thing(**kwargs)
    thing.update(part)   # overlay any extra metadata from the descriptor

    # ── dispatch to builder ───────────────────────────────────────────────────
    # Lazy import avoids circular dependency; working_svg imports svg_help.
    import working_svg as _ws
    func = getattr(_ws, f"get_{oobb_name}", None)
    if callable(func):
        func(thing, **kwargs)
    else:
        _ws.get_default_part(thing, **kwargs)

    # ── build output folder ───────────────────────────────────────────────────
    part_id = id_from_part(part)
    folder  = os.path.join("parts", part_id)

    if save_type != "all":
        print(f"  dry-run — would write to {folder}/")
        return thing

    if not os.path.isdir(folder):
        os.makedirs(folder)

    # ── SVG ───────────────────────────────────────────────────────────────────
    svg_path = os.path.join(folder, "working.svg")
    opsvg.opsvg_make_object(svg_path, thing["svg_components"], overwrite=overwrite)

    # ── working.yaml  (kwargs only — mirrors scad_help partial dump) ──────────
    yaml_working = os.path.join(folder, "working.yaml")
    part_export  = copy.deepcopy(part)
    kwargs_export = copy.deepcopy(part_export.get("kwargs", {}))
    kwargs_export.pop("save_type", None)
    part_export["kwargs"]       = kwargs_export
    part_export["project_name"] = os.getcwd()
    part_export["id_svg"]       = part_id
    part_export.pop("thing", None)
    with open(yaml_working, "w", encoding="utf-8") as fh:
        yaml.dump(part_export, fh, allow_unicode=True)
    print(f"saved yaml: {yaml_working}")

    # ── thing.yaml  (full archive) ────────────────────────────────────────────
    yaml_thing   = os.path.join(folder, "thing.yaml")
    part_full    = copy.deepcopy(part_export)
    part_full["thing"] = _serialisable(thing)
    with open(yaml_thing, "w", encoding="utf-8") as fh:
        yaml.dump(part_full, fh, allow_unicode=True)
    print(f"saved yaml: {yaml_thing}")

    # ── optional PNG / PDF ────────────────────────────────────────────────────
    if "png" in output_formats:
        png_path = os.path.join(folder, "working.png")
        svg_to_png(svg_path, png_path)

    if "pdf" in output_formats:
        pdf_path = os.path.join(folder, "working.pdf")
        svg_to_pdf(svg_path, pdf_path)

    print(f"done {part_id}")
    return thing


# ─────────────────────────────────────────────────────────────────────────────
# Multi-part orchestrator  (mirrors scad_help.make_parts)
# ─────────────────────────────────────────────────────────────────────────────

def make_parts(**kwargs):
    """
    Build all parts in the parts list, with optional filtering.

    Parameters (all via kwargs)
    --------------------------
    parts          : list   list of part descriptor dicts
    filter         : str    only build parts whose oobb_name or extra contains this
    save_type      : str    "all" or "none"
    overwrite      : bool   default True
    output_formats : list   e.g. ["png", "pdf"]
    """
    parts          = kwargs.get("parts",          [])
    filter_str     = kwargs.get("filter",          "")
    save_type      = kwargs.get("save_type",       "all")
    overwrite      = kwargs.get("overwrite",        True)
    output_formats = kwargs.get("output_formats",   [])

    for part in parts:
        oobb_name = part.get("oobb_name", "default")
        extra     = part.get("kwargs", {}).get("extra", "")
        if filter_str and filter_str not in oobb_name and filter_str not in extra:
            print(f"skipping  {oobb_name}")
            continue
        print(f"making    {oobb_name}")
        make_svg_generic(
            part,
            save_type=save_type,
            overwrite=overwrite,
            output_formats=output_formats,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _serialisable(obj, _depth=0):
    """
    Recursively convert an object to a yaml-safe structure.
    Drops non-serialisable values rather than crashing.
    """
    if _depth > 10:
        return str(obj)
    if isinstance(obj, dict):
        return {k: _serialisable(v, _depth + 1) for k, v in obj.items()
                if not callable(v)}
    if isinstance(obj, (list, tuple)):
        return [_serialisable(i, _depth + 1) for i in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)
