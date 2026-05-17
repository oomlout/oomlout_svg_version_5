"""
working_svg.py  —  SVG part definitions, analogous to working_scad.py.

Overview
--------
Each get_<name>(thing, **kwargs) function builds a flat 2-D part by calling
opsvg.svg_append(thing, **p3) with shape descriptors that opsvg.py knows how
to render.  The pattern is deliberately identical to working_scad.py:

    SCAD:  p3["shape"] = "oobb_plate"   →  oobb.append_full(thing, **p3)
    SVG:   p3["shape"] = "oobb_plate"   →  opsvg.svg_append(thing, **p3)

Available shapes (see opsvg.py for full docs)
---------------------------------------------
  Positive / negative:  set p3["type"] = "positive" or "negative"

  rect               – axis-aligned rectangle         size=[w, h, _]
  circle / hole      – filled circle                  r=<mm>
  slot               – capsule shape                  r=<mm>, w=<length mm>
  rounded_rectangle  – rect with corner radius        size=[w, h, _], r=<mm>
  polygon            – arbitrary polygon               points=[[x,y], ...]
  text               – SVG text label                  text, size, font
  oobb_plate         – OOBB plate footprint            width, height (OOBB units)
  oobb_holes         – OOBB hole grid on osp grid     width, height, radius_name
  oobb_circle        – circular OOBB disc              diameter (OOBB units)

Usage
-----
    python working_svg.py          # generate all parts → svg_parts/
    python working_svg.py none     # dry run (no files written)
    python working_svg.py all my_part   # only parts whose name contains "my_part"
"""

import copy
import os
import sys

import opsvg

# Import oobb only for the grid-geometry helpers (gv, get_hole_pos).
# opsvg.py falls back gracefully if oobb is unavailable.
try:
    import oobb as _oobb
    _OSP  = _oobb.gv("osp")
    _OSPM = _oobb.gv("osp_minus")
except Exception:
    _oobb = None
    _OSP  = 15.0
    _OSPM = 1.0


# ─────────────────────────────────────────────────────────────────────────────
# Entry points  (mirrors working_scad.main / make_scad)
# ─────────────────────────────────────────────────────────────────────────────

def main(**kwargs):
    make_svg(**kwargs)


def make_svg(**kwargs):
    """
    Orchestrate SVG generation for all parts.
    Mirrors working_scad.make_scad().

    kwargs
    ------
    save_type : "all" (default) writes files; "none" does a dry-run
    overwrite : True (default) regenerates existing files
    filter    : only build parts whose name contains this string
    """
    save_type = kwargs.get("save_type", "all")
    overwrite  = kwargs.get("overwrite",  True)
    filt       = kwargs.get("filter",     "")

    parts = get_parts()

    for part in parts:
        name  = part.get("name", "unnamed")
        extra = part.get("kwargs", {}).get("extra", "")
        if filt and filt not in name and filt not in extra:
            print(f"skipping  {name}")
            continue
        print(f"making    {name}")
        make_svg_generic(part, save_type=save_type, overwrite=overwrite)


def get_parts():
    """
    Return the list of part descriptors to build.

    Each descriptor is a dict:
        name       – used as the output folder and file-name stem
        oobb_name  – selects the builder:  get_<oobb_name>(thing, **kwargs)
        kwargs     – forwarded to the builder function

    This mirrors the get_parts() / parts.append({}) pattern in working_scad.py.
    Add your own entries below following the same convention.
    """
    parts = []

    # ── 1 × 1 OOBB plate ─────────────────────────────────────────────────────
    parts.append({
        "name":      "plate_1x1",
        "oobb_name": "plate",
        "kwargs": {
            "width":  1,
            "height": 1,
            "depth":  3,
        },
    })

    # ── 2 × 1 OOBB plate ─────────────────────────────────────────────────────
    parts.append({
        "name":      "plate_2x1",
        "oobb_name": "plate",
        "kwargs": {
            "width":  2,
            "height": 1,
            "depth":  3,
        },
    })

    # ── 4 × 2 OOBB plate ─────────────────────────────────────────────────────
    parts.append({
        "name":      "plate_4x2",
        "oobb_name": "plate",
        "kwargs": {
            "width":  4,
            "height": 2,
            "depth":  3,
        },
    })

    # ── OOBB circle (3-unit diameter disc) ───────────────────────────────────
    parts.append({
        "name":      "circle_dia3",
        "oobb_name": "oobb_circle",
        "kwargs": {
            "diameter": 3,    # OOBB units → 3 × 15 mm = 45 mm outer diameter
            "depth":    3,
        },
    })

    # ── L-shaped bracket ─────────────────────────────────────────────────────
    parts.append({
        "name":      "bracket_4x2",
        "oobb_name": "bracket",
        "kwargs": {
            "width":  4,
            "height": 2,
            "depth":  3,
        },
    })

    # ── mounting bracket with slots ───────────────────────────────────────────
    parts.append({
        "name":      "mount_slot_2x1",
        "oobb_name": "mount_slot",
        "kwargs": {
            "width":  2,
            "height": 1,
            "depth":  3,
            "extra":  "slot",
        },
    })

    return parts


