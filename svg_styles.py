"""
svg_styles.py  —  Stylesheet system for the SVG pipeline.

A stylesheet is a plain dict mapping style names to property dicts.
Style names support dot-notation for variants that inherit from a base:

    "plate"        → full property dict
    "plate.accent" → only the properties that differ from "plate"

resolve("plate.accent") merges base + variant, variant wins per-property.

Usage
-----
    import svg_styles

    # Apply a named style — inline kwargs always win over style values
    opsvg.se(thing, shape="oobb_plate", style="plate",        width=2, height=2, pos=pos)
    opsvg.se(thing, shape="text",       style="header.label", text="Hello",      pos=pos)
    opsvg.se(thing, shape="text",       style="label.small",  halign="left",     pos=pos)

    # Per-part override (only list what changes)
    svg_styles.set_style(thing, "plate",  {"color": "#E85D04"})
    svg_styles.set_style(thing, "label",  {"font": "JetBrains Mono, monospace"})

    # Switch to jazzy stylesheet
    thing["styles"] = svg_styles.get_stylesheet("jazzy")

    # Mix stylesheets (custom overrides on top of jazzy)
    thing["styles"] = svg_styles.merge(
        svg_styles.get_stylesheet("jazzy"),
        {"plate": {"color": "#FF0000"}},
    )
"""

from __future__ import annotations
import copy
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Default stylesheet  — technical monochrome, burnt-orange accent
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT: dict[str, dict] = {
    # ── Plate / body geometry ────────────────────────────────────────────────
    "plate":          {"color": "#333333", "stroke": "none",    "stroke_width": 0},
    "plate.accent":   {"color": "#E85D04"},                         # burnt orange
    "plate.light":    {"color": "#888888"},                         # mid grey
    "plate.outline":  {"color": "none",    "stroke": "#333333", "stroke_width": 0.5},
    # plate + stroke weight (merges with plate fill, adds a visible border)
    "plate.hairline": {"stroke": "#333333", "stroke_width": 0.1},
    "plate.thin":     {"stroke": "#333333", "stroke_width": 0.25},
    "plate.thick":    {"stroke": "#333333", "stroke_width": 1.0},
    "plate.heavy":    {"stroke": "#333333", "stroke_width": 2.0},

    # ── Holes & slots ────────────────────────────────────────────────────────
    "hole":           {"color": "#666666", "stroke": "none",    "stroke_width": 0},
    "hole.cut":       {"color": "#FFFFFF", "stroke": "none",    "stroke_width": 0},
    "slot":           {"color": "#666666", "stroke": "none",    "stroke_width": 0},

    # ── Outline-only shapes ───────────────────────────────────────────────────
    "outline":          {"color": "none",  "stroke": "#333333", "stroke_width": 0.5},
    "outline.accent":   {"color": "none",  "stroke": "#E85D04", "stroke_width": 0.5},
    "outline.light":    {"color": "none",  "stroke": "#888888", "stroke_width": 0.3},
    # outline weight variants — inherit stroke color from base outline
    "outline.hairline": {"stroke_width": 0.1},
    "outline.thin":     {"stroke_width": 0.25},
    "outline.thick":    {"stroke_width": 1.0},
    "outline.heavy":    {"stroke_width": 2.0},

    # ── Line drawing ──────────────────────────────────────────────────────────
    # Pure stroke style for construction lines, dimensions, crosshairs, grids
    "line":           {"color": "none",    "stroke": "#333333", "stroke_width": 0.5},
    "line.accent":    {"stroke": "#E85D04"},
    "line.muted":     {"stroke": "#888888"},
    # line weight variants — inherit stroke color from base line
    "line.hairline":  {"stroke_width": 0.1},
    "line.thin":      {"stroke_width": 0.25},
    "line.thick":     {"stroke_width": 1.0},
    "line.heavy":     {"stroke_width": 2.0},

    # ── Text / labels ─────────────────────────────────────────────────────────
    "label":          {"color": "#111111", "stroke": "none",    "stroke_width": 0,
                       "font": "Inter, sans-serif", "size": 4.0,
                       "halign": "center", "valign": "center"},
    "label.small":    {"size": 2.5},
    "label.large":    {"size": 7.0},
    "label.mono":     {"font": "JetBrains Mono, Fira Code, monospace"},
    "label.light":    {"color": "#FFFFFF"},
    "label.muted":    {"color": "#666666"},
    "label.accent":   {"color": "#E85D04"},

    # ── Header bar ────────────────────────────────────────────────────────────
    "header":         {"color": "#111111", "stroke": "none",    "stroke_width": 0},
    "header.label":   {"color": "#FFFFFF", "stroke": "none",    "stroke_width": 0,
                       "font": "Inter, sans-serif", "size": 5.0,
                       "halign": "center", "valign": "center"},
    "header.accent":  {"color": "#E85D04"},

    # ── Engraved / etched ─────────────────────────────────────────────────────
    "engraved":       {"color": "#555555", "stroke": "none",    "stroke_width": 0},
    "engraved.light": {"color": "#999999"},
}


