"""
opsvg.py  —  SVG rendering pipeline, analogous to opsc.py.

Overview
--------
Converts a flat list of component dicts (produced by svg_append / svg_easy below)
into an SVG file.  The component dict format is intentionally the same as what
working_scad.py puts into p3 before calling oobb.append_full(), so porting a
part builder from SCAD → SVG is mostly a matter of:

    # SCAD:  oobb.append_full(thing, **p3)
    # SVG:   opsvg.svg_append(thing, **p3)   ← low-level, always available
    #   or:  opsvg.se(thing, **p3)           ← high-level, routes through svg_components/

Component discovery
-------------------
At import time, opsvg scans svg_components/*/working.py and builds a lookup
table (_COMPONENT_MAP) keyed by shape name and any declared aliases.

    se(thing, shape="rect", ...)   →  svg_components/rect/working.action(**kwargs)
                                       → list of dicts → svg_append each one

svg_easy() / se() falls back to svg_append() directly for any shape not found
in the map, so mixing se() and svg_append() in the same builder is safe.

Coordinate system
-----------------
OOBB uses mm, centred at the part origin, with Y increasing upward.
SVG uses px (we keep units in mm via the viewBox), with Y increasing downward.
Y values are negated during rendering to match the SVG convention.

Shape vocabulary  (type key = "positive" / "p"  or  "negative" / "n")
----------------------------------------------------------------------
  rect               – axis-aligned rectangle         size=[w, h, _]
  circle / hole      – filled circle                  r=<mm>
  slot               – capsule (semicircles + rect)   r=<mm>, w=<length mm>
  rounded_rectangle  – rect with corner radius        size=[w, h, _], r=<mm>
  polygon            – arbitrary polygon               points=[[x,y], ...]
  text               – SVG text label                  text, size, font, halign, valign
  oobb_plate         – OOBB plate footprint            width, height (in OOBB units)
  oobb_holes         – OOBB hole grid                  width, height, radius_name
  oobb_circle        – circular OOBB disc              diameter (in OOBB units)

Usage
-----
    import opsvg

    # low-level (always works, no component lookup)
    opsvg.svg_append(thing, type="positive", shape="oobb_plate", width=2, height=1, pos=[0,0,0])

    # high-level dispatcher (routes through svg_components/ if available)
    opsvg.se(thing, type="negative", shape="oobb_holes", width=2, height=1, radius_name="m6", pos=[0,0,0])

    opsvg.opsvg_make_object("parts/my_part/my_part.svg", thing["svg_components"])
"""

import copy
import importlib.util
import os
import sys

# ── attempt to use OOBB variables; fall back to hard-coded defaults ───────────
# Variable names in this OOBB project carry a mode suffix: _laser / _true / _3dpr.
# SVG output corresponds to laser-cut flat parts, so we default to _laser.
_SVG_MODE = "laser"

try:
    import oobb as _oobb
    _OSP       = _oobb.gv("osp")       # 15 mm
    _OSP_MINUS = _oobb.gv("osp_minus") # 1 mm

    def _gv(name):
        """
        Look up an OOBB variable, automatically trying the _laser suffix when
        the bare name is not found (e.g. hole_radius_m6 → hole_radius_m6_laser).
        """
        try:
            return _oobb.gv(name)
        except KeyError:
            return _oobb.gv(f"{name}_{_SVG_MODE}")

    def _hole_pos(xi, yi, w, h):
        return _oobb.get_hole_pos(xi, yi, w, h)

except Exception:
    _oobb      = None
    _OSP       = 15.0
    _OSP_MINUS = 1.0
    _HOLE_DEFAULTS = {
        "hole_radius_m6": 3.0, "hole_radius_m3": 1.8,
        "hole_radius_m4": 2.1, "hole_radius_m5": 2.7,
        "hole_radius_m2": 1.2, "osp": 15.0, "osp_minus": 1.0,
        "osp_hole": "m6",
    }

    def _gv(name):
        if name in _HOLE_DEFAULTS:
            return _HOLE_DEFAULTS[name]
        for sfx in ("_laser", "_true", "_3dpr"):
            if name.endswith(sfx):
                bare = name[: -len(sfx)]
                if bare in _HOLE_DEFAULTS:
                    return _HOLE_DEFAULTS[bare]
        raise KeyError(name)

    def _hole_pos(xi, yi, w, h):
        sp = _OSP
        return (-(w - 1) * sp / 2 + (xi - 1) * sp,
                -(h - 1) * sp / 2 + (yi - 1) * sp)


