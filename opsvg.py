"""
opsvg.py  —  SVG rendering pipeline, analogous to opsc.py.

No external dependencies beyond the stdlib and svg_variables.py.

Overview
--------
Converts a flat list of component dicts (produced by svg_append / svg_easy
below) into an SVG file.  The component dict format is intentionally the same
as what working_scad.py puts into p3 before calling oobb.append_full(), so
porting a part builder from SCAD → SVG is mostly a matter of:

    # SCAD:  oobb.append_full(thing, **p3)
    # SVG:   opsvg.svg_append(thing, **p3)   ← low-level, always available
    #   or:  opsvg.se(thing, **p3)           ← high-level, routes through svg_components/

Component discovery
-------------------
At import time opsvg scans svg_components/*/working.py and builds a lookup
table (_COMPONENT_MAP) keyed by shape name and any declared aliases.

    se(thing, shape="rect", ...)   →  svg_components/rect/working.action(**kwargs)
                                       → list of dicts → svg_append each one

svg_easy() / se() falls back to svg_append() directly for any shape not found
in the map, so mixing se() and svg_append() in the same builder is safe.

Coordinate system
-----------------
Part origin is at the centre, Y increasing upward (OOBB convention).
SVG origin is top-left, Y increasing downward.
opsvg auto-flips Y and computes the viewBox from the bounding box.
Units stay in mm via the SVG viewBox — no manual canvas size needed.

Shape vocabulary
----------------
  rect               – axis-aligned rectangle         size=[w, h, _]
  circle / hole      – filled circle                  r=<mm>
  slot / capsule     – capsule (semicircles + rect)   r=<mm>, w=<length mm>
  rounded_rectangle  – rect with corner radius        size=[w, h, _], r=<mm>
    aliases: rounded_rect, rrect
  polygon            – arbitrary polygon               points=[[x,y], ...]
  text / label       – SVG text label                  text, size, font, halign, valign
  oobb_plate         – OOBB plate footprint            width, height (OOBB units)
  oobb_holes         – OOBB hole grid                  width, height, radius_name
  oobb_circle        – circular OOBB disc              diameter (OOBB units)

  Each shape uses its "color" kwarg for fill; falls back to the default fill.
  Components are rendered in the order they are appended.

Usage
-----
    import opsvg

    # low-level
    opsvg.svg_append(thing, shape="oobb_plate", color="#333333",
                     width=2, height=1, pos=[0,0,0])

    # high-level dispatcher (preferred)
    opsvg.se(thing, shape="oobb_holes", color="#ffffff",
             width=2, height=1, radius_name="m6", pos=[0,0,0])

    opsvg.opsvg_make_object("parts/my_part/working.svg", thing["svg_components"])
"""

import copy
import importlib.util
import os
import sys

import svg_variables as _sv
import svg_styles as _ss

# ── constants pulled from svg_variables ───────────────────────────────────────
_OSP           = _sv.OSP
_OSP_MINUS     = _sv.OSP_MINUS
_FILL_POSITIVE = _sv.FILL_POSITIVE
_FILL_NEGATIVE = _sv.FILL_NEGATIVE
_STROKE        = _sv.STROKE
_STROKE_WIDTH  = _sv.STROKE_WIDTH
_PADDING_MM    = _sv.PADDING_MM
_CORNER_RADIUS = _sv.CORNER_RADIUS


# ── variable helpers (no oobb dependency) ─────────────────────────────────────

def _gv(name):
    """
    Look up a pipeline variable by name.
    For hole-radius names tries the bare name then strips mode suffixes.
    Raises KeyError if nothing matches.
    """
    try:
        return _sv.gv(name)
    except KeyError:
        pass
    # Treat as a hole-radius shorthand
    return _sv.hole_radius(name)


