"""
svg_components/polygon/working.py

Arbitrary filled polygon shape component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

Points are given relative to pos so the whole polygon can be repositioned
by changing pos alone.
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "polygon"
    _d["name_long"] = "Polygon"
    _d["description"] = (
        "Arbitrary filled polygon. Points are relative to pos, "
        "so repositioning is done by changing pos alone."
    )
    _d["category"] = "SVG Primitives"
    _d["shape_aliases"] = []
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "points",
            "description": "List of [x, y] vertices in mm, relative to pos. "
                           "The polygon is automatically closed.",
            "type": "list",
            "default": [[0, 5], [-5, -5], [5, -5]],
        },
        {
            "name": "pos",
            "description": "Origin offset [x, y, z] in OOBB mm (Y-up). "
                           "All points are translated by this value.",
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
    Return a single polygon shape-descriptor.

    Parameters
    ----------
    points       : list   [[x, y], ...] vertices in mm, relative to pos
    pos          : list   [x, y, z] origin in OOBB mm
    rot          : list   [rx, ry, rz] degrees
    color        : str    fill colour (CSS); 'none' = transparent
    stroke       : str    outline colour (CSS); 'none' = no outline
    stroke_width : float  outline width in mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "polygon"
    descriptor.setdefault("points",       [[0, 5], [-5, -5], [5, -5]])
    descriptor.setdefault("pos",          [0, 0, 0])
    descriptor.setdefault("rot",          [0, 0, 0])
    descriptor.setdefault("color",        "#333333")
    descriptor.setdefault("stroke",       "none")
    descriptor.setdefault("stroke_width", 0)
    return [descriptor]
