"""
svg_components/oobb_plate/working.py

OOBB plate footprint component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

Renders a rounded rectangle sized to the OOBB grid:
    width_mm  = width  × osp − osp_minus  (e.g. 2×15−1 = 29 mm)
    height_mm = height × osp − osp_minus

osp and osp_minus are read from oobb.gv() when available, otherwise
the standard defaults (15 mm / 1 mm) are used.
"""

import copy
import svg_variables as _sv

_d   = {}
_OSP  = _sv.OSP
_OSPM = _sv.OSP_MINUS


def describe():
    global _d
    _d = {}
    _d["name"] = "oobb_plate"
    _d["name_long"] = "OOBB Plate"
    _d["description"] = (
        "OOBB grid plate: a rounded rectangle whose dimensions are computed "
        "from width/height in OOBB units (osp=15 mm, osp_minus=1 mm). "
        "A 2×1 plate is 29×14 mm."
    )
    _d["category"] = "OOBB Shapes"
    _d["shape_aliases"] = []
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "width",
            "description": "Plate width in OOBB units.",
            "type": "int",
            "default": 1,
        },
        {
            "name": "height",
            "description": "Plate height in OOBB units.",
            "type": "int",
            "default": 1,
        },
        {
            "name": "corner_radius",
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
    Return a single oobb_plate shape-descriptor.

    Parameters
    ----------
    width         : int   plate width in OOBB units
    height        : int   plate height in OOBB units
    corner_radius : float corner radius in mm
    pos           : list  [x, y, z] centre in OOBB mm
    rot           : list  [rx, ry, rz] degrees
    color         : str   fill colour (CSS); 'none' = transparent
    stroke        : str   outline colour (CSS); 'none' = no outline
    stroke_width  : float outline width in mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "oobb_plate"
    descriptor.setdefault("width",         1)
    descriptor.setdefault("height",        1)
    descriptor.setdefault("corner_radius", 2.0)
    descriptor.setdefault("pos",           [0, 0, 0])
    descriptor.setdefault("rot",           [0, 0, 0])
    descriptor.setdefault("color",         "#333333")
    descriptor.setdefault("stroke",        "none")
    descriptor.setdefault("stroke_width",  0)
    return [descriptor]
