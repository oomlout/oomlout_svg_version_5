// Simplified standalone Gridfinity base tile.
// This version keeps only the geometry and parameters used by the current model.

/* [Setup Parameters] */
$fa = 8;
$fs = 0.25;

/* [General Settings] */
gridx = 1;
gridy = 1;

/* [Fit to Drawer] */
distancex = 0;
distancey = 0;
fitx = 0; // [-1:0.1:1]
fity = 0; // [-1:0.1:1]

GRID_SIZE_MM = 42;
TOLLERANCE = 0.02;

BASEPLATE_HEIGHT = 4.631;
BASEPLATE_OUTER_DIAMETER = 8;
BASEPLATE_OUTER_RADIUS = BASEPLATE_OUTER_DIAMETER / 2;

_BASEPLATE_PROFILE = [
    [0, 0],
    [0.7, 0.7],
    [0.7, 2.5],
    [2.85, 4.65]
];

BASEPLATE_INNER_RADIUS = BASEPLATE_OUTER_RADIUS - _BASEPLATE_PROFILE[3].x;
BASEPLATE_INNER_DIAMETER = BASEPLATE_INNER_RADIUS * 2;

function foreach_add(list, to_add) =
    [for (item = list) item + to_add];

function _affine_rotate_x(angle_x) = [
    [1, 0, 0, 0],
    [0, cos(angle_x), -sin(angle_x), 0],
    [0, sin(angle_x), cos(angle_x), 0],
    [0, 0, 0, 1]
];

function _affine_rotate_y(angle_y) = [
    [cos(angle_y), 0, sin(angle_y), 0],
    [0, 1, 0, 0],
    [-sin(angle_y), 0, cos(angle_y), 0],
    [0, 0, 0, 1]
];

function _affine_rotate_z(angle_z) = [
    [cos(angle_z), -sin(angle_z), 0, 0],
    [sin(angle_z), cos(angle_z), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
];

function affine_rotate(angle_vector) =
    _affine_rotate_z(angle_vector.z) *
    _affine_rotate_y(angle_vector.y) *
    _affine_rotate_x(angle_vector.x);

function affine_translate(vector) = [
    [1, 0, 0, vector.x],
    [0, 1, 0, vector.y],
    [0, 0, 1, vector.z],
    [0, 0, 0, 1]
];

module sweep_rounded(size) {
    width = is_num(size) ? size : size.x;
    length = is_num(size) ? size : size.y;
    half_width = width / 2;
    half_length = length / 2;

    path_points = [
        [-half_width, half_length],
        [half_width, half_length],
        [half_width, -half_length],
        [-half_width, -half_length],
        [-half_width, half_length]
    ];

    path_vectors = [
        path_points[1] - path_points[0],
        path_points[2] - path_points[1],
        path_points[3] - path_points[2],
        path_points[4] - path_points[3]
    ];

    first_translation = affine_translate([path_points[0].y, 0, path_points[0].x]);
    affine_translations = concat([first_translation], [
        for (
            i = 0, a = first_translation;
            i < len(path_vectors);
            a = a * affine_translate([path_vectors[i].y, 0, path_vectors[i].x]), i = i + 1
        )
        a * affine_translate([path_vectors[i].y, 0, path_vectors[i].x])
    ]);

    affine_matrix = affine_rotate([90, 0, 90]);

    walls = [
        for (i = [0 : len(path_vectors) - 1])
        affine_matrix * affine_translations[i]
        * affine_rotate([0, atan2(path_vectors[i].y, path_vectors[i].x), 0])
    ];

    union() {
        for (i = [0 : len(walls) - 1]) {
            multmatrix(walls[i])
            linear_extrude(norm(path_vectors[i]))
            children();

            multmatrix(walls[i] * affine_rotate([-90, 0, 0]))
            rotate_extrude(angle = 90, convexity = 4)
            children();
        }
    }
}

function baseplate_inner_size(size = [GRID_SIZE_MM, GRID_SIZE_MM]) =
    foreach_add(size, BASEPLATE_INNER_DIAMETER - BASEPLATE_OUTER_DIAMETER);

module _baseplate_cutter_polygon(height) {
    clearance_height = height - _BASEPLATE_PROFILE[3].y;
    translated_line = foreach_add(
        _BASEPLATE_PROFILE,
        [BASEPLATE_INNER_RADIUS, clearance_height]
    );

    polygon(concat(translated_line, [
        [0, height],
        [0, 0],
        [translated_line[0].x, 0]
    ]));
}

module baseplate_cutter(size = [GRID_SIZE_MM, GRID_SIZE_MM], height = BASEPLATE_HEIGHT) {
    inner_dimensions = foreach_add(size, -BASEPLATE_OUTER_DIAMETER);
    inner_size = baseplate_inner_size(size);
    cube_dimensions = [
        inner_size.x - BASEPLATE_INNER_RADIUS,
        inner_size.y - BASEPLATE_INNER_RADIUS,
        height
    ];

    union() {
        sweep_rounded(inner_dimensions) {
            _baseplate_cutter_polygon(height);
        }

        translate([0, 0, height / 2])
        cube(cube_dimensions, center = true);
    }
}

module gridfinity_baseplate(grid_size_bases, length, min_size_mm, fit_offset = [0, 0]) {
    grid_size = [
        grid_size_bases.x == 0 ? floor(min_size_mm.x / length) : grid_size_bases.x,
        grid_size_bases.y == 0 ? floor(min_size_mm.y / length) : grid_size_bases.y
    ];

    grid_size_mm = concat(grid_size * length, [BASEPLATE_HEIGHT]);
    size_mm = [
        max(grid_size_mm.x, min_size_mm.x),
        max(grid_size_mm.y, min_size_mm.y),
        BASEPLATE_HEIGHT
    ];
    padding_mm = size_mm - grid_size_mm;

    fit_percent_positive = [
        (fit_offset.x + 1) / 2,
        (fit_offset.y + 1) / 2
    ];

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
            translate([
                (x + 0.5) * length,
                (y + 0.5) * length,
                -TOLLERANCE / 2
            ])
            baseplate_cutter([length, length], BASEPLATE_HEIGHT + TOLLERANCE);
        }
    }
}

gridfinity_baseplate([gridx, gridy], GRID_SIZE_MM, [distancex, distancey], [fitx, fity]);
