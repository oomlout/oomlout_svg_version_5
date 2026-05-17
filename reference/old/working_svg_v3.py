"""
working_svg.py  —  SVG part definitions, analogous to working_scad.py.

Overview
--------
Each get_<name>(thing, **kwargs) function builds a flat 2-D part by calling
opsvg.se(thing, **p3) with shape descriptors that opsvg.py renders to SVG.

The pattern is deliberately identical to working_scad.py:

    SCAD:  p3["shape"] = "oobb_plate"   →  oobb.append_full(thing, **p3)
    SVG:   p3["shape"] = "oobb_plate"   →  opsvg.se(thing, **p3)

Orchestration is handled by svg_help.make_parts() / make_svg_generic(),
which writes output to:

    parts/<id>/working.svg     — SVG file
    parts/<id>/working.yaml    — kwargs (for re-running)
    parts/<id>/thing.yaml      — full thing dict

Optional PNG and PDF exports are triggered via CLI flags (see below).

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
    python working_svg.py                      # all parts → parts/
    python working_svg.py none                 # dry run
    python working_svg.py all label            # only parts matching "label"
    python working_svg.py all label png        # + PNG export
    python working_svg.py all label png pdf    # + PNG and PDF export
    python working_svg.py all "" png pdf       # all parts + PNG + PDF

CLI argument order
------------------
  argv[1]  save_type      "all" (default) or "none"
  argv[2]  filter         substring to match against oobb_name / extra ("" = no filter)
  argv[3+] output_formats any of "png", "pdf"
"""

import copy
import sys

import opsvg
import svg_help
import svg_variables as sv


# ─────────────────────────────────────────────────────────────────────────────
# Entry points  (mirrors working_scad.py main / make_scad)
# ─────────────────────────────────────────────────────────────────────────────

def main(**kwargs):
    make_svg(**kwargs)


