import copy
import math
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


d = {}

# ---------------------------------------------------------------------------
# OpenSCAD geometry
# ---------------------------------------------------------------------------

SCAD_SOURCE = """
module oobb_cube_hexagon_cutout_raw(sx=100, sy=100, sz=10, cut_sx=100, cut_sy=100, cut_sz=10, hex_r=10, border=10, rot_cut=[0, 0, 0]) {
    // Flat-top hexagon tiling:
    //   col_step = hex_r * sqrt(3)   (horizontal centre-to-centre, same row)
    //   row_step = hex_r * 1.5       (vertical   centre-to-centre)
    //   odd rows are offset by col_step/2
    // Shrink the cutout hexagons relative to the lattice pitch so the
    // requested border width also appears between neighbouring cutouts.
    col_step = hex_r * sqrt(3);
    row_step = hex_r * 1.5;
    hex_cut_r = max(hex_r - border / sqrt(3), 0.01);
    usable_x = cut_sx - border * 2;
    usable_y = cut_sy - border * 2;
    cols = ceil(usable_x / col_step) + 2;
    rows = ceil(usable_y / row_step) + 2;

    // Outer cube minus only the hex-hole portion of the inner workspace.
    difference() {
        cube([sx, sy, sz], center=true);
        rotate(rot_cut)
            intersection() {
                // Inner cube clips the cutout region to keep the edge border.
                cube([usable_x, usable_y, cut_sz + 2], center=true);
                // Hex lattice clipped by the inner cube becomes the subtraction volume.
                for (row = [-rows : rows]) {
                    for (col = [-cols : cols]) {
                        x_off = (row % 2 == 0) ? 0 : col_step / 2;
                        translate([col * col_step + x_off, row * row_step, 0])
                            rotate([0, 0, 30])
                                cylinder(r=hex_cut_r, h=cut_sz + 4, center=true, $fn=6);
                    }
                }
            }
    }
}
"""


def _matrix_multiply(a, b):
    return [
        [
            sum(a[row][idx] * b[idx][col] for idx in range(3))
            for col in range(3)
        ]
        for row in range(3)
    ]


def _rotation_matrix_xyz(rot):
    rx = math.radians(rot[0])
    ry = math.radians(rot[1])
    rz = math.radians(rot[2])

    mx = [
        [1, 0, 0],
        [0, math.cos(rx), -math.sin(rx)],
        [0, math.sin(rx), math.cos(rx)],
    ]
    my = [
        [math.cos(ry), 0, math.sin(ry)],
        [0, 1, 0],
        [-math.sin(ry), 0, math.cos(ry)],
    ]
    mz = [
        [math.cos(rz), -math.sin(rz), 0],
        [math.sin(rz), math.cos(rz), 0],
        [0, 0, 1],
    ]

    # OpenSCAD rotate([x, y, z]) applies X, then Y, then Z.
    return _matrix_multiply(mz, _matrix_multiply(my, mx))


def _local_cutout_size(size, rot_cut):
    rotation_matrix = _rotation_matrix_xyz(rot_cut)
    return [
        sum(abs(rotation_matrix[row][col]) * size[row] for row in range(3))
        for col in range(3)
    ]


# ---------------------------------------------------------------------------
# Component metadata
# ---------------------------------------------------------------------------