def _hole_pos(xi, yi, w, h):
    """Return (x_mm, y_mm) for hole grid position xi,yi in a w×h plate."""
    return _sv.hole_pos(xi, yi, w, h)


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
    the folder name.  Discovery is relative to the directory containing
    opsvg.py so the import works regardless of the current working directory.
    """
    component_map = {}

    base_dir       = os.path.dirname(os.path.abspath(__file__))
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

        component_map[entry] = module

        try:
            meta    = module.define()
            aliases = meta.get("shape_aliases", [])
            for alias in aliases:
                component_map[alias] = module
        except Exception:
            pass

    return component_map


# Populated once at import time
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

    Low-level primitive — mirrors oobb.append_full() in the SCAD pipeline.
    Supports list values for pos and shape to place multiple copies.

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
    High-level shape dispatcher — analogous to oobb.oobb_easy() / oe().

    Looks up kwargs["shape"] in _COMPONENT_MAP (built from svg_components/).
    If found, calls component.action(**kwargs) to get a list of shape dicts,
    then appends each via svg_append().

    Falls back to svg_append() directly for unknown shapes so se() and
    svg_append() can be freely mixed in the same builder.

    Style resolution
    ----------------
    Pass style="plate" (or any name from the active stylesheet) to apply
    a set of pre-defined properties.  Inline kwargs always override the style.

        opsvg.se(thing, shape="oobb_plate", style="plate",        width=2, height=2, pos=pos)
        opsvg.se(thing, shape="text",       style="header.label", text="Title",      pos=pos)
        opsvg.se(thing, shape="text",       style="label.small",  halign="left",     pos=pos)
    """
    svg_init(thing)

    # ── Style resolution ──────────────────────────────────────────────────────
    style_name = kwargs.pop("style", None)
    if style_name:
        stylesheet = thing.get("styles", _ss.default_styles())
        resolved   = _ss.resolve(style_name, stylesheet)
        # Style provides defaults; explicit inline kwargs always win
        for k, v in resolved.items():
            kwargs.setdefault(k, v)
    # ─────────────────────────────────────────────────────────────────────────

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
                      stroke=_STROKE,
                      stroke_width=_STROKE_WIDTH,
                      overwrite=True,
                      **kwargs):
    """
    Render *components* to an SVG file.

    Parameters
    ----------
    filename     : output path (parent folders created automatically)
    components   : thing["svg_components"]
    scale        : mm-to-SVG-unit multiplier (default 1 — stays in mm)
    padding      : whitespace around the part in mm
    fill         : default fill colour (overridden per-shape by "color" kwarg)
    overwrite    : if False, skip existing files
    """
    if not overwrite and os.path.isfile(filename):
        print(f"svg exists, skipping: {filename}")
        return

    folder = os.path.dirname(filename)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)

    svg = opsvg_get_svg(components, scale=scale, padding=padding,
                        fill=fill,
                        stroke=stroke, stroke_width=stroke_width, **kwargs)

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(svg)

    print(f"saved svg: {filename}")


