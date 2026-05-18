"""
svg_components/oobb_circle/working.py

OOBB circular disc component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

Diameter is given in OOBB units; the rendered radius is:
    r = diameter × osp / 2   (e.g. diameter=3 → r = 3×15/2 = 22.5 mm)
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "oobb_circle"
    _d["name_long"] = "OOBB Circle"
    _d["description"] = (
        "Solid disc sized to the OOBB grid. "
        "diameter is in OOBB units (osp=15 mm), so diameter=3 → 45 mm outer diameter."
    )
    _d["category"] = "OOBB Shapes"
    _d["shape_aliases"] = []
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "diameter",
            "description": "Disc diameter in OOBB units. "
                           "Rendered radius = diameter × osp / 2.",
            "type": "float",
            "default": 1,
        },
        {
            "name": "pos",
            "description": "Centre position [x, y, z] in OOBB mm (Y-up).",
            "type": "list",
            "default": [0, 0, 0],
        },
        {
            "name": "rot",
            "description": "Rotation [rx, ry, rz] degrees. "
                           "rz rotates any attached transform; the disc itself is symmetric.",
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
    Return a single oobb_circle shape-descriptor.

    Parameters
    ----------
    diameter     : float  disc diameter in OOBB units
    pos          : list   [x, y, z] centre in OOBB mm
    rot          : list   [rx, ry, rz] degrees (rz has no visual effect on a circle)
    color        : str    fill colour (CSS); 'none' = transparent
    stroke       : str    outline colour (CSS); 'none' = no outline
    stroke_width : float  outline width in mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "oobb_circle"
    descriptor.setdefault("diameter",     1)
    descriptor.setdefault("pos",          [0, 0, 0])
    descriptor.setdefault("rot",          [0, 0, 0])
    descriptor.setdefault("color",        "#333333")
    descriptor.setdefault("stroke",       "none")
    descriptor.setdefault("stroke_width", 0)
    return [descriptor]