def describe():
    global d
    d = {}
    d["name"] = 'oobb_cube_hexagon_cutout'
    d["name_long"] = 'OOBB Geometry Primitives: Cube with Hexagon Cutouts'
    d["description"] = (
        'A cube with a tiling hexagonal cutout pattern. '
        'A solid border is preserved around all edges and between neighbouring cutouts. '
        'The hex grid rotation can be adjusted with rotation_cutout.'
    )
    d["category"] = 'OOBB Geometry Primitives'
    d["shape_aliases"] = ['oobb_cube_hexagon_cutout']
    d["returns"] = 'List of geometry component dicts.'
    v = []
    v.append({"name": 'pos',              "description": '3-element [x,y,z] position.',                        "type": 'list',   "default": '[0,0,0]'})
    v.append({"name": 'size',             "description": '[x,y,z] outer cube dimensions in mm.',               "type": 'list',   "default": '(required)'})
    v.append({"name": 'hexagon_radius',   "description": 'Base circumradius used to lay out the hex lattice (mm).', "type": 'number', "default": 10})
    v.append({"name": 'border_width',     "description": 'Solid border width kept around the cube edges and between cutouts (mm).', "type": 'number', "default": 10})
    v.append({"name": 'rotation_cutout',  "description": 'Rotation [rx,ry,rz] for the hex grid in degrees. A scalar still maps to Z for compatibility.',  "type": 'list',   "default": '[0,0,0]'})
    v.append({"name": 'type',             "description": 'Geometry type: positive or negative.',               "type": 'string', "default": '"positive"'})
    v.append({"name": 'zz',              "description": 'Z anchor point: bottom, top, center/middle.',         "type": 'string', "default": '"bottom"'})
    v.append({"name": 'rot',             "description": 'Rotation [rx,ry,rz] in degrees.',                     "type": 'list',   "default": '[0,0,0]'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------

def action(**kwargs):
    """Cube with tiling hexagonal cutouts and a solid border around the edges."""
    pos  = list(kwargs.get("pos", [0, 0, 0]))
    size = list(kwargs.get("size", [100, 100, 10]))
    zz   = kwargs.get("zz", "bottom")
    rot  = list(kwargs.get("rot", [0, 0, 0]))
    typ  = kwargs.get("type", kwargs.get("t", "positive"))

    hex_r  = kwargs.get("hexagon_radius", 10)
    border = kwargs.get("border_width", 10)
    rot_cut = kwargs.get("rotation_cutout", [0, 0, 0])
    if isinstance(rot_cut, (int, float)):
        rot_cut = [0, 0, rot_cut]
    else:
        rot_cut = list(rot_cut)
        if len(rot_cut) != 3:
            raise ValueError("rotation_cutout must be a number or a 3-element rotation list.")

    sx, sy, sz = size[0], size[1], size[2]
    cut_sx, cut_sy, cut_sz = _local_cutout_size(size, rot_cut)
    usable_x = cut_sx - border * 2
    usable_y = cut_sy - border * 2
    if usable_x <= 0 or usable_y <= 0:
        print("Warning: border_width is too large for the given size and rotation, no cutouts will be made.")

    # Adjust Z origin so the shape sits on the correct anchor plane.
    # The SCAD module uses center=true, so the geometry spans -sz/2 to +sz/2.
    # We shift pos[2] so that the requested anchor aligns with z=0.
    if zz in ("center", "middle"):
        pos[2] = pos[2]               # centred already
    elif zz == "top":
        pos[2] = pos[2] - sz / 2
    else:  # bottom (default)
        pos[2] = pos[2] + sz / 2

    return {
        "type": typ,
        "shape": "raw_scad",
        "source": SCAD_SOURCE,
        "module": "oobb_cube_hexagon_cutout_raw",
        "module_kwargs": {
            "sx": sx,
            "sy": sy,
            "sz": sz,
            "cut_sx": cut_sx,
            "cut_sy": cut_sy,
            "cut_sz": cut_sz,
            "hex_r": hex_r,
            "border": border,
            "rot_cut": rot_cut,
        },
        "pos": pos,
        "rot": rot,
    }


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [30, 0, 35],
      'kwargs': {'pos': [0, 0, 0],
                 'size': [40, 30, 20],
                 'hexagon_radius': 4,
                 'border_width': 2.4,
                 'rotation_cutout': [0, 0, 0],
                 'type': 'positive',
                 'zz': 'middle',
                 'rot': [0, 0, 0]}},
     {'filename': 'test_2',
      'preview_rot': [30, 0, 35],
      'kwargs': {'pos': [0, 0, 0],
                 'size': [40, 30, 20],
                 'hexagon_radius': 4,
                 'border_width': 2.4,
                 'rotation_cutout': [0, 0, 30],
                 'type': 'positive',
                 'zz': 'middle',
                 'rot': [0, 0, 0]}}]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, dict) and "components" in result:
            components = copy.deepcopy(result["components"])
        elif isinstance(result, list):
            components = result
        else:
            components = [result]

        sample_dir = os.path.join(test_dir, sample["filename"])
        os.makedirs(sample_dir, exist_ok=True)
        scad_path = os.path.join(sample_dir, "working.scad")
        png_path = os.path.join(sample_dir, "image.png")

        opsc.opsc_make_object(
            scad_path,
            components,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_preview_images(scad_path, sample_dir)
        generated_files.append(png_path)

    return generated_files