def opsvg_get_svg(components,
                  scale=1.0,
                  padding=_PADDING_MM,
                  fill=_FILL_POSITIVE,
                  stroke=_STROKE,
                  stroke_width=_STROKE_WIDTH,
                  **kwargs):
    """
    Convert *components* to an SVG string and return it.

    Components are rendered in the order they are appended.
    Each component uses its "color" kwarg for fill; falls back to *fill*.
    """
    flat = _flatten(components)

    bb   = _bounding_box(flat)
    xmin = bb["xmin"] - padding
    ymin = bb["ymin"] - padding
    xmax = bb["xmax"] + padding
    ymax = bb["ymax"] + padding
    vw   = (xmax - xmin) * scale
    vh   = (ymax - ymin) * scale

    def sx(x):
        return (x - xmin) * scale

    def sy(y):
        return (ymax - y) * scale   # flip Y

    ctx = dict(sx=sx, sy=sy, scale=scale, fill=fill)

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg"',
        f'     width="{vw:.4f}mm" height="{vh:.4f}mm"',
        f'     viewBox="0 0 {vw:.4f} {vh:.4f}">',
    ]

    for comp in flat:
        elem = _render_shape(comp, ctx)
        if elem:
            comp_fill         = comp.get("color",        fill)
            comp_stroke       = comp.get("stroke",       stroke)
            comp_stroke_width = comp.get("stroke_width", stroke_width)
            lines.append(_styled(elem, comp_fill, comp_stroke, comp_stroke_width))

    lines.append("</svg>")
    return "\n".join(lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Shape renderers
# ─────────────────────────────────────────────────────────────────────────────

def _render_shape(comp, ctx):
    """Convert one component dict to a raw SVG element string."""
    shape = comp.get("shape", "")
    pos   = comp.get("pos",   [0, 0, 0])
    rot   = comp.get("rot",   [0, 0, 0])
    sx    = ctx["sx"]
    sy    = ctx["sy"]
    sc    = ctx["scale"]

    cx = sx(pos[0])
    cy = sy(pos[1])
    rz = rot[2] if rot else 0

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
    if shape in ("slot", "capsule"):
        r = comp.get("r", 3.0) * sc
        w = comp.get("w", comp.get("width", 10.0)) * sc
        x1, x2   = cx - w / 2, cx + w / 2
        top, bot = cy - r, cy + r
        d = (f"M {x1:.4f} {top:.4f} "
             f"A {r:.4f} {r:.4f} 0 0 0 {x1:.4f} {bot:.4f} "
             f"L {x2:.4f} {bot:.4f} "
             f"A {r:.4f} {r:.4f} 0 0 0 {x2:.4f} {top:.4f} Z")
        return f'<path d="{d}"{_rot_attr()} />'

    # ── rounded_rectangle ─────────────────────────────────────────────────────
    if shape in ("rounded_rectangle", "rounded_rect", "rrect"):
        size = comp.get("size", [10, 10, 3])
        w, h = size[0] * sc, size[1] * sc
        r    = comp.get("r", _CORNER_RADIUS) * sc
        x, y = cx - w / 2, cy - h / 2
        return (f'<rect x="{x:.4f}" y="{y:.4f}" '
                f'width="{w:.4f}" height="{h:.4f}" '
                f'rx="{r:.4f}" ry="{r:.4f}"{_rot_attr()} />')

    # ── rounded_rectangle_corners — per-corner radii ─────────────────────────
    # r_tl, r_tr, r_br, r_bl  (top-left, top-right, bottom-right, bottom-left)
    if shape in ("rrect_corners", "rounded_rectangle_corners"):
        size  = comp.get("size", [10, 10, 3])
        w, h  = size[0] * sc, size[1] * sc
        r_tl  = comp.get("r_tl", 0) * sc
        r_tr  = comp.get("r_tr", 0) * sc
        r_br  = comp.get("r_br", 0) * sc
        r_bl  = comp.get("r_bl", 0) * sc
        x, y  = cx - w / 2, cy - h / 2
        d = (
            f"M {x + r_tl:.4f} {y:.4f} "
            f"L {x + w - r_tr:.4f} {y:.4f} "
            f"A {r_tr:.4f} {r_tr:.4f} 0 0 1 {x + w:.4f} {y + r_tr:.4f} "
            f"L {x + w:.4f} {y + h - r_br:.4f} "
            f"A {r_br:.4f} {r_br:.4f} 0 0 1 {x + w - r_br:.4f} {y + h:.4f} "
            f"L {x + r_bl:.4f} {y + h:.4f} "
            f"A {r_bl:.4f} {r_bl:.4f} 0 0 1 {x:.4f} {y + h - r_bl:.4f} "
            f"L {x:.4f} {y + r_tl:.4f} "
            f"A {r_tl:.4f} {r_tl:.4f} 0 0 1 {x + r_tl:.4f} {y:.4f} Z"
        )
        return f'<path d="{d}"{_rot_attr()} />'

    # ── polygon ───────────────────────────────────────────────────────────────
    if shape == "polygon":
        pts = comp.get("points", [])
        if not pts:
            return None
        pts_str = " ".join(
            f"{sx(pos[0] + p[0]):.4f},{sy(pos[1] + p[1]):.4f}" for p in pts
        )
        return f'<polygon points="{pts_str}"{_rot_attr()} />'

    # ── text / label ──────────────────────────────────────────────────────────
    if shape in ("text", "label"):
        txt     = comp.get("text", "")
        fsz     = comp.get("size", 4.0) * sc
        font    = comp.get("font", "sans-serif").split(":")[0]
        _halign = {"left": "start", "center": "middle", "right": "end"}
        _valign = {"bottom": "auto", "center": "middle", "top": "hanging"}
        anchor  = _halign.get(comp.get("halign", "center"), "middle")
        base    = _valign.get(comp.get("valign", "center"), "middle")
        colour  = comp.get("color", ctx["fill"])
        weight  = comp.get("font_weight", "")
        wattr   = f' font-weight="{weight}"' if weight else ""
        return (f'<text x="{cx:.4f}" y="{cy:.4f}" '
                f'font-family="{font}" font-size="{fsz:.4f}"'
                f'{wattr} '
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
        r   = dia * _OSP / 2 * sc
        return f'<circle cx="{cx:.4f}" cy="{cy:.4f}" r="{r:.4f}" />'

    return None   # unknown / 3-D-only shape — silently skip


def _oobb_plate(comp, cx, cy, rz, sc):
    """Render oobb_plate as a rounded rectangle."""
    w     = comp.get("width",  1)
    h     = comp.get("height", 1)
    r     = comp.get("corner_radius", _CORNER_RADIUS)
    w_mm  = (w * _OSP - _OSP_MINUS) * sc
    h_mm  = (h * _OSP - _OSP_MINUS) * sc
    r_mm  = r * sc
    x, y  = cx - w_mm / 2, cy - h_mm / 2
    rot_a = f' transform="rotate({-rz:.3f},{cx:.4f},{cy:.4f})"' if rz else ""
    return (f'<rect x="{x:.4f}" y="{y:.4f}" '
            f'width="{w_mm:.4f}" height="{h_mm:.4f}" '
            f'rx="{r_mm:.4f}" ry="{r_mm:.4f}"{rot_a} />')


def _oobb_holes(comp, pos, ctx):
    """Render oobb_holes as a <g> of circles."""
    sx_fn = ctx["sx"]
    sy_fn = ctx["sy"]
    sc    = ctx["scale"]
    w     = comp.get("width",  1)
    h     = comp.get("height", 1)

    rn = comp.get("radius_name", _sv.OSP_HOLE)
    try:
        r = _sv.hole_radius(rn) * sc
    except KeyError:
        r = 3.0 * sc

    circles = []
    for xi in range(1, int(w) + 1):
        for yi in range(1, int(h) + 1):
            hx, hy = _hole_pos(xi, yi, w, h)
            circles.append(
                f'    <circle cx="{sx_fn(pos[0] + hx):.4f}" '
                f'cy="{sy_fn(pos[1] + hy):.4f}" r="{r:.4f}" />'
            )
    return "<g>\n" + "\n".join(circles) + "\n  </g>"


# ─────────────────────────────────────────────────────────────────────────────
# Bounding-box estimation
# ─────────────────────────────────────────────────────────────────────────────

def _bounding_box(components):
    """Return {"xmin","xmax","ymin","ymax"} in mm."""
    xs = [0.0]
    ys = [0.0]

    for c in components:
        shape  = c.get("shape", "")
        pos    = c.get("pos", [0, 0, 0])
        px, py = pos[0], pos[1]

        if shape == "oobb_plate":
            w  = c.get("width", 1)
            h  = c.get("height", 1)
            hw = (w * _OSP - _OSP_MINUS) / 2
            hh = (h * _OSP - _OSP_MINUS) / 2
            xs += [px - hw, px + hw];  ys += [py - hh, py + hh]

        elif shape == "oobb_circle":
            dia = c.get("diameter", c.get("dia", 1))
            r   = dia * _OSP / 2
            xs += [px - r, px + r];    ys += [py - r, py + r]

        elif shape == "oobb_holes":
            xs.append(px);             ys.append(py)

        elif shape == "rect":
            size   = c.get("size", [10, 10, 3])
            hw, hh = size[0] / 2, size[1] / 2
            xs += [px - hw, px + hw];  ys += [py - hh, py + hh]

        elif shape in ("rounded_rectangle", "rounded_rect", "rrect"):
            size   = c.get("size", [10, 10, 3])
            hw, hh = size[0] / 2, size[1] / 2
            xs += [px - hw, px + hw];  ys += [py - hh, py + hh]

        elif shape in ("circle", "hole"):
            r = c.get("r", c.get("radius", 3.0))
            xs += [px - r, px + r];    ys += [py - r, py + r]

        elif shape in ("slot", "capsule"):
            r = c.get("r", 3.0)
            w = c.get("w", c.get("width", 10.0))
            xs += [px - w / 2 - r, px + w / 2 + r]
            ys += [py - r, py + r]

        elif shape == "polygon":
            for pt in c.get("points", []):
                xs.append(px + pt[0]);  ys.append(py + pt[1])

        else:
            xs.append(px);  ys.append(py)

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
    """
    Inject fill/stroke attributes into a raw SVG element string.

    fill         : CSS colour for the shape interior ('none' = transparent)
    stroke       : CSS colour for the outline ('none' = no outline)
    stroke_width : outline width in mm (ignored when stroke is 'none')

    Three common modes
    ------------------
    Fill only  : fill='#E85D04', stroke='none'
    Outline    : fill='none',    stroke='#E85D04', stroke_width=0.5
    Both       : fill='#333333', stroke='#E85D04', stroke_width=0.3
    """
    stroke_val = stroke if stroke else "none"
    sw_attr    = f' stroke-width="{stroke_width}"' if stroke_width else ""
    attrs      = f'fill="{fill}" stroke="{stroke_val}"{sw_attr}'

    elem = elem.rstrip()

    # Text elements already embed fill= in the element; preserve them and
    # optionally splice in stroke attrs before the closing > of the opening tag.
    if elem.startswith("<text"):
        if stroke_val != "none":
            idx = elem.index(">")
            return f"  {elem[:idx]} stroke=\"{stroke_val}\"{sw_attr}{elem[idx:]}"
        return f"  {elem}"

    # Self-closing element: <rect ... />, <circle ... />, <path ... />, etc.
    if elem.endswith("/>"):
        return f"  {elem[:-2]} {attrs} />"

    # Group element: <g>\n...\n  </g>  — used by oobb_holes
    if elem.startswith("<g"):
        return f"  {elem[:2]} {attrs}{elem[2:]}"

    # Fallback — return indented as-is
    return f"  {elem}"
