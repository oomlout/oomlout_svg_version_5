d = {}


SCAD_SOURCE = """module gridfinity_base_tile_raw(distancex=0, distancey=0, fitx=0, fity=0) {
    $fa = 8;
    $fs = 0.25;
    clearance = 0.5;
    grid_pitch = 42;
    tile_size = grid_pitch - clearance;
    outer_diameter = 8;
    inner_span = tile_size - outer_diameter;
    fill_cube_size = 35.15 - clearance;

    function _rx(a) = [
        [1, 0, 0, 0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a), cos(a), 0],
        [0, 0, 0, 1]
    ];

    function _ry(a) = [
        [cos(a), 0, sin(a), 0],
        [0, 1, 0, 0],
        [-sin(a), 0, cos(a), 0],
        [0, 0, 0, 1]
    ];

    function _rz(a) = [
        [cos(a), -sin(a), 0, 0],
        [sin(a), cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ];

    module sweep_rounded_square_34(size = inner_span) {
        half_size = size / 2;
        path_points = [
            [-half_size, half_size],
            [half_size, half_size],
            [half_size, -half_size],
            [-half_size, -half_size],
            [-half_size, half_size]
        ];

        path_vectors = [
            path_points[1] - path_points[0],
            path_points[2] - path_points[1],
            path_points[3] - path_points[2],
            path_points[4] - path_points[3]
        ];

        first_translation = [
            [1, 0, 0, path_points[0].y],
            [0, 1, 0, 0],
            [0, 0, 1, path_points[0].x],
            [0, 0, 0, 1]
        ];

        affine_translations = concat([first_translation], [
            for (
                i = 0, a = first_translation;
                i < len(path_vectors);
                a = a * [
                    [1, 0, 0, path_vectors[i].y],
                    [0, 1, 0, 0],
                    [0, 0, 1, path_vectors[i].x],
                    [0, 0, 0, 1]
                ],
                i = i + 1
            )
            a * [
                [1, 0, 0, path_vectors[i].y],
                [0, 1, 0, 0],
                [0, 0, 1, path_vectors[i].x],
                [0, 0, 0, 1]
            ]
        ]);

        base_rotation = _rz(90) * _ry(0) * _rx(90);

        walls = [
            for (i = [0 : 3])
            base_rotation * affine_translations[i]
            * (_rz(0) * _ry(atan2(path_vectors[i].y, path_vectors[i].x)) * _rx(0))
        ];

        union() {
            for (i = [0 : 3]) {
                multmatrix(walls[i])
                linear_extrude(size)
                children();

                multmatrix(walls[i] * (_rz(0) * _ry(0) * _rx(-90)))
                rotate_extrude(angle = 90, convexity = 4)
                children();
            }
        }
    }

    grid_size = [1, 1];

    grid_size_mm = [grid_size.x * tile_size, grid_size.y * tile_size, 4.631];
    size_mm = [
        max(grid_size_mm.x, distancex),
        max(grid_size_mm.y, distancey),
        4.631
    ];
    padding_mm = size_mm - grid_size_mm;
    fit_percent_positive = [(fitx + 1) / 2, (fity + 1) / 2];

    padding_start_point = -grid_size_mm / 2 - [
        padding_mm.x * (1 - fit_percent_positive.x),
        padding_mm.y * (1 - fit_percent_positive.y),
        -grid_size_mm.z / 2
    ];

    echo(str("Number of Grids per axes (X, Y)]: ", grid_size));
    echo(str("Final size (in mm): ", size_mm));

    if (padding_mm != [0, 0, 0]) {
        echo(str("Padding +X (in mm): ", padding_mm.x * fit_percent_positive.x));
        echo(str("Padding -X (in mm): ", padding_mm.x * (1 - fit_percent_positive.x)));
        echo(str("Padding +Y (in mm): ", padding_mm.y * fit_percent_positive.y));
        echo(str("Padding -Y (in mm): ", padding_mm.y * (1 - fit_percent_positive.y)));
    }

    translate(padding_start_point)
    for (x = [0 : grid_size.x - 1]) {
        for (y = [0 : grid_size.y - 1]) {
            translate([(x + 0.5) * tile_size, (y + 0.5) * tile_size, -0.01])
            union() {
                sweep_rounded_square_34() {
                    polygon([
                        [1.15, 0.001],
                        [1.85, 0.701],
                        [1.85, 2.501],
                        [4.00, 4.651],
                        [0, 4.651],
                        [0, 0],
                        [1.15, 0]
                    ]);
                }

                translate([0, 0, 4.651 / 2])
                cube([fill_cube_size, fill_cube_size, 4.651], center = true);
            }
        }
    }
}
"""


def describe():
    global d
    d = {}
    d["name"] = 'gridfinity_base_tile'
    d["name_long"] = 'Gridfinity: Base Tile'
    d["description"] = 'Returns the raw OpenSCAD source for a Gridfinity base tile.'
    d["category"] = 'Gridfinity'
    d["shape_aliases"] = ['gridfinity_base_tile']
    d["returns"] = 'SCAD source string.'
    v = []
    v.append({"name": 'distancex', "description": 'Distance in X direction (mm).', "type": 'number', "default": 0})
    v.append({"name": 'distancey', "description": 'Distance in Y direction (mm).', "type": 'number', "default": 0})
    v.append({"name": 'fitx', "description": 'Fit adjustment in X (mm).', "type": 'number', "default": 0})
    v.append({"name": 'fity', "description": 'Fit adjustment in Y (mm).', "type": 'number', "default": 0})
    v.append({"name": 'pos', "description": '3-element [x,y,z] position.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'rot', "description": 'Rotation [rx,ry,rz] in degrees.', "type": 'list', "default": '[0,0,0]'})
    v.append({"name": 'type', "description": 'Geometry type: positive or negative.', "type": 'string', "default": '"positive"'})
    d["variables"] = v
    return d


def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    defined_variable = {}
    defined_variable.update(d)
    return defined_variable
def action(**kwargs):
    distancex = kwargs.get("distancex", 0)
    distancey = kwargs.get("distancey", 0)
    fitx = kwargs.get("fitx", 0)
    fity = kwargs.get("fity", 0)
    pos = list(kwargs.get("pos", [0, 0, 0]))
    rot = kwargs.get("rot", [0, 0, 0])
    inclusion = kwargs.get("inclusion", "all")
    m = kwargs.get("m", "")
    typ = kwargs.get("type", kwargs.get("t", "positive"))

    pos[2] -= 6.1

    return {
        "type": typ,
        "shape": "raw_scad",
        "source": SCAD_SOURCE,
        "module": "gridfinity_base_tile_raw",
        "module_kwargs": {
            "distancex": distancex,
            "distancey": distancey,
            "fitx": fitx,
            "fity": fity,
        },
        "pos": pos,
        "rot": rot,
        "inclusion": inclusion,
        "m": m,
    }


def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(folder, "test")
    os.makedirs(test_dir, exist_ok=True)

    samples = [{'filename': 'test_1',
      'preview_rot': [55, 0, 25],
      'kwargs': {'distancex': 0,
                 'distancey': 0,
                 'fitx': 0,
                 'fity': 0,
                 'pos': [0, 0, 0],
                 'rot': [0, 0, 0],
                 'type': 'positive'}},
     {'filename': 'test_2',
      'preview_rot': [55, 0, 25],
      'kwargs': {'distancex': 0,
                 'distancey': 0,
                 'fitx': 0.25,
                 'fity': 0.25,
                 'pos': [0, 0, 0],
                 'rot': [0, 0, 0],
                 'type': 'positive'}}]

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


