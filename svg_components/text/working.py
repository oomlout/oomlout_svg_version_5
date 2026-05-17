"""
svg_components/text/working.py

SVG text label component for the opsvg SVG pipeline.
Follows the components/*/working.py contract from oomlout_oobb_version_5.

Text is always rendered as-is in the SVG; no outlining or path conversion
is performed.  Supply a web-safe font or embed the font separately if the
SVG will be used outside Inkscape.
"""

import copy

_d = {}


def describe():
    global _d
    _d = {}
    _d["name"] = "text"
    _d["name_long"] = "Text Label"
    _d["description"] = (
        "SVG text element positioned at pos. "
        "Supports horizontal/vertical alignment, font family, and size. "
        "Use the color kwarg to override the default fill colour."
    )
    _d["category"] = "SVG Annotations"
    _d["shape_aliases"] = ["label"]
    _d["returns"] = "List containing one shape-descriptor dict."
    _d["variables"] = [
        {
            "name": "text",
            "description": "The string to render.",
            "type": "string",
            "default": "",
        },
        {
            "name": "size",
            "description": "Font size in mm.",
            "type": "float",
            "default": 4.0,
        },
        {
            "name": "font",
            "description": "Font family name. A ':style=Bold' suffix is stripped "
                           "to keep the SVG font-family clean.",
            "type": "string",
            "default": "sans-serif",
        },
        {
            "name": "halign",
            "description": "Horizontal alignment: 'left', 'center', or 'right'.",
            "type": "string",
            "default": "center",
        },
        {
            "name": "valign",
            "description": "Vertical alignment: 'bottom', 'center', or 'top'.",
            "type": "string",
            "default": "center",
        },
        {
            "name": "color",
            "description": "Optional explicit fill colour (CSS colour string). "
                           "Overrides the type-based fill so white text can sit "
                           "on a dark header bar.",
            "type": "string",
            "default": "",
        },
        {
            "name": "pos",
            "description": "Anchor position [x, y, z] in OOBB mm (Y-up).",
            "type": "list",
            "default": [0, 0, 0],
        },
        {
            "name": "rot",
            "description": "Rotation [rx, ry, rz] degrees. Only rz affects the 2-D render.",
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
    Return a single text shape-descriptor.

    Parameters
    ----------
    type   : str   "positive" or "negative"
    text   : str   string to render
    size   : float font size in mm
    font   : str   font-family (web-safe name or 'Name:style=Bold')
    halign : str   "left" | "center" | "right"
    valign : str   "bottom" | "center" | "top"
    color  : str   optional explicit CSS colour
    pos    : list  [x, y, z] anchor in OOBB mm
    rot    : list  [rx, ry, rz] degrees
    """
    descriptor = copy.deepcopy(kwargs)
    descriptor["shape"] = "text"
    descriptor.setdefault("text",   "")
    descriptor.setdefault("size",   4.0)
    descriptor.setdefault("font",   "sans-serif")
    descriptor.setdefault("halign", "center")
    descriptor.setdefault("valign", "center")
    descriptor.setdefault("pos",    [0, 0, 0])
    descriptor.setdefault("rot",    [0, 0, 0])
    return [descriptor]
