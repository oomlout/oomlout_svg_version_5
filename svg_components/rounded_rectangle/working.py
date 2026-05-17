"""
svg_components/rounded_rectangle/working.py

Rectangle with rounded corners, for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

Shape aliases: "rounded_rect", "rrect"
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "rounded_rectangle"
    _d["name_long"] = "Rounded Rectangle"
    _d["description"] = (
        "Axis-aligned rectangle with uniform corner radii, centred on pos. "
        "Accepts aliases 'rounded_rect' and 'rrect'."
    )
    _d["category"] = "SVG Primitives"
    _d["shape_aliases"] = ["rounded_rect", "rrect"]
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "size",
            "description": "Width, height, depth in mm as [w, h, d]. "
                           "Depth is carried through but ignored by the 2-D renderer.",
            "type": "list",
            "default": [20, 10, 3],
        },
        {
            "name": "r",
            "description": "Corner radius in mm.",
            "type": "float",
            "default": 2.0,
        },
        {
            "name": "pos",
            "description": "Centre position [x, y, z] in OOBB mm (Y-up).",
            "type": "list",
            "default": [0, 0, 0],
        },
        {
            "name": "rot",
            "description": "Rotation [rx, ry, rz] degrees. Only rz affects the 2-D render.",
            "type": "list",
            "default": [0, 0, 0],
        },
        {
            "name": "color",
            "description": "Fill colour (CSS colour string, e.g. '#333333'). "
                           "Set to 'none' for an outline-only shape.",
            "type": "string",
            "default": "#333333",
        },
        {
            "name": "stroke",
            "description": "Outline colour (CSS colour string). "
                           "Set to a colour to draw an outline; 'none' disables it.",
            "type": "string",
            "default": "none",
        },
        {
            "name": "stroke_width",
            "description": "Outline width in mm. Only visible when stroke is set.",
            "type": "float",
            "default": 0,
        },
    ]
    return _d


def define():
    global _d
    if not isinstance(_d, dict) or not _d:
        describe()
    result = {}
    result.update(_d)
    return result


def action(**kwargs):
    """
    Return a single rounded_rectangle shape-descriptor.

    Any alias name ("rounded_rect", "rrect") is normalised to
    "rounded_rectangle" so the renderer handles it correctly.

    Parameters
    ----------
    size         : list   [width_mm, height_mm, depth_mm]
    r            : float  corner radius in mm
    pos          : list   [x, y, z] centre in OOBB mm
    rot          : list   [rx, ry, rz] degrees
    color        : str    fill colour (CSS); 'none' = transparent
    stroke       : str    outline colour (CSS); 'none' = no outline
    stroke_width : float  outline width in mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "rounded_rectangle"
    descriptor.setdefault("size",         [20, 10, 3])
    descriptor.setdefault("r",            2.0)
    descriptor.setdefault("pos",          [0, 0, 0])
    descriptor.setdefault("rot",          [0, 0, 0])
    descriptor.setdefault("color",        "#333333")
    descriptor.setdefault("stroke",       "none")
    descriptor.setdefault("stroke_width", 0)
    return [descriptor]