def make_svg(**kwargs):
    """
    Orchestrate SVG generation for all (or filtered) parts.

    kwargs
    ------
    save_type      : "all" (default) writes files; "none" dry-run
    overwrite      : True (default) regenerates existing files
    filter         : only build parts whose oobb_name / extra contains this
    output_formats : list of additional formats, e.g. ["png", "pdf"]
    """
    save_type      = kwargs.get("save_type",      "all")
    overwrite      = kwargs.get("overwrite",       True)
    filter_str     = kwargs.get("filter",          "")
    output_formats = kwargs.get("output_formats",  [])

    svg_help.make_parts(
        parts=get_parts(),
        filter=filter_str,
        save_type=save_type,
        overwrite=overwrite,
        output_formats=output_formats,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Part registry  (mirrors working_scad.py get_parts)
# ─────────────────────────────────────────────────────────────────────────────

def get_parts():
    """
    Return the list of part descriptor dicts to build.

    Each descriptor mirrors the working_scad.py format exactly:
        oobb_name        – selects builder: get_<oobb_name>(thing, **kwargs)
        project_name     – project tag used in the ID
        classification   – catalogue field (e.g. "svg")
        type             – part type string
        size             – size identifier
        color            – colour code
        description_main – primary catalogue label
        description_extra– secondary catalogue label
        kwargs           – forwarded to the builder function

    The parts/<id>/ folder name is built from:
        classification_type_size_color_description_main_description_extra
    """
    parts = []

    # ── A4 demo sheet  (210 × 297 mm) ────────────────────────────────────────
    # Demonstrates every generic SVG shape: rect, rounded_rectangle, circle,
    # slot, polygon, and multiple text labels in the painter-algorithm style.
    parts.append({
        "oobb_name":         "a4_sheet",
        "project_name":      "svg_demo",
        "classification":    "svg",
        "type":              "demo",
        "size":              "a4",
        "color":             "",
        "description_main":  "a4_sheet",
        "description_extra": "",
        "kwargs": {
            "depth":     3,
            "save_type": "all",
            "overwrite": True,
        },
    })

    # ── Avery / Dymo label  (76.2 × 50.4 mm) ─────────────────────────────────
    # Demonstrates a real-world tight layout: dark header bar, white title,
    # body text, bullet mark, and part-number footer.
    parts.append({
        "oobb_name":         "label_76x50",
        "project_name":      "svg_demo",
        "classification":    "svg",
        "type":              "label",
        "size":              "76x50",
        "color":             "",
        "description_main":  "label_76x50",
        "description_extra": "",
        "kwargs": {
            "depth":     3,
            "save_type": "all",
            "overwrite": True,
        },
    })

    return parts


# ─────────────────────────────────────────────────────────────────────────────
# Default / fallback builder
# ─────────────────────────────────────────────────────────────────────────────

def get_default_part(thing, **kwargs):
    """
    Fallback builder — plain OOBB plate with M6 holes.
    Called when no get_<oobb_name> function exists for the requested part.
    Mirrors working_scad.get_base().
    """
    pos    = kwargs.get("pos",    [0, 0, 0])
    width  = kwargs.get("width",  1)
    height = kwargs.get("height", 1)

    # ── plate body ────────────────────────────────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "oobb_plate"
    p3["width"]  = width
    p3["height"] = height
    p3["pos"]    = copy.deepcopy(pos)
    opsvg.se(thing, **p3)

    # ── M6 mounting holes ─────────────────────────────────────────────────────
    p3                = copy.deepcopy(kwargs)
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
#   2.  For each shape:
#           p3 = copy.deepcopy(kwargs)
#           p3["type"]  = "positive" or "negative"
#           p3["shape"] = <shape name>
#           p3["pos"]   = copy.deepcopy(pos)
#           opsvg.se(thing, **p3)
# ─────────────────────────────────────────────────────────────────────────────

def get_a4_sheet(thing, **kwargs):
    """
    A4 demo sheet — 210 × 297 mm, origin at the sheet centre.

    Demonstrates every generic SVG shape:

        rect               full A4 background plate
        rounded_rectangle  inset content area (r=5)
        circle             decorative corner punch-out  (negative)
        slot               horizontal adjustment slot near bottom  (negative)
        polygon            small upward-pointing triangle marker
        text               title, subtitle, and corner version label

    Positive shapes are drawn first (dark fill), then negatives cut through
    in background colour.  Text uses the color= kwarg to force white on dark.
    """
    pos = kwargs.get("pos", [0, 0, 0])

    # ── geometry parameters ───────────────────────────────────────────────────
    sheet_width   = 210.0   # mm  A4 short edge
    sheet_height  = 297.0   # mm  A4 long edge

    content_inset         = 10.0   # mm  inset from each edge
    content_width         = sheet_width  - 2 * content_inset
    content_height        = sheet_height - 2 * content_inset
    content_corner_radius = 5.0    # mm

    corner_punch_radius   = 4.0    # mm  decorative negative circle
    corner_punch_x        = -(sheet_width  / 2 - 20.0)
    corner_punch_y        =   sheet_height / 2 - 20.0

    slot_end_cap_radius   = 3.0    # mm
    slot_travel_length    = 40.0   # mm  centre-to-centre
    slot_y                = -(sheet_height / 2 - 20.0)

    triangle_half_base    = 6.0    # mm
    triangle_height_mm    = 8.0    # mm
    triangle_x            =  sheet_width  / 2 - 20.0
    triangle_y            =  sheet_height / 2 - 20.0

    title_text            = "A4 Demo Sheet"
    title_font_size       = 14.0
    title_y               =  sheet_height / 2 - 30.0

    subtitle_text         = "oomlout SVG pipeline"
    subtitle_font_size    = 7.0
    subtitle_y            = title_y - title_font_size - 4.0

    version_text          = "v1.0"
    version_font_size     = 4.0
    version_x             =  sheet_width  / 2 - 8.0
    version_y             = -(sheet_height / 2 - 8.0)

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
    p3              = copy.deepcopy(kwargs)
    p3["type"]      = "positive"
    p3["shape"]     = "text"
    p3["text"]      = subtitle_text
    p3["size"]      = subtitle_font_size
    p3["font"]      = "sans-serif"
    p3["halign"]    = "center"
    p3["valign"]    = "center"
    p3["color"]     = "#ffffff"
    subtitle_pos    = copy.deepcopy(pos)
    subtitle_pos[1] = pos[1] + subtitle_y
    p3["pos"]       = subtitle_pos
    opsvg.se(thing, **p3)

    # ── version label (bottom-right corner) ───────────────────────────────────
    p3             = copy.deepcopy(kwargs)
    p3["type"]     = "positive"
    p3["shape"]    = "text"
    p3["text"]     = version_text
    p3["size"]     = version_font_size
    p3["font"]     = "sans-serif"
    p3["halign"]   = "right"
    p3["valign"]   = "center"
    p3["color"]    = "#ffffff"
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
        [0,                    triangle_height_mm / 2],
        [-triangle_half_base, -triangle_height_mm / 2],
        [ triangle_half_base, -triangle_height_mm / 2],
    ]
    triangle_pos    = copy.deepcopy(pos)
    triangle_pos[0] = pos[0] + triangle_x
    triangle_pos[1] = pos[1] + triangle_y
    p3["pos"]       = triangle_pos
    opsvg.se(thing, **p3)

    # ── corner decorative punch-out (negative circle) ─────────────────────────
    p3            = copy.deepcopy(kwargs)
    p3["type"]    = "negative"
    p3["shape"]   = "circle"
    p3["r"]       = corner_punch_radius
    punch_pos     = copy.deepcopy(pos)
    punch_pos[0]  = pos[0] + corner_punch_x
    punch_pos[1]  = pos[1] + corner_punch_y
    p3["pos"]     = punch_pos
    opsvg.se(thing, **p3)

    # ── horizontal adjustment slot (negative) ─────────────────────────────────
    p3          = copy.deepcopy(kwargs)
    p3["type"]  = "negative"
    p3["shape"] = "slot"
    p3["r"]     = slot_end_cap_radius
    p3["w"]     = slot_travel_length
    slot_pos    = copy.deepcopy(pos)
    slot_pos[1] = pos[1] + slot_y
    p3["pos"]   = slot_pos
    opsvg.se(thing, **p3)


