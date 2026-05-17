"""
svg_components/rect/working.py

Axis-aligned rectangle shape component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "rect"
    _d["name_long"] = "Rectangle"
    _d["description"] = "Axis-aligned filled rectangle, centred on pos."
    _d["category"] = "SVG Primitives"
    _d["shape_aliases"] = []
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "size",
            "description": "Width, height and depth in mm as [w, h, d]. "
                           "Depth is carried through but ignored by the 2-D renderer.",
            "type": "list",
            "default": [10, 10, 3],
        },
        {
            "name": "pos",
            "description": "Centre position [x, y, z] in OOBB mm (Y-up).",
            "type": "list",
            "default": [0, 0, 0],
        },
        {
            "name": "rot",
            "description": "Rotation [rx, ry, rz] in degrees. Only rz (Z-axis) "
                           "affects the 2-D render.",
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
    Return a single rect shape-descriptor.

    Parameters
    ----------
    size         : list   [width_mm, height_mm, depth_mm]
    pos          : list   [x, y, z] centre in OOBB mm
    rot          : list   [rx, ry, rz] degrees
    color        : str    fill colour (CSS), e.g. '#333333'; 'none' = transparent
    stroke       : str    outline colour (CSS); 'none' = no outline
    stroke_width : float  outline width in mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "rect"
    descriptor.setdefault("size",         [10, 10, 3])
    descriptor.setdefault("pos",          [0, 0, 0])
    descriptor.setdefault("rot",          [0, 0, 0])
    descriptor.setdefault("color",        "#333333")
    descriptor.setdefault("stroke",       "none")
    descriptor.setdefault("stroke_width", 0)
    return [descriptor]