def make_svg_generic(part, save_type="all", overwrite=True):
    """
    Build a single part and (optionally) write it to an SVG file.
    Mirrors scad_help.make_scad_generic().

    Dispatches to get_<oobb_name>(thing, **kwargs) if that function exists in
    this module, otherwise falls back to get_default_part().
    """
    name      = part.get("name",      "unnamed")
    oobb_name = part.get("oobb_name", "default")
    kwargs    = copy.deepcopy(part.get("kwargs", {}))

    # ── populate a minimal 'thing' dict  (mirrors oobb.get_default_thing) ────
    thing = {
        "name":           name,
        "oobb_name":      oobb_name,
        "svg_components": [],
        "width":          kwargs.get("width",  1),
        "height":         kwargs.get("height", 1),
        "depth":          kwargs.get("depth",  3),
        "extra":          kwargs.get("extra",  ""),
    }
    thing.update(part)          # any extra metadata from the descriptor

    # ── dispatch to get_<oobb_name>() ────────────────────────────────────────
    module = sys.modules[__name__]
    func   = getattr(module, f"get_{oobb_name}", None)
    if callable(func):
        func(thing, **kwargs)
    else:
        get_default_part(thing, **kwargs)

    # ── write SVG ─────────────────────────────────────────────────────────────
    if save_type == "all":
        folder   = os.path.join("svg_parts", name)
        filename = os.path.join(folder, f"{name}.svg")
        opsvg.opsvg_make_object(
            filename,
            thing["svg_components"],
            overwrite=overwrite,
        )

    return thing   # useful when calling programmatically


# ─────────────────────────────────────────────────────────────────────────────
# Part builders
# ─────────────────────────────────────────────────────────────────────────────
# Convention (identical to working_scad.py):
#   1.  Read geometry parameters from kwargs.
#   2.  For each shape: copy kwargs → p3, set p3["type"] / p3["shape"] / p3["pos"].
#   3.  Call opsvg.svg_append(thing, **p3).
# ─────────────────────────────────────────────────────────────────────────────

def get_default_part(thing, **kwargs):
    """
    Fallback builder — plain OOBB plate with M6 holes.
    Analogous to working_scad.get_base().
    """
    pos    = kwargs.get("pos",    [0, 0, 0])
    width  = kwargs.get("width",  1)
    height = kwargs.get("height", 1)

    # ── plate body ────────────────────────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "oobb_plate"
    p3["width"]  = width
    p3["height"] = height
    p3["pos"]    = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)

    # ── M6 holes ──────────────────────────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "oobb_holes"
    p3["width"]       = width
    p3["height"]      = height
    p3["radius_name"] = "m6"
    p3["pos"]         = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)


def get_plate(thing, **kwargs):
    """
    Standard OOBB plate — outer rounded-rect body, M6 holes at every grid point.
    Parameterised by width × height in OOBB units.

    This is the direct SVG equivalent of adding an oobb_plate + oobb_holes in
    working_scad.py.
    """
    pos    = kwargs.get("pos",    [0, 0, 0])
    width  = kwargs.get("width",  1)
    height = kwargs.get("height", 1)

    # outer body
    p3 = copy.deepcopy(kwargs)
    p3["type"]  = "positive"
    p3["shape"] = "oobb_plate"
    p3["pos"]   = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)

    # holes
    p3 = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "oobb_holes"
    p3["radius_name"] = "m6"
    p3["pos"]         = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)


def get_oobb_circle(thing, **kwargs):
    """
    Circular disc sized to the OOBB grid (diameter in OOBB units).
    A centre M6 mounting hole is cut out.

    Mirrors the oobb_circle component from working_scad.py.
    """
    pos      = kwargs.get("pos",      [0, 0, 0])
    diameter = kwargs.get("diameter", 3)       # OOBB units

    # disc body
    p3 = copy.deepcopy(kwargs)
    p3["type"]     = "positive"
    p3["shape"]    = "oobb_circle"
    p3["diameter"] = diameter
    p3["pos"]      = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)

    # centre hole — use opsvg._gv which resolves _laser suffix automatically
    p3 = copy.deepcopy(kwargs)
    p3["type"]  = "negative"
    p3["shape"] = "hole"
    p3["r"]     = opsvg._gv("hole_radius_m6")
    p3["pos"]   = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)


