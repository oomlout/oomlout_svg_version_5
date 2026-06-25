"""
svg_components/dimension_line/working.py

Engineering dimension line: two extension (witness) lines, a dimension bar with
tick marks at each end, and a centred text label.  Matches the style used in
technical drawings such as the OOMLOUT bearing data sheets.

Coordinate notes
----------------
All lengths are in mm in the Y-up part coordinate system (same as every other
component).  ``p1`` and ``p2`` are measured relative to the component's ``pos``.
For a horizontal dimension the line sits above/below; for vertical it sits
left/right — controlled by the sign of ``offset``.
"""

import copy
import math


def describe():
    return {
        "name": "dimension_line",
        "name_long": "Dimension Line",
        "description": (
            "Engineering dimension annotation: extension lines, a dimension bar "
            "with end ticks, and a centred label.  Supports horizontal and "
            "vertical orientations with configurable offset and tick style."
        ),
        "category": "SVG Annotations",
        "shape_aliases": ["dim_line", "dimension"],
        "variables": [
            {
                "name": "p1",
                "description": "First measurement point [x, y] relative to pos.",
                "type": "list",
                "default": [0, 0],
            },
            {
                "name": "p2",
                "description": "Second measurement point [x, y] relative to pos.",
                "type": "list",
                "default": [10, 0],
            },
            {
                "name": "direction",
                "description": (
                    "'horizontal' — dim line runs horizontally, extension lines are vertical.  "
                    "'vertical' — dim line runs vertically, extension lines are horizontal.  "
                    "'auto' (default) — inferred from the larger axis span of p1→p2."
                ),
                "type": "string",
                "default": "auto",
            },
            {
                "name": "offset",
                "description": (
                    "Signed perpendicular distance from the measured edge to the dimension "
                    "bar (mm).  Positive = above for horizontal, right for vertical."
                ),
                "type": "float",
                "default": 10.0,
            },
            {
                "name": "text",
                "description": "Label string.  Omit (or pass '') to auto-compute the distance.",
                "type": "string",
                "default": "",
            },
            {
                "name": "text_size",
                "description": "Label font size in mm.",
                "type": "float",
                "default": 4.0,
            },
            {
                "name": "font",
                "description": "Label font family.",
                "type": "string",
                "default": "Arial, Helvetica, sans-serif",
            },
            {
                "name": "gap",
                "description": "Gap between the measured object edge and the start of each extension line (mm).",
                "type": "float",
                "default": 1.5,
            },
            {
                "name": "overshoot",
                "description": "How far the extension line continues past the dimension bar (mm).",
                "type": "float",
                "default": 1.5,
            },
            {
                "name": "tick_size",
                "description": "Half-length of the tick marks at each end of the dimension bar (mm).",
                "type": "float",
                "default": 1.5,
            },
            {
                "name": "text_offset",
                "description": (
                    "Additional gap between the dimension bar and the text label (mm).  "
                    "Positive places text on the far side of the bar from the object."
                ),
                "type": "float",
                "default": 1.0,
            },
            {
                "name": "stroke_width",
                "description": "Stroke width for all lines (mm).",
                "type": "float",
                "default": 0.3,
            },
            {
                "name": "color",
                "description": "Color applied to lines and text.",
                "type": "string",
                "default": "#000000",
            },
            {
                "name": "pos",
                "description": "Component anchor [x, y, z] in mm (Y-up).",
                "type": "list",
                "default": [0, 0, 0],
            },
        ],
    }


def define():
    d = describe()
    d["shape_name"] = "dimension_line"
    return d


def action(**kwargs):
    """
    Return a list of shape-descriptor dicts (lines + text) that together form
    one engineering dimension annotation.
    """
    pos        = kwargs.get("pos",         [0, 0, 0])
    p1         = kwargs.get("p1",          [0, 0])
    p2         = kwargs.get("p2",          [10, 0])
    direction  = kwargs.get("direction",   "auto")
    offset     = float(kwargs.get("offset",      10.0))
    label      = kwargs.get("text",        "")
    text_size  = float(kwargs.get("text_size",   4.0))
    font       = kwargs.get("font",        "Arial, Helvetica, sans-serif")
    gap        = float(kwargs.get("gap",         1.5))
    overshoot  = float(kwargs.get("overshoot",   1.5))
    tick_size  = float(kwargs.get("tick_size",   1.5))
    text_off   = float(kwargs.get("text_offset", 1.0))
    sw         = float(kwargs.get("stroke_width", 0.3))
    color      = kwargs.get("color",       "#000000")

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    if direction == "auto":
        direction = "horizontal" if abs(dx) >= abs(dy) else "vertical"

    if not label:
        dist  = math.sqrt(dx * dx + dy * dy)
        label = f"{dist:.1f} mm"

    out = []
    sign = 1 if offset >= 0 else -1

    # ── helpers ───────────────────────────────────────────────────────────────

    def _line(x1, y1, x2, y2):
        """Line with p1/p2 relative to component pos."""
        return {
            "shape":        "line",
            "pos":          copy.deepcopy(pos),
            "p1":           [x1, y1],
            "p2":           [x2, y2],
            "stroke":       color,
            "stroke_width": sw,
            "color":        color,
        }

    def _text(rx, ry, txt, rz=0):
        """Text at absolute part-space position pos + (rx, ry)."""
        return {
            "shape":  "text",
            "pos":    [pos[0] + rx, pos[1] + ry, pos[2] if len(pos) > 2 else 0],
            "text":   txt,
            "size":   text_size,
            "font":   font,
            "halign": "center",
            "valign": "center",
            "color":  color,
            "rot":    [0, 0, rz],
        }

    # ── horizontal dimension ──────────────────────────────────────────────────
    if direction == "horizontal":
        # Dimension bar sits at:  y_bar = point_y + offset
        # For each measured point the extension line runs from (point_y + gap*sign)
        # to (y_bar + overshoot*sign).

        for px, py in (p1, p2):
            y_near = py + gap * sign
            y_far  = py + offset + overshoot * sign
            out.append(_line(px, y_near, px, y_far))

        # Dimension bar
        out.append(_line(p1[0], p1[1] + offset, p2[0], p2[1] + offset))

        # Tick marks (perpendicular = vertical)
        for px, py in (p1, p2):
            y_bar = py + offset
            out.append(_line(px, y_bar - tick_size, px, y_bar + tick_size))

        # Label above (or below) the bar
        mid_x  = (p1[0] + p2[0]) / 2
        mid_y  = (p1[1] + p2[1]) / 2 + offset
        text_y = mid_y + sign * (text_size * 0.6 + text_off)
        out.append(_text(mid_x, text_y, label))

    # ── vertical dimension ────────────────────────────────────────────────────
    else:
        # Dimension bar sits at:  x_bar = point_x + offset

        for px, py in (p1, p2):
            x_near = px + gap * sign
            x_far  = px + offset + overshoot * sign
            out.append(_line(x_near, py, x_far, py))

        # Dimension bar
        out.append(_line(p1[0] + offset, p1[1], p2[0] + offset, p2[1]))

        # Tick marks (perpendicular = horizontal)
        for px, py in (p1, p2):
            x_bar = px + offset
            out.append(_line(x_bar - tick_size, py, x_bar + tick_size, py))

        # Label right (or left) of the bar, rotated 90° (reads bottom-to-top)
        mid_x  = (p1[0] + p2[0]) / 2 + offset
        mid_y  = (p1[1] + p2[1]) / 2
        text_x = mid_x + sign * (text_size * 0.6 + text_off)
        out.append(_text(text_x, mid_y, label, rz=90))

    return out