# ── visual defaults ───────────────────────────────────────────────────────────
_FILL_POSITIVE = "#333333"   # material colour
_FILL_NEGATIVE = "#ffffff"   # cut / background colour
_STROKE        = "none"
_STROKE_WIDTH  = 0
_PADDING_MM    = 5           # extra white-space around the part
_CORNER_RADIUS = 2.0         # default plate corner radius (mm)


# ─────────────────────────────────────────────────────────────────────────────
# Component discovery
# ─────────────────────────────────────────────────────────────────────────────

def _discover_components(root="svg_components"):
    """
    Scan *root*/*/working.py files, import each as a module, and build a
    shape-name → module mapping.

    Each working.py must expose:
        define()  → dict with optional "shape_aliases" key
        action(**kwargs) → list of shape-descriptor dicts

    Aliases declared in define()["shape_aliases"] are registered alongside
    the folder name so that, e.g., shape="hole" routes to the circle component.

    Discovery is relative to the directory containing opsvg.py so the import
    works regardless of the current working directory.
    """
    component_map = {}

    base_dir = os.path.dirname(os.path.abspath(__file__))
    components_dir = os.path.join(base_dir, root)

    if not os.path.isdir(components_dir):
        return component_map

    for entry in sorted(os.listdir(components_dir)):
        component_folder = os.path.join(components_dir, entry)
        working_file     = os.path.join(component_folder, "working.py")

        if not os.path.isfile(working_file):
            continue

        module_name = f"svg_components.{entry}.working"
        try:
            spec   = importlib.util.spec_from_file_location(module_name, working_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        except Exception as exc:
            print(f"[opsvg] warning: could not load {working_file}: {exc}")
            continue

        # Register by folder name
        component_map[entry] = module

        # Register any declared aliases
        try:
            meta    = module.define()
            aliases = meta.get("shape_aliases", [])
            for alias in aliases:
                component_map[alias] = module
        except Exception:
            pass

    return component_map


# Populated once at import time; available as opsvg._COMPONENT_MAP
_COMPONENT_MAP = _discover_components()


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def svg_init(thing):
    """Add the svg_components list to an existing thing dict (idempotent)."""
    if "svg_components" not in thing:
        thing["svg_components"] = []


def svg_append(thing, **kwargs):
    """
    Store a shape descriptor onto thing["svg_components"].

    This is the low-level primitive — it mirrors the role of oobb.append_full()
    in the SCAD pipeline.  Call it exactly as you would oobb.append_full(),
    just swap the function name.

    Supports multiple positions and/or multiple shapes by passing lists:
        pos=[[0,0,0], [15,0,0]]   → two copies of the shape
        shape=["rect", "circle"]  → two different shapes at the same pos

    Example
    -------
        p3 = copy.deepcopy(kwargs)
        p3["type"]  = "positive"
        p3["shape"] = "oobb_plate"
        p3["pos"]   = copy.deepcopy(pos)
        opsvg.svg_append(thing, **p3)
    """
    svg_init(thing)

    poss = kwargs.get("pos", [0, 0, 0])
    if not poss or not isinstance(poss[0], list):
        poss = [poss]

    shapes = kwargs.get("shape", "")
    if not isinstance(shapes, list):
        shapes = [shapes]

    for shape in shapes:
        for pos in poss:
            entry          = copy.deepcopy(kwargs)
            entry["shape"] = shape
            entry["pos"]   = copy.deepcopy(pos)
            thing["svg_components"].append(entry)


def svg_easy(thing, **kwargs):
    """
    High-level shape dispatcher, analogous to oobb.oobb_easy() / oe().

    Looks up kwargs["shape"] in _COMPONENT_MAP (built from svg_components/).
    If found, calls component.action(**kwargs) to get a list of shape dicts,
    then appends each via svg_append().

    Falls back to svg_append() directly when the shape is not in the map,
    so se() and svg_append() can be mixed freely in the same builder.

    Supports list values for shape and pos the same way svg_append() does.

    Example
    -------
        p3 = copy.deepcopy(kwargs)
        p3["type"]  = "positive"
        p3["shape"] = "rounded_rectangle"
        p3["size"]  = [label_width, label_height, depth]
        p3["r"]     = corner_radius
        p3["pos"]   = copy.deepcopy(pos)
        opsvg.se(thing, **p3)
    """
    svg_init(thing)

    shape_arg = kwargs.get("shape", "")
    shapes    = shape_arg if isinstance(shape_arg, list) else [shape_arg]

    poss = kwargs.get("pos", [0, 0, 0])
    if not poss or not isinstance(poss[0], list):
        poss = [poss]

    for shape in shapes:
        component = _COMPONENT_MAP.get(shape)
        if component is not None:
            for pos in poss:
                call_kwargs          = copy.deepcopy(kwargs)
                call_kwargs["shape"] = shape
                call_kwargs["pos"]   = copy.deepcopy(pos)
                try:
                    descriptors = component.action(**call_kwargs)
                except Exception as exc:
                    print(f"[opsvg] warning: {shape}.action() failed: {exc}")
                    descriptors = []
                for descriptor in (descriptors or []):
                    svg_append(thing, **descriptor)
        else:
            # Unknown shape — pass through directly so nothing is silently lost
            for pos in poss:
                call_kwargs          = copy.deepcopy(kwargs)
                call_kwargs["shape"] = shape
                call_kwargs["pos"]   = copy.deepcopy(pos)
                svg_append(thing, **call_kwargs)


# Short alias — mirrors oobb.oe()
se = svg_easy


def opsvg_make_object(filename, components,
                      scale=1.0,
                      padding=_PADDING_MM,
                      fill=_FILL_POSITIVE,
                      cut=_FILL_NEGATIVE,
                      stroke=_STROKE,
                      stroke_width=_STROKE_WIDTH,
                      overwrite=True,
                      **kwargs):
    """
    Render *components* (a list of shape dicts from svg_append / se) to an SVG file.

    Parameters
    ----------
    filename     : output path (folders are created automatically)
    components   : thing["svg_components"]
    scale        : mm-to-SVG-unit multiplier (default 1 — units stay in mm)
    padding      : whitespace around the part in mm
    fill         : colour for positive (material) shapes
    cut          : colour for negative (cutout) shapes, and background
    overwrite    : if False, skip files that already exist
    """
    if not overwrite and os.path.isfile(filename):
        print(f"svg exists, skipping: {filename}")
        return

    folder = os.path.dirname(filename)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)

    svg = opsvg_get_svg(components, scale=scale, padding=padding,
                        fill=fill, cut=cut,
                        stroke=stroke, stroke_width=stroke_width, **kwargs)

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(svg)

    print(f"saved svg: {filename}")