def get_bracket(thing, **kwargs):
    """
    L-shaped bracket built from two rounded rectangles with OOBB holes.
    Demonstrates combining multiple primitives in one part, exactly as you
    would in working_scad.py using oobb.append_full multiple times.

    Layout (width=4, height=2, OOBB units):
        ╔════════════════╗
        ║  horizontal    ║   ← one-unit-tall bar spanning full width
        ╠══╗             ║
        ║  ║  vertical   ║   ← one-unit-wide bar spanning full height
        ╚══╝─────────────╝
    """
    pos    = kwargs.get("pos",    [0, 0, 0])
    width  = kwargs.get("width",  4)
    height = kwargs.get("height", 2)
    osp    = _OSP
    ospm   = _OSPM

    w_mm   = width  * osp - ospm
    h_mm   = height * osp - ospm
    arm_mm = osp - ospm           # one OOBB unit wide

    # ── horizontal bar (bottom of the L) ─────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]  = "positive"
    p3["shape"] = "rounded_rectangle"
    p3["size"]  = [w_mm, arm_mm, kwargs.get("depth", 3)]
    p3["r"]     = 2
    pos1        = copy.deepcopy(pos)
    pos1[1]    -= (h_mm - arm_mm) / 2      # shift downward
    p3["pos"]   = pos1
    opsvg.svg_append(thing, **p3)

    # ── vertical bar (left of the L) ─────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]  = "positive"
    p3["shape"] = "rounded_rectangle"
    p3["size"]  = [arm_mm, h_mm, kwargs.get("depth", 3)]
    p3["r"]     = 2
    pos1        = copy.deepcopy(pos)
    pos1[0]    -= (w_mm - arm_mm) / 2      # shift leftward
    p3["pos"]   = pos1
    opsvg.svg_append(thing, **p3)

    # ── holes on horizontal bar ───────────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "oobb_holes"
    p3["width"]       = width
    p3["height"]      = 1
    p3["radius_name"] = "m6"
    pos1              = copy.deepcopy(pos)
    pos1[1]          -= (h_mm - arm_mm) / 2
    p3["pos"]         = pos1
    opsvg.svg_append(thing, **p3)

    # ── holes on vertical bar ─────────────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "oobb_holes"
    p3["width"]       = 1
    p3["height"]      = height
    p3["radius_name"] = "m6"
    pos1              = copy.deepcopy(pos)
    pos1[0]          -= (w_mm - arm_mm) / 2
    p3["pos"]         = pos1
    opsvg.svg_append(thing, **p3)


def get_mount_slot(thing, **kwargs):
    """
    Mounting plate where the normal round holes are replaced with slots,
    allowing positional adjustment after assembly.

    Uses the 'slot' primitive — analogous to using oobb_slot in a SCAD builder.
    """
    pos    = kwargs.get("pos",    [0, 0, 0])
    width  = kwargs.get("width",  2)
    height = kwargs.get("height", 1)
    osp    = _OSP
    ospm   = _OSPM

    # ── plate body ────────────────────────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]  = "positive"
    p3["shape"] = "oobb_plate"
    p3["pos"]   = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)

    # ── slots  (one per grid column, spanning one OOBB unit vertically) ───────
    slot_r   = opsvg._gv("hole_radius_m6")
    slot_len = osp * 0.5     # slot travel distance in mm

    try:
        import oobb as _o
        col_positions = [
            _o.get_hole_pos(xi, 1, width, height)
            for xi in range(1, int(width) + 1)
        ]
    except Exception:
        # manual fallback
        col_positions = [
            (-(width - 1) * osp / 2 + (xi - 1) * osp, 0)
            for xi in range(1, int(width) + 1)
        ]

    for hx, hy in col_positions:
        p3 = copy.deepcopy(kwargs)
        p3["type"]  = "negative"
        p3["shape"] = "slot"
        p3["r"]     = slot_r
        p3["w"]     = slot_len
        p3["rot"]   = [0, 0, 90]       # vertical slots
        pos1        = copy.deepcopy(pos)
        pos1[0]    += hx
        pos1[1]    += hy
        p3["pos"]   = pos1
        opsvg.svg_append(thing, **p3)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    kw = {}
    args = sys.argv[1:]
    # first positional arg = save_type  ("all" or "none")
    if args:
        kw["save_type"] = args[0]
    # second positional arg = filter string
    if len(args) > 1:
        kw["filter"] = args[1]
    main(**kw)