# ─────────────────────────────────────────────────────────────────────────────
# Jazzy stylesheet  — vivid purple + coral + gold palette
# ─────────────────────────────────────────────────────────────────────────────
#
# Palette:
#   #1B2869  deep navy    — base plates
#   #7B2FBE  deep purple  — headers, accents
#   #FF6B6B  coral red    — accent plates, outlines
#   #FFD60A  gold yellow  — holes, highlights, bright labels
#   #00B4D8  sky blue     — slots, cool variant
#   #4ECDC4  teal         — secondary cool
#   #C77DFF  soft purple  — engraved, glow
#   #F0E6FF  lavender wht — text on dark
#   #1B003E  deep violet  — dark text

JAZZY: dict[str, dict] = {
    # ── Plate / body geometry ────────────────────────────────────────────────
    "plate":          {"color": "#1B2869", "stroke": "none",    "stroke_width": 0},
    "plate.accent":   {"color": "#FF6B6B"},                         # coral
    "plate.pop":      {"color": "#00B4D8"},                         # sky blue
    "plate.light":    {"color": "#C8B6FF"},                         # lavender
    "plate.outline":  {"color": "none",    "stroke": "#FF6B6B", "stroke_width": 0.8},
    # plate + stroke weight (merges with plate fill, adds a visible border)
    "plate.hairline": {"stroke": "#FF6B6B", "stroke_width": 0.1},
    "plate.thin":     {"stroke": "#FF6B6B", "stroke_width": 0.25},
    "plate.thick":    {"stroke": "#FF6B6B", "stroke_width": 1.0},
    "plate.heavy":    {"stroke": "#FF6B6B", "stroke_width": 2.0},

    # ── Holes & slots ────────────────────────────────────────────────────────
    "hole":           {"color": "#FFD60A", "stroke": "none",    "stroke_width": 0},
    "hole.cut":       {"color": "#FFFFFF", "stroke": "none",    "stroke_width": 0},
    "slot":           {"color": "#4ECDC4", "stroke": "none",    "stroke_width": 0},

    # ── Outline-only shapes ───────────────────────────────────────────────────
    "outline":          {"color": "none",  "stroke": "#FF6B6B", "stroke_width": 0.6},
    "outline.accent":   {"color": "none",  "stroke": "#FFD60A", "stroke_width": 0.6},
    "outline.cool":     {"color": "none",  "stroke": "#00B4D8", "stroke_width": 0.6},
    # outline weight variants — inherit stroke color from base outline
    "outline.hairline": {"stroke_width": 0.1},
    "outline.thin":     {"stroke_width": 0.25},
    "outline.thick":    {"stroke_width": 1.0},
    "outline.heavy":    {"stroke_width": 2.0},

    # ── Line drawing ──────────────────────────────────────────────────────────
    "line":           {"color": "none",    "stroke": "#FF6B6B", "stroke_width": 0.6},
    "line.accent":    {"stroke": "#FFD60A"},                        # gold
    "line.cool":      {"stroke": "#00B4D8"},                        # sky blue
    # line weight variants — inherit stroke color from base line
    "line.hairline":  {"stroke_width": 0.1},
    "line.thin":      {"stroke_width": 0.25},
    "line.thick":     {"stroke_width": 1.0},
    "line.heavy":     {"stroke_width": 2.0},

    # ── Text / labels ─────────────────────────────────────────────────────────
    "label":          {"color": "#F0E6FF", "stroke": "none",    "stroke_width": 0,
                       "font": "Inter, sans-serif", "size": 4.0,
                       "halign": "center", "valign": "center"},
    "label.small":    {"size": 2.5},
    "label.large":    {"size": 7.0},
    "label.mono":     {"font": "JetBrains Mono, Fira Code, monospace"},
    "label.dark":     {"color": "#1B003E"},
    "label.accent":   {"color": "#FFD60A"},                         # gold
    "label.pop":      {"color": "#FF6B6B"},                         # coral

    # ── Header bar ────────────────────────────────────────────────────────────
    "header":         {"color": "#7B2FBE", "stroke": "none",    "stroke_width": 0},
    "header.label":   {"color": "#F0E6FF", "stroke": "none",    "stroke_width": 0,
                       "font": "Inter, sans-serif", "size": 5.0,
                       "halign": "center", "valign": "center"},
    "header.accent":  {"color": "#FFD60A"},                         # gold on purple

    # ── Engraved / etched ─────────────────────────────────────────────────────
    "engraved":       {"color": "#9D4EDD", "stroke": "none",    "stroke_width": 0},
    "engraved.light": {"color": "#C77DFF"},
}


