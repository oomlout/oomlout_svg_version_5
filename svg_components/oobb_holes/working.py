"""
svg_components/oobb_holes/working.py

OOBB hole-grid component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

Renders one circle at each grid intersection of a width×height OOBB plate.
Hole radius is resolved via opsvg._gv(), which automatically appends the
'_laser' suffix when the bare name is not found in the variable table.
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "oobb_holes"
    _d["name_long"] = "OOBB Hole Grid"
    _d["description"] = (
        "Grid of circles at every OOBB hole position for a width×height plate. "
        "radius_name selects the fastener size (e.g. 'm6', 'm3'). "
        "Typically used as type='negative' to cut holes through a plate."
    )
    _d["category"] = "OOBB Shapes"
    _d["shape_aliases"] = []
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "width",
            "description": "Grid width in OOBB units (number of hole columns).",
            "type": "int",
            "default": 1,
        },
        {
            "name": "height",
            "description": "Grid height in OOBB units (number of hole rows).",
            "type": "int",
            "default": 1,
        },
        {
            "name": "radius_name",
            "description": "Fastener size key, e.g. 'm6', 'm3', 'm4'. "
                           "Resolved via opsvg._gv('hole_radius_<name>').",
            "type": "string",
            "default": "m6",
        },
        {
            "name": "pos",
            "description": "Centre position [x, y, z] in OOBB mm (Y-up). "
                           "Must match the pos of the companion oobb_plate.",
            "type": "list",
            "default": [0, 0, 0],
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
    Return a single oobb_holes shape-descriptor.

    Parameters
    ----------
    type        : str  "positive" or "negative"
    width       : int  number of hole columns
    height      : int  number of hole rows
    radius_name : str  fastener key, e.g. "m6"
    pos         : list [x, y, z] centre in OOBB mm
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "oobb_holes"
    descriptor.setdefault("width",       1)
    descriptor.setdefault("height",      1)
    descriptor.setdefault("radius_name", "m6")
    descriptor.setdefault("pos",         [0, 0, 0])
    return [descriptor]