def get_label_76x50(thing, **kwargs):
    """
    Standard 76.2 × 50.4 mm label  (Avery / Dymo compatible footprint).
    Origin at the label centre.

    Layout (top → bottom):
        rounded_rectangle   full label outline (r=3)
        rect                solid dark header bar  (~top 12 mm)
        text                "OOMLOUT" title inside header  (white)
        circle              small bullet mark left of body text  (negative)
        text                part name row
        text                description row
        text                part-number footer strip  (bottom-right, small)

    The header bar is a positive rect that paints over the white background,
    creating a dark band.  The title uses color="#ffffff" to read against it.
    Body text is rendered as negative so it appears white-on-dark when the
    label outline provides the dark background, matching real label printers.
    """
    pos = kwargs.get("pos", [0, 0, 0])

    # ── geometry parameters ───────────────────────────────────────────────────
    label_width          = 76.2    # mm  standard label short edge
    label_height         = 50.4    # mm  standard label long edge
    label_corner_radius  = 3.0     # mm

    header_height        = 12.0    # mm  dark header band
    header_centre_y      = label_height / 2 - header_height / 2

    header_title_text    = "OOMLOUT"
    header_title_size    = 9.0     # mm

    bullet_radius        = 1.5     # mm
    bullet_x             = -(label_width / 2 - 8.0)
    body_row_1_y         = header_centre_y - header_height - 4.0

    part_name_text       = "Bracket  4 × 2"
    part_name_size       = 5.0     # mm
    part_name_x          = bullet_x + bullet_radius + 3.0

    description_text     = "L-shaped laser-cut plate"
    description_size     = 4.0     # mm
    description_x        = -(label_width / 2 - 6.0)
    description_y        = body_row_1_y - part_name_size - 3.0

    part_number_text     = "OOBB-BKT-4x2-001"
    part_number_size     = 3.0     # mm
    part_number_x        = label_width / 2 - 4.0
    part_number_y        = -(label_height / 2 - 5.0)

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
    header_pos[1] = pos[1] + header_centre_y
    p3["pos"]     = header_pos
    opsvg.se(thing, **p3)

    # ── header title text ("OOMLOUT" in white) ────────────────────────────────
    p3           = copy.deepcopy(kwargs)
    p3["type"]   = "positive"
    p3["shape"]  = "text"
    p3["text"]   = header_title_text
    p3["size"]   = header_title_size
    p3["font"]   = "sans-serif"
    p3["halign"] = "center"
    p3["valign"] = "center"
    p3["color"]  = "#ffffff"
    title_pos    = copy.deepcopy(pos)
    title_pos[1] = pos[1] + header_centre_y
    p3["pos"]    = title_pos
    opsvg.se(thing, **p3)

    # ── bullet mark (small negative circle) ──────────────────────────────────
    p3            = copy.deepcopy(kwargs)
    p3["type"]    = "negative"
    p3["shape"]   = "circle"
    p3["r"]       = bullet_radius
    bullet_pos    = copy.deepcopy(pos)
    bullet_pos[0] = pos[0] + bullet_x
    bullet_pos[1] = pos[1] + body_row_1_y
    p3["pos"]     = bullet_pos
    opsvg.se(thing, **p3)

    # ── part name text (body row 1) ───────────────────────────────────────────
    p3               = copy.deepcopy(kwargs)
    p3["type"]       = "negative"
    p3["shape"]      = "text"
    p3["text"]       = part_name_text
    p3["size"]       = part_name_size
    p3["font"]       = "sans-serif"
    p3["halign"]     = "left"
    p3["valign"]     = "center"
    part_name_pos    = copy.deepcopy(pos)
    part_name_pos[0] = pos[0] + part_name_x
    part_name_pos[1] = pos[1] + body_row_1_y
    p3["pos"]        = part_name_pos
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
    p3                 = copy.deepcopy(kwargs)
    p3["type"]         = "negative"
    p3["shape"]        = "text"
    p3["text"]         = part_number_text
    p3["size"]         = part_number_size
    p3["font"]         = "sans-serif"
    p3["halign"]       = "right"
    p3["valign"]       = "center"
    part_number_pos    = copy.deepcopy(pos)
    part_number_pos[0] = pos[0] + part_number_x
    part_number_pos[1] = pos[1] + part_number_y
    p3["pos"]          = part_number_pos
    opsvg.se(thing, **p3)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    # argv[1]  save_type       "all" or "none"
    save_type = args[0] if len(args) > 0 else "all"

    # argv[2]  filter string   "" = no filter
    filter_str = args[1] if len(args) > 1 else ""

    # argv[3+] output formats  any of "png" "pdf"
    output_formats = [a.lower() for a in args[2:] if a.lower() in ("png", "pdf")]

    main(
        save_type=save_type,
        filter=filter_str,
        output_formats=output_formats,
    )