# ─────────────────────────────────────────────────────────────────────────────
# Registry
# ─────────────────────────────────────────────────────────────────────────────

STYLESHEET_META: dict[str, dict] = {
    "default": {
        "label":       "Default",
        "description": (
            "Technical monochrome palette. Dark charcoal fills, single "
            "burnt-orange (#E85D04) accent. Clean, precise — designed for "
            "laser-cut technical drawings and assembly labels."
        ),
    },
    "jazzy": {
        "label":       "Jazzy",
        "description": (
            "Vivid purple-and-coral palette. Deep navy plates (#1B2869), "
            "fuchsia headers (#7B2FBE), coral accents (#FF6B6B), gold holes "
            "(#FFD60A) and sky-blue slots (#00B4D8). Bold and expressive — "
            "great for demos, art pieces, and anything that should pop."
        ),
    },
}

STYLESHEETS: dict[str, dict] = {
    "default": DEFAULT,
    "jazzy":   JAZZY,
}

# Directory scanned for *.yaml stylesheet files (sits next to this module)
STYLES_DIR: Path = Path(__file__).parent / "styles"


# ─────────────────────────────────────────────────────────────────────────────
# File-based stylesheet helpers
# ─────────────────────────────────────────────────────────────────────────────

def _load_yaml_sheet(path: Path) -> dict:
    """
    Parse a YAML stylesheet file and return the styles dict.

    File format
    -----------
    Top-level keys are style names (e.g. 'plate', 'label.small').
    The reserved key 'meta' holds human-readable metadata and is stripped.

        meta:
          name: Blueprint
          description: "Engineering drawing style."

        plate:
          color: "#0B3D91"
          stroke: "#4FC3F7"
          stroke_width: 0.3

        label:
          color: "#B3E5FC"
          font: "JetBrains Mono, monospace"
          size: 4.0
          halign: center
          valign: center
    """
    import yaml  # lazy import — yaml is a project dependency
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, dict):
        return {}
    return {k: dict(v) for k, v in raw.items()
            if k != "meta" and isinstance(v, dict)}