def opsvg_get_svg(components,
                  scale=1.0,
                  padding=_PADDING_MM,
                  fill=_FILL_POSITIVE,
                  cut=_FILL_NEGATIVE,
                  stroke=_STROKE,
                  stroke_width=_STROKE_WIDTH,
                  **kwargs):
    """
    Convert *components* to an SVG string and return it.

    The background is filled with *cut* colour; positives are drawn on top,
    then negatives are drawn over them (painter's algorithm — same approach
    as the laser DXF output in opsc.py).
    """
    flat = _flatten(components)

    positives = [c for c in flat if c.get("type", "p") in ("positive", "p")]
    negatives = [c for c in flat if c.get("type", "n") in ("negative", "n")]

    # ── bounding box ──────────────────────────────────────────────────────────
    bb   = _bounding_box(flat)
    xmin = bb["xmin"] - padding
    ymin = bb["ymin"] - padding
    xmax = bb["xmax"] + padding
    ymax = bb["ymax"] + padding
    vw   = (xmax - xmin) * scale
    vh   = (ymax - ymin) * scale

    # ── coordinate converters (OOBB mm → SVG units, Y-flipped) ───────────────
    def sx(x):
        return (x - xmin) * scale

    def sy(y):
        return (ymax - y) * scale   # flip Y

    ctx = dict(sx=sx, sy=sy, scale=scale, fill=fill, cut=cut)

    # ── render ────────────────────────────────────────────────────────────────
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg"',
        f'     width="{vw:.4f}mm" height="{vh:.4f}mm"',
        f'     viewBox="0 0 {vw:.4f} {vh:.4f}">',
        f'  <!-- background -->',
        f'  <rect x="0" y="0" width="{vw:.4f}" height="{vh:.4f}" fill="{cut}" />',
        f'  <!-- positive shapes -->',
    ]

    for comp in positives:
        elem = _render_shape(comp, ctx)
        if elem:
            lines.append(_styled(elem, fill, stroke, stroke_width))

    lines.append("  <!-- negative / cutout shapes -->")

    for comp in negatives:
        elem = _render_shape(comp, ctx)
        if elem:
            lines.append(_styled(elem, cut, stroke, stroke_width))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Shape renderers
# ─────────────────────────────────────────────────────────────────────────────

