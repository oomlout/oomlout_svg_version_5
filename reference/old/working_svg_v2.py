"""
working_svg.py  —  SVG part definitions, analogous to working_scad.py.

Overview
--------
Each get_<name>(thing, **kwargs) function builds a flat 2-D part by calling
opsvg.se(thing, **p3) with shape descriptors that opsvg.py knows how to render.
The pattern is deliberately identical to working_scad.py:

    SCAD:  p3["shape"] = "oobb_plate"   →  oobb.append_full(thing, **p3)
    SVG:   p3["shape"] = "oobb_plate"   →  opsvg.se(thing, **p3)

se() routes through the svg_components/ discovery system so every shape is
self-documenting.  For shapes not in the component map, se() falls back to
svg_append() automatically.

Available shapes (see opsvg.py and svg_components/ for full docs)
-----------------------------------------------------------------
  Positive / negative:  set p3["type"] = "positive" or "negative"

  rect               – axis-aligned rectangle         size=[w, h, _]
  circle / hole      – filled circle                  r=<mm>
  slot / capsule     – capsule shape                  r=<mm>, w=<length mm>
  rounded_rectangle  – rect with corner radius        size=[w, h, _], r=<mm>
    aliases: rounded_rect, rrect
  polygon            – arbitrary polygon               points=[[x,y], ...]
  text / label       – SVG text label                  text, size, font
  oobb_plate         – OOBB plate footprint            width, height (OOBB units)
  oobb_holes         – OOBB hole grid on osp grid     width, height, radius_name
  oobb_circle        – circular OOBB disc              diameter (OOBB units)

Usage
-----
    python working_svg.py          # generate all parts → svg_parts/
    python working_svg.py none     # dry run (no files written)
    python working_svg.py all label   # only parts whose name contains "label"
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
    Orchestrate SVG generation for all parts (or a filtered subset).

    kwargs
    ------
    save_type : "all" (default) writes SVG files; "none" does a dry-run
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
    """
    parts = []

    # ── A4 demo sheet  (210 × 297 mm) ────────────────────────────────────────
    # Demonstrates every generic SVG shape: rect, rounded_rectangle, circle,
    # slot, polygon, and multiple text labels.
    parts.append({
        "name":      "a4_sheet",
        "oobb_name": "a4_sheet",
        "kwargs": {
            "depth": 3,
        },
    })

    # ── Avery / Dymo label  (76.2 × 50.4 mm) ─────────────────────────────────
    # Demonstrates a real-world tight layout: header bar, body text, bullet
    # mark, and a footer part-number strip.
    parts.append({
        "name":      "label_76x50",
        "oobb_name": "label_76x50",
        "kwargs": {
            "depth": 3,
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
    thing.update(part)

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
# Default / fallback builder
# ─────────────────────────────────────────────────────────────────────────────

def get_default_part(thing, **kwargs):
    """
    Fallback builder — plain OOBB plate with M6 holes.
    Used when no get_<oobb_name> function exists for the requested part.
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
    opsvg.se(thing, **p3)

    # ── M6 mounting holes ─────────────────────────────────────────────────────
    p3 = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "oobb_holes"
    p3["width"]       = width
    p3["height"]      = height
    p3["radius_name"] = "m6"
    p3["pos"]         = copy.deepcopy(pos)
    opsvg.se(thing, **p3)


# ─────────────────────────────────────────────────────────────────────────────
# Part builders
# ─────────────────────────────────────────────────────────────────────────────
# Convention (identical to working_scad.py):
#   1.  Read geometry parameters from kwargs.
#   2.  For each shape: copy kwargs → p3, set p3["type"] / p3["shape"] / p3["pos"].
#   3.  Call opsvg.se(thing, **p3).
# ─────────────────────────────────────────────────────────────────────────────

def get_a4_sheet(thing, **kwargs):
    """
    A4 demo sheet — 210 × 297 mm landscape, origin at the sheet centre.

    Demonstrates every generic SVG shape:
        rect               – full A4 background
        rounded_rectangle  – inset content area
        circle             – decorative corner punch-out (negative)
        slot               – horizontal adjustment slot near the bottom (negative)
        polygon            – small upward-pointing triangle marker
        text               – title, subtitle, and corner version label

    The sheet uses the painter algorithm:
        positives (background, inset box, triangle) drawn first in dark fill.
        negatives (corner circle, slot) cut through in background colour.
        text is always rendered last in the painter pass it belongs to.
    """
    pos = kwargs.get("pos", [0, 0, 0])

    sheet_width  = 210.0   # mm  A4 short edge
    sheet_height = 297.0   # mm  A4 long edge

    content_inset        = 10.0   # mm inset from each edge for the content area
    content_width        = sheet_width  - 2 * content_inset
    content_height       = sheet_height - 2 * content_inset
    content_corner_radius = 5.0   # mm

    corner_punch_radius  = 4.0    # mm  corner decorative hole
    corner_punch_offset  = 20.0   # mm  from centre to punch centre

    slot_end_cap_radius  = 3.0    # mm
    slot_travel_length   = 40.0   # mm  centre-to-centre
    slot_y_from_centre   = -(sheet_height / 2) + 20.0   # near bottom edge

    triangle_half_base   = 6.0    # mm
    triangle_height      = 8.0    # mm
    triangle_x           = (sheet_width / 2) - 20.0   # near right edge
    triangle_y           = (sheet_height / 2) - 20.0  # near top edge

    title_text           = "A4 Demo Sheet"
    title_font_size      = 14.0   # mm
    title_y              = (sheet_height / 2) - 30.0  # below top edge

    subtitle_text        = "oomlout SVG pipeline"
    subtitle_font_size   = 7.0    # mm
    subtitle_y           = title_y - title_font_size - 4.0

    version_text         = "v1.0"
    version_font_size    = 4.0    # mm
    version_x            = (sheet_width / 2) - 8.0
    version_y            = -(sheet_height / 2) + 8.0

    depth = kwargs.get("depth", 3)

    # ── full A4 background rectangle ──────────────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "rect"
    p3["size"]   = [sheet_width, sheet_height, depth]
    p3["pos"]    = copy.deepcopy(pos)
    opsvg.se(thing, **p3)

    # ── inset content area (rounded rectangle) ────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "rounded_rectangle"
    p3["size"]   = [content_width, content_height, depth]
    p3["r"]      = content_corner_radius
    p3["pos"]    = copy.deepcopy(pos)
    opsvg.se(thing, **p3)

    # ── title text ────────────────────────────────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "text"
    p3["text"]   = title_text
    p3["size"]   = title_font_size
    p3["font"]   = "sans-serif"
    p3["halign"] = "center"
    p3["valign"] = "center"
    p3["color"]  = "#ffffff"
    title_pos    = copy.deepcopy(pos)
    title_pos[1] = pos[1] + title_y
    p3["pos"]    = title_pos
    opsvg.se(thing, **p3)

    # ── subtitle text ─────────────────────────────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "text"
    p3["text"]   = subtitle_text
    p3["size"]   = subtitle_font_size
    p3["font"]   = "sans-serif"
    p3["halign"] = "center"
    p3["valign"] = "center"
    p3["color"]  = "#ffffff"
    subtitle_pos    = copy.deepcopy(pos)
    subtitle_pos[1] = pos[1] + subtitle_y
    p3["pos"]       = subtitle_pos
    opsvg.se(thing, **p3)

    # ── version label (bottom-right corner) ───────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "text"
    p3["text"]   = version_text
    p3["size"]   = version_font_size
    p3["font"]   = "sans-serif"
    p3["halign"] = "right"
    p3["valign"] = "center"
    p3["color"]  = "#ffffff"
    version_pos    = copy.deepcopy(pos)
    version_pos[0] = pos[0] + version_x
    version_pos[1] = pos[1] + version_y
    p3["pos"]      = version_pos
    opsvg.se(thing, **p3)

    # ── triangle marker (top-right area) ─────────────────────────────────────
    p3            = copy.deepcopy(kwargs)
    p3["type"]    = "positive"
    p3["shape"]   = "polygon"
    p3["points"]  = [
        [0,                   triangle_height / 2],    # apex
        [-triangle_half_base, -triangle_height / 2],   # bottom-left
        [ triangle_half_base, -triangle_height / 2],   # bottom-right
    ]
    triangle_pos    = copy.deepcopy(pos)
    triangle_pos[0] = pos[0] + triangle_x
    triangle_pos[1] = pos[1] + triangle_y
    p3["pos"]       = triangle_pos
    opsvg.se(thing, **p3)

    # ── corner decorative punch-out (negative circle) ─────────────────────────
    p3        = copy.deepcopy(kwargs)
    p3["type"]  = "negative"
    p3["shape"] = "circle"
    p3["r"]     = corner_punch_radius
    punch_pos    = copy.deepcopy(pos)
    punch_pos[0] = pos[0] - corner_punch_offset
    punch_pos[1] = pos[1] + corner_punch_offset
    p3["pos"]    = punch_pos
    opsvg.se(thing, **p3)

    # ── horizontal adjustment slot (negative) ─────────────────────────────────
    p3          = copy.deepcopy(kwargs)
    p3["type"]  = "negative"
    p3["shape"] = "slot"
    p3["r"]     = slot_end_cap_radius
    p3["w"]     = slot_travel_length
    slot_pos    = copy.deepcopy(pos)
    slot_pos[1] = pos[1] + slot_y_from_centre
    p3["pos"]   = slot_pos
    opsvg.se(thing, **p3)


def get_label_76x50(thing, **kwargs):
    """
    Standard 76.2 × 50.4 mm label  (Avery / Dymo compatible footprint).
    Origin at the label centre.

    Layout (top → bottom):
        rounded_rectangle   full label outline
        rect                solid dark header bar (top ~12 mm)
        text                "OOMLOUT" title inside the header bar (white)
        circle              small bullet mark left of the first body line
        text                part name row
        text                description row
        text                part-number / footer strip (bottom-right, small)

    The header bar is a positive rect drawn over the background — it forms a
    dark band.  The title text uses color="#ffffff" so it reads against the bar.
    Body text uses the default fill colour (dark on white).
    """
    pos = kwargs.get("pos", [0, 0, 0])

    label_width          = 76.2   # mm
    label_height         = 50.4   # mm
    label_corner_radius  = 3.0    # mm

    header_height        = 12.0   # mm
    header_y             = (label_height / 2) - (header_height / 2)
    # header rect is centred at (0, header_y) relative to label centre

    header_title_text    = "OOMLOUT"
    header_title_size    = 9.0    # mm
    header_title_y       = header_y   # vertically centred in header bar

    bullet_radius        = 1.5    # mm
    bullet_x             = -(label_width / 2) + 8.0
    body_row_1_y         = header_y - header_height - 4.0
    bullet_y             = body_row_1_y

    part_name_text       = "Bracket  4 × 2"
    part_name_size       = 5.0    # mm
    part_name_x          = bullet_x + bullet_radius + 3.0
    part_name_y          = body_row_1_y

    description_text     = "L-shaped laser-cut plate"
    description_size     = 4.0    # mm
    description_x        = -(label_width / 2) + 6.0
    description_y        = part_name_y - part_name_size - 3.0

    part_number_text     = "OOBB-BKT-4x2-001"
    part_number_size     = 3.0    # mm
    part_number_x        = (label_width / 2) - 4.0
    part_number_y        = -(label_height / 2) + 5.0

    depth = kwargs.get("depth", 3)

    # ── full label outline (rounded rectangle) ────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "rounded_rectangle"
    p3["size"]   = [label_width, label_height, depth]
    p3["r"]      = label_corner_radius
    p3["pos"]    = copy.deepcopy(pos)
    opsvg.se(thing, **p3)

    # ── header bar (solid dark rect across the top) ───────────────────────────
    p3            = copy.deepcopy(kwargs)
    p3["type"]    = "positive"
    p3["shape"]   = "rect"
    p3["size"]    = [label_width, header_height, depth]
    header_pos    = copy.deepcopy(pos)
    header_pos[1] = pos[1] + header_y
    p3["pos"]     = header_pos
    opsvg.se(thing, **p3)

    # ── header title text ("OOMLOUT" in white) ────────────────────────────────
    p3             = copy.deepcopy(kwargs)
    p3["type"]     = "positive"
    p3["shape"]    = "text"
    p3["text"]     = header_title_text
    p3["size"]     = header_title_size
    p3["font"]     = "sans-serif"
    p3["halign"]   = "center"
    p3["valign"]   = "center"
    p3["color"]    = "#ffffff"
    title_pos      = copy.deepcopy(pos)
    title_pos[1]   = pos[1] + header_title_y
    p3["pos"]      = title_pos
    opsvg.se(thing, **p3)

    # ── bullet mark (small filled circle) ────────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "negative"
    p3["shape"]  = "circle"
    p3["r"]      = bullet_radius
    bullet_pos   = copy.deepcopy(pos)
    bullet_pos[0] = pos[0] + bullet_x
    bullet_pos[1] = pos[1] + bullet_y
    p3["pos"]    = bullet_pos
    opsvg.se(thing, **p3)

    # ── part name text (body row 1) ───────────────────────────────────────────
    p3              = copy.deepcopy(kwargs)
    p3["type"]      = "negative"
    p3["shape"]     = "text"
    p3["text"]      = part_name_text
    p3["size"]      = part_name_size
    p3["font"]      = "sans-serif"
    p3["halign"]    = "left"
    p3["valign"]    = "center"
    part_name_pos   = copy.deepcopy(pos)
    part_name_pos[0] = pos[0] + part_name_x
    part_name_pos[1] = pos[1] + part_name_y
    p3["pos"]       = part_name_pos
    opsvg.se(thing, **p3)

    # ── description text (body row 2) ─────────────────────────────────────────
    p3                = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "text"
    p3["text"]        = description_text
    p3["size"]        = description_size
    p3["font"]        = "sans-serif"
    p3["halign"]      = "left"
    p3["valign"]      = "center"
    description_pos   = copy.deepcopy(pos)
    description_pos[0] = pos[0] + description_x
    description_pos[1] = pos[1] + description_y
    p3["pos"]         = description_pos
    opsvg.se(thing, **p3)

    # ── part-number footer (bottom-right, small text) ─────────────────────────
    p3               = copy.deepcopy(kwargs)
    p3["type"]       = "negative"
    p3["shape"]      = "text"
    p3["text"]       = part_number_text
    p3["size"]       = part_number_size
    p3["font"]       = "sans-serif"
    p3["halign"]     = "right"
    p3["valign"]     = "center"
    part_number_pos   = copy.deepcopy(pos)
    part_number_pos[0] = pos[0] + part_number_x
    part_number_pos[1] = pos[1] + part_number_y
    p3["pos"]        = part_number_pos
    opsvg.se(thing, **p3)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    kw   = {}
    args = sys.argv[1:]
    # first positional arg  = save_type  ("all" or "none")
    if args:
        kw["save_type"] = args[0]
    # second positional arg = filter string
    if len(args) > 1:
        kw["filter"] = args[1]
    main(**kw)
