"""
svg_components/slot/working.py

Capsule (slot) shape component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

A slot is two semicircles joined by a rectangle — useful for adjustment slots
that allow a fastener to slide during assembly.

Orientation:
  default (rot=[0,0,0])  — horizontal, long axis along X
  rot=[0,0,90]           — vertical,   long axis along Y
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "slot"
    _d["name_long"] = "Slot (Capsule)"
    _d["description"] = (
        "Capsule shape: two semicircles joined by a rectangle. "
        "Horizontal by default; use rot=[0,0,90] for a vertical slot."
    )
    _d["category"] = "SVG Primitives"
    _d["shape_aliases"] = ["capsule"]
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "r",
            "description": "End-cap radius in mm (also controls slot width = 2r).",
            "type": "float",
            "default": 3.0,
        },
        {
            "name": "w",
            "description": "Centre-to-centre travel distance in mm "
                           "(total length = w + 2r).",
            "type": "float",
            "default": 10.0,
        },
        {
            "name": "pos",
            "description": "Centre position [x, y, z] in OOBB mm (Y-up).",
            "type": "list",
            "default": [0, 0, 0],
        },
        {
            "name": "rot",
            "description": "Rotation [rx, ry, rz] degrees. Use rz=90 for vertical.",
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
    Return a single slot shape-descriptor.

    Parameters
    ----------
    r            : float  end-cap radius in mm
    w            : float  centre-to-centre length in mm
    pos          : list   [x, y, z] centre in OOBB mm
    rot          : list   [rx, ry, rz] degrees; rz=90 -> vertical
    color        : str    fill colour (CSS); 'none' = transparent
    stroke       : str    outline colour (CSS); 'none' = no outline
    stroke_width : float  outline width in mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "slot"
    descriptor.setdefault("r",            3.0)
    descriptor.setdefault("w",            10.0)
    descriptor.setdefault("pos",          [0, 0, 0])
    descriptor.setdefault("rot",          [0, 0, 0])
    descriptor.setdefault("color",        "#333333")
    descriptor.setdefault("stroke",       "none")
    descriptor.setdefault("stroke_width", 0)
    return [descriptor]