def _render_shape(comp, ctx):
    """
    Convert one component dict to a raw SVG element string.
    Returns None for unknown / 3-D-only shapes (they are silently skipped).
    """
    shape = comp.get("shape", "")
    pos   = comp.get("pos",   [0, 0, 0])
    rot   = comp.get("rot",   [0, 0, 0])
    sx    = ctx["sx"]
    sy    = ctx["sy"]
    sc    = ctx["scale"]

    cx = sx(pos[0])
    cy = sy(pos[1])
    rz = rot[2] if rot else 0        # only Z-rotation makes sense in 2-D

    def _rot_attr():
        return f' transform="rotate({-rz:.3f},{cx:.4f},{cy:.4f})"' if rz else ""

    # ── rect ─────────────────────────────────────────────────────────────────
    if shape == "rect":
        size = comp.get("size", [10, 10, 3])
        w, h = size[0] * sc, size[1] * sc
        x, y = cx - w / 2, cy - h / 2
        return f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}"{_rot_attr()} />'

    # ── circle / hole ─────────────────────────────────────────────────────────
    if shape in ("circle", "hole"):
        r = comp.get("r", comp.get("radius", 3.0)) * sc
        return f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" />'

    # ── slot (capsule) ────────────────────────────────────────────────────────
    if shape == "slot":
        r = comp.get("r", 3.0) * sc
        w = comp.get("w", comp.get("width", 10.0)) * sc
        x1, x2  = cx - w / 2, cx + w / 2
        top, bot = cy - r, cy + r
        d = (f"M {x1:.4f} {top:.4f} "
             f"A {r:.4f} {r:.4f} 0 0 0 {x1:.4f} {bot:.4f} "
             f"L {x2:.4f} {bot:.4f} "
             f"A {r:.4f} {r:.4f} 0 0 0 {x2:.4f} {top:.4f} Z")
        return f'<path d="{d}"{_rot_attr()} />'

    # ── rounded_rectangle ─────────────────────────────────────────────────────
    if shape == "rounded_rectangle":
        size = comp.get("size", [10, 10, 3])
        w, h = size[0] * sc, size[1] * sc
        r    = comp.get("r", _CORNER_RADIUS) * sc
        x, y = cx - w / 2, cy - h / 2
        return (f'<rect x="{x:.4f}" y="{y:.4f}" '
                f'width="{w:.4f}" height="{h:.4f}" '
                f'rx="{r:.4f}" ry="{r:.4f}"{_rot_attr()} />')

    # ── polygon ───────────────────────────────────────────────────────────────
    if shape == "polygon":
        pts = comp.get("points", [])
        if not pts:
            return None
        pts_str = " ".join(
            f"{sx(pos[0] + p[0]):.4f},{sy(pos[1] + p[1]):.4f}" for p in pts
        )
        return f'<polygon points="{pts_str}"{_rot_attr()} />'

    # ── text ──────────────────────────────────────────────────────────────────
    if shape == "text":
        txt     = comp.get("text", "")
        fsz     = comp.get("size", 4.0) * sc
        font    = comp.get("font", "sans-serif").split(":")[0]  # strip :style=
        _halign = {"left": "start", "center": "middle", "right": "end"}
        _valign = {"bottom": "auto", "center": "middle", "top": "hanging"}
        anchor  = _halign.get(comp.get("halign", "center"), "middle")
        base    = _valign.get(comp.get("valign", "center"), "middle")
        # color kwarg overrides the painter-algorithm fill for this element
        colour  = comp.get("color", ctx["fill"])
        return (f'<text x="{cx:.4f}" y="{cy:.4f}" '
                f'font-family="{font}" font-size="{fsz:.4f}" '
                f'text-anchor="{anchor}" dominant-baseline="{base}" '
                f'fill="{colour}"{_rot_attr()}>{txt}</text>')

    # ── oobb_plate ────────────────────────────────────────────────────────────
    if shape == "oobb_plate":
        return _oobb_plate(comp, cx, cy, rz, sc)

    # ── oobb_holes ────────────────────────────────────────────────────────────
    if shape == "oobb_holes":
        return _oobb_holes(comp, pos, ctx)

    # ── oobb_circle ───────────────────────────────────────────────────────────
    if shape == "oobb_circle":
        dia = comp.get("diameter", comp.get("dia", 1))
        osp = _gv("osp")
        r   = dia * osp / 2 * sc
        return f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" />'

    # unknown / 3-D-only shapes — silently skip
    return None


def _oobb_plate(comp, cx, cy, rz, sc):
    """Render oobb_plate as a rounded rectangle."""
    osp  = _gv("osp")
    ospm = _gv("osp_minus")
    w    = comp.get("width",  1)
    h    = comp.get("height", 1)
    r    = comp.get("corner_radius", _CORNER_RADIUS)
    w_mm = (w * osp - ospm) * sc
    h_mm = (h * osp - ospm) * sc
    r_mm = r * sc
    x, y = cx - w_mm / 2, cy - h_mm / 2
    rot_attr = f' transform="rotate({-rz:.3f},{cx:.4f},{cy:.4f})"' if rz else ""
    return (f'<rect x="{x:.4f}" y="{y:.4f}" '
            f'width="{w_mm:.4f}" height="{h_mm:.4f}" '
            f'rx="{r_mm:.4f}" ry="{r_mm:.4f}"{rot_attr} />')


