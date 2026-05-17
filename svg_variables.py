"""
svg_variables.py  —  Standalone constants and helpers for the SVG pipeline.

Replaces every call to oobb.gv() / oobb.get_hole_pos() so that opsvg.py,
svg_help.py, and working_svg.py have zero dependency on the oobb package.

All hole radii are laser-cut values (the equivalent of mode="laser" in the
upstream oobb_variables.py).  3dpr / true-size variants are not needed here
because SVG output targets 2-D laser-cut flat parts only.

Usage
-----
    import svg_variables as sv

    pitch      = sv.OSP                 # 15.0
    hole_r     = sv.hole_radius("m6")   # 3.0
    x, y       = sv.hole_pos(1, 1, 2, 1)
    val        = sv.gv("osp")           # 15.0
"""

# ─────────────────────────────────────────────────────────────────────────────
# Grid constants  (mirrors oobb_variables.py osp / osp_minus)
# ─────────────────────────────────────────────────────────────────────────────

OSP        = 15.0    # OOBB standard pitch in mm
OSP_MINUS  = 1.0     # body shrink applied once per axis (not per edge)
OSP_HOLE   = "m6"    # default fastener size for hole grids
OSPE       = 7.5     # half-pitch (used in some component calculations)
OSPE_MINUS = 0.5     # half of osp_minus

# ─────────────────────────────────────────────────────────────────────────────
# Hole radii — laser-cut values (mm radius, not diameter)
# Source: oobb_variables.py, [0] (laser) element of each 3-element list.
# ─────────────────────────────────────────────────────────────────────────────

HOLE_RADII = {
    # metric clearance holes
    "md5":      0.25,   # M0.5
    "m1":       0.50,   # M1
    "m1_4":     0.70,   # M1.4
    "m1_5":     0.80,   # M1.5
    "m1_6":     0.85,   # M1.6
    "m2":       1.00,   # M2
    "m2_5":     1.25,   # M2.5
    "m3":       1.50,   # M3
    "m3_5":     1.75,   # M3.5
    "m4":       2.00,   # M4
    "m5":       2.50,   # M5
    "m6":       3.00,   # M6  ← OOBB standard
    "m7":       3.50,   # M7
    "m8":       4.00,   # M8
    "m10":      5.00,   # M10
    "m11":      5.50,   # M11
    "m12":      6.00,   # M12
    # wood screw clearance holes
    "m3_screw_wood": 2.00,
    "m4_screw_wood": 2.60,
    "m5_screw_wood": 2.25,
    "m6_screw_wood": 2.25,
}

# ─────────────────────────────────────────────────────────────────────────────
# Visual defaults  (used by opsvg.py as fallbacks)
# ─────────────────────────────────────────────────────────────────────────────

FILL_POSITIVE = "#333333"   # material / ink colour
FILL_NEGATIVE = "#ffffff"   # cut / background colour
STROKE        = "none"
STROKE_WIDTH  = 0
PADDING_MM    = 5.0         # whitespace around part bounding box
CORNER_RADIUS = 2.0         # default rounded-rectangle corner radius (mm)

# ─────────────────────────────────────────────────────────────────────────────
# Named variable lookup table
# Allows opsvg._gv("osp") style access for backward compatibility.
# ─────────────────────────────────────────────────────────────────────────────

_VARIABLES = {
    "osp":         OSP,
    "osp_minus":   OSP_MINUS,
    "osp_hole":    OSP_HOLE,
    "ospe":        OSPE,
    "ospe_minus":  OSPE_MINUS,
}

# Inject all hole radii under their canonical names
for _name, _r in HOLE_RADII.items():
    _VARIABLES[f"hole_radius_{_name}"] = _r


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def gv(name):
    """
    Get a variable value by name.

    Raises KeyError if the name is not found, so callers can distinguish
    "missing" from zero.

    Examples
    --------
        sv.gv("osp")                  # 15.0
        sv.gv("hole_radius_m6")       # 3.0
    """
    if name in _VARIABLES:
        return _VARIABLES[name]
    raise KeyError(f"svg_variables: unknown variable '{name}'")


def hole_radius(name):
    """
    Return the laser-cut hole radius in mm for the given shorthand name.

    Accepts:
        bare name        e.g. "m6"        → looks up HOLE_RADII["m6"]
        prefixed name    e.g. "hole_radius_m6"
        mode-suffixed    e.g. "m6_laser" / "m6_true" / "m6_3dpr"
                         (all normalised to the laser value)

    Raises KeyError if nothing matches.

    Examples
    --------
        sv.hole_radius("m6")            # 3.0
        sv.hole_radius("hole_radius_m6") # 3.0
        sv.hole_radius("m6_laser")      # 3.0
    """
    # Strip known mode suffixes
    for suffix in ("_laser", "_true", "_3dpr"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break

    # Strip "hole_radius_" prefix if present
    if name.startswith("hole_radius_"):
        name = name[len("hole_radius_"):]

    if name in HOLE_RADII:
        return HOLE_RADII[name]

    raise KeyError(f"svg_variables: unknown hole radius '{name}'")


def hole_pos(xi, yi, w, h):
    """
    Return (x_mm, y_mm) for hole grid position (xi, yi) in a w×h OOBB plate.

    xi, yi are 1-based column / row indices (1 … w, 1 … h).
    The origin is at the plate centre (Y-up convention).

    Mirrors oobb.get_hole_pos(xi, yi, w, h).

    Examples
    --------
        # Centre hole of a 1×1 plate
        sv.hole_pos(1, 1, 1, 1)   # (0.0, 0.0)

        # Left and right holes of a 2×1 plate
        sv.hole_pos(1, 1, 2, 1)   # (-7.5, 0.0)
        sv.hole_pos(2, 1, 2, 1)   # ( 7.5, 0.0)
    """
    x = -(w - 1) * OSP / 2 + (xi - 1) * OSP
    y = -(h - 1) * OSP / 2 + (yi - 1) * OSP
    return (x, y)