def _yaml_meta(path: Path) -> dict:
    """Return the 'meta' block from a YAML stylesheet file (or {})."""
    import yaml
    try:
        with open(path, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        return dict(raw.get("meta", {})) if isinstance(raw, dict) else {}
    except Exception:
        return {}


def _find_yaml(name: str, extra_dir: Path | None = None) -> Path | None:
    """Return path to <name>.yaml if it exists in extra_dir or STYLES_DIR."""
    for d in filter(None, [extra_dir, STYLES_DIR]):
        p = Path(d) / f"{name}.yaml"
        if p.exists():
            return p
    return None


def _load_single(name: str, extra_dir: Path | None = None) -> dict:
    """
    Load one stylesheet by name.  Lookup order:
      1. extra_dir/<name>.yaml   (caller-supplied directory)
      2. styles/<name>.yaml      (project styles/ folder)
      3. Built-in STYLESHEETS dict
      4. DEFAULT (fallback)
    """
    yaml_path = _find_yaml(name, extra_dir)
    if yaml_path is not None:
        try:
            return _load_yaml_sheet(yaml_path)
        except Exception as exc:
            print(f"[svg_styles] warning: could not load {yaml_path}: {exc}")
    sheet = STYLESHEETS.get(name, DEFAULT)
    return copy.deepcopy(sheet)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def get_stylesheet(
    name_or_names: "str | list[str]" = "default",
    styles_dir: "Path | str | None" = None,
) -> dict:
    """
    Return a stylesheet dict, optionally merged from multiple sources.

    Parameters
    ----------
    name_or_names : str | list[str]
        A single stylesheet name, or a list of names to merge in order.
        Later entries in the list override earlier ones (CSS-like cascade).

        Examples::

            get_stylesheet("jazzy")
            get_stylesheet(["default", "blueprint"])   # blueprint overrides default
            get_stylesheet(["jazzy", "my_overrides"])  # personal tweaks on jazzy

    styles_dir : Path | str | None
        Additional directory to search for *.yaml files before the built-in
        styles/ folder.  Useful for project-specific style libraries.

    Lookup order per name
    ---------------------
      1. styles_dir/<name>.yaml  (if styles_dir given)
      2. styles/<name>.yaml      (project styles/ folder)
      3. Built-in STYLESHEETS dict
      4. DEFAULT (last resort)

    Returns
    -------
    dict  — stylesheet ready to assign to thing["styles"]
    """
    extra = Path(styles_dir) if styles_dir else None

    if isinstance(name_or_names, (list, tuple)):
        result: dict = {}
        for name in name_or_names:
            sheet = _load_single(str(name), extra)
            result = merge(result, sheet)
        return result

    return _load_single(str(name_or_names), extra)


def list_available_stylesheets(styles_dir: "Path | str | None" = None) -> list[dict]:
    """
    Return info dicts for every known stylesheet (built-in + file-based).

    Each dict has keys: name, label, description, source ('builtin'|'file'),
    styles (the full stylesheet dict).

    File-based sheets are found in *styles_dir* (if given) and in the
    project styles/ folder.  A file-based sheet shadows a built-in of the
    same name.
    """
    found: dict[str, dict] = {}

    # Scan file system first
    search_dirs = [d for d in [styles_dir, STYLES_DIR] if d is not None]
    for d in search_dirs:
        d = Path(d)
        if not d.is_dir():
            continue
        for yaml_path in sorted(d.glob("*.yaml")):
            name = yaml_path.stem
            if name in found:
                continue   # already registered (earlier dir wins)
            try:
                meta   = _yaml_meta(yaml_path)
                styles = _load_yaml_sheet(yaml_path)
                found[name] = {
                    "name":        name,
                    "label":       meta.get("name", name.replace("_", " ").title()),
                    "description": meta.get("description", ""),
                    "source":      "file",
                    "styles":      styles,
                }
            except Exception as exc:
                print(f"[svg_styles] warning: skipping {yaml_path}: {exc}")

    # Add built-ins not already covered by a file
    for bname, sheet in STYLESHEETS.items():
        if bname in found:
            continue
        meta = STYLESHEET_META.get(bname, {})
        found[bname] = {
            "name":        bname,
            "label":       meta.get("label", bname.title()),
            "description": meta.get("description", ""),
            "source":      "builtin",
            "styles":      copy.deepcopy(sheet),
        }

    # Return in a stable order: built-ins first (default, jazzy), then files sorted
    order = list(STYLESHEETS.keys()) + sorted(
        k for k in found if k not in STYLESHEETS
    )
    return [found[k] for k in order if k in found]


def default_styles() -> dict:
    """Return a fresh copy of the DEFAULT stylesheet (convenience alias)."""
    return copy.deepcopy(DEFAULT)


def resolve(style_name: str, stylesheet: dict) -> dict:
    """
    Resolve a style name against a stylesheet, handling dot-notation variants.

    'plate'         → copy of stylesheet['plate']
    'plate.accent'  → merge(stylesheet['plate'], stylesheet['plate.accent'])
                      variant properties win over base properties.
    'unknown'       → {}

    If only the variant key exists (no matching base) the variant is returned
    as-is.  If only the base exists the base is returned.

    Parameters
    ----------
    style_name  : str   e.g. 'plate', 'plate.accent', 'header.label'
    stylesheet  : dict  active stylesheet (typically thing["styles"])

    Returns
    -------
    dict  — merged property dict (always a fresh copy, mutation-safe)
    """
    if "." in style_name:
        base_name = style_name.rsplit(".", 1)[0]
        base    = dict(stylesheet.get(base_name, {}))
        variant = dict(stylesheet.get(style_name, {}))
        return {**base, **variant}
    return dict(stylesheet.get(style_name, {}))


def merge(base: dict, overrides: dict) -> dict:
    """
    Merge two stylesheets, returning a new stylesheet.

    For each style name in *overrides*, the properties are shallow-merged
    into the matching style in *base* (override wins per-property).
    Style names not mentioned in *overrides* are preserved unchanged.
    Neither argument is mutated.

    Parameters
    ----------
    base      : dict  base stylesheet (e.g. default_styles())
    overrides : dict  partial stylesheet with only the changes

    Returns
    -------
    dict  — new merged stylesheet

    Example
    -------
        styles = svg_styles.merge(
            svg_styles.default_styles(),
            {"plate": {"color": "#E85D04"}, "label": {"size": 5.0}},
        )
    """
    result = copy.deepcopy(base)
    for name, props in overrides.items():
        result[name] = {**result.get(name, {}), **props}
    return result


def set_style(thing: dict, name: str, props: dict) -> None:
    """
    Merge *props* into one named style on thing["styles"] in-place.

    Initialises thing["styles"] from the DEFAULT stylesheet if the key is
    absent.  Only the listed properties are changed; others are preserved.

    Parameters
    ----------
    thing : dict  the active part dict (carries thing["styles"])
    name  : str   style name, e.g. 'plate', 'label.small'
    props : dict  properties to override, e.g. {"color": "#E85D04"}

    Example
    -------
        svg_styles.set_style(thing, "plate", {"color": kwargs.get("color", "#333333")})
        svg_styles.set_style(thing, "label", {"font": "JetBrains Mono, monospace"})
    """
    thing.setdefault("styles", default_styles())
    thing["styles"][name] = {**thing["styles"].get(name, {}), **props}


def apply(style_name: str, stylesheet: dict, **inline_kwargs) -> dict:
    """
    Return a kwargs dict with the named style as defaults and inline_kwargs
    overriding them.

    Equivalent to: {**resolve(style_name, stylesheet), **inline_kwargs}

    Parameters
    ----------
    style_name     : str   style to apply
    stylesheet     : dict  active stylesheet
    **inline_kwargs        explicit overrides (always win)

    Returns
    -------
    dict  — ready to splat into a shape call

    Example
    -------
        kwargs = svg_styles.apply("label.small", thing["styles"],
                                   text="v1.0", halign="right")
        opsvg.se(thing, shape="text", **kwargs, pos=pos)
    """
    resolved = resolve(style_name, stylesheet)
    return {**resolved, **inline_kwargs}