def _oobb_holes(comp, pos, ctx):
    """Render oobb_holes as a <g> of circles."""
    sx   = ctx["sx"]
    sy   = ctx["sy"]
    sc   = ctx["scale"]
    w    = comp.get("width",  1)
    h    = comp.get("height", 1)

    rn = comp.get("radius_name", _gv("osp_hole"))
    try:
        r = _gv(f"hole_radius_{rn}") * sc
    except Exception:
        r = 3.0 * sc

    circles = []
    for xi in range(1, int(w) + 1):
        for yi in range(1, int(h) + 1):
            hx, hy = _hole_pos(xi, yi, w, h)
            circles.append(
                f'    <circle cx="{sx(pos[0] + hx):.4f}" '
                f'cy="{sy(pos[1] + hy):.4f}" r="{r:.4f}" />'
            )
    return "<g>\n" + "\n".join(circles) + "\n  </g>"


# ─────────────────────────────────────────────────────────────────────────────
# Bounding-box estimation
# ─────────────────────────────────────────────────────────────────────────────

def _bounding_box(components):
    """
    Return {"xmin", "xmax", "ymin", "ymax"} in OOBB mm coords.
    Falls back gracefully if shapes are unknown.
    """
    xs = [0.0]
    ys = [0.0]
    osp  = _gv("osp")
    ospm = _gv("osp_minus")

    for c in components:
        shape  = c.get("shape", "")
        pos    = c.get("pos", [0, 0, 0])
        px, py = pos[0], pos[1]

        if shape == "oobb_plate":
            w  = c.get("width", 1)
            h  = c.get("height", 1)
            hw = (w * osp - ospm) / 2
            hh = (h * osp - ospm) / 2
            xs += [px - hw, px + hw];  ys += [py - hh, py + hh]

        elif shape == "oobb_circle":
            dia = c.get("diameter", c.get("dia", 1))
            r   = dia * osp / 2
            xs += [px - r, px + r];    ys += [py - r, py + r]

        elif shape == "oobb_holes":
            xs.append(px);             ys.append(py)

        elif shape == "rect":
            size = c.get("size", [10, 10, 3])
            hw, hh = size[0] / 2, size[1] / 2
            xs += [px - hw, px + hw];  ys += [py - hh, py + hh]

        elif shape == "rounded_rectangle":
            size = c.get("size", [10, 10, 3])
            hw, hh = size[0] / 2, size[1] / 2
            xs += [px - hw, px + hw];  ys += [py - hh, py + hh]

        elif shape in ("circle", "hole"):
            r = c.get("r", c.get("radius", 3.0))
            xs += [px - r, px + r];    ys += [py - r, py + r]

        elif shape == "slot":
            r = c.get("r", 3.0)
            w = c.get("w", c.get("width", 10.0))
            xs += [px - w / 2 - r, px + w / 2 + r]
            ys += [py - r, py + r]

        elif shape == "polygon":
            for pt in c.get("points", []):
                xs.append(px + pt[0]);  ys.append(py + pt[1])

        else:
            xs.append(px);             ys.append(py)

    return {"xmin": min(xs), "xmax": max(xs),
            "ymin": min(ys), "ymax": max(ys)}


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _flatten(items, depth=8):
    """Recursively flatten nested lists of component dicts."""
    for _ in range(depth):
        flat, changed = [], False
        for item in items:
            if isinstance(item, list):
                flat.extend(item);  changed = True
            else:
                flat.append(item)
        items = flat
        if not changed:
            break
    return items


def _styled(elem, fill, stroke, stroke_width):
    """Inject fill/stroke attributes into a raw SVG element string."""
    if elem.startswith("<text"):
        return f"  {elem}"              # text carries its own fill attribute
    stroke_attr = f'stroke="{stroke}"'
    sw_attr     = f'stroke-width="{stroke_width}"' if stroke_width else ""
    attrs       = f'fill="{fill}" {stroke_attr} {sw_attr}'.strip()
    elem        = elem.rstrip()
    if elem.endswith("/>"):
        return f"  {elem[:-2]} {attrs} />"
    if elem.startswith("<g"):
        return f"  {elem[:2]} {attrs}{elem[2:]}"
    return f"  {elem}"
