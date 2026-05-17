include <git/BOSL2/std.scad>;

function _gridfinity_mm(value, pitch_value) =
    is_num(value) ? value * pitch_value :
    is_list(value) && len(value) > 1 && value[1] != 0 ? value[1] :
    is_list(value) && len(value) > 0 ? value[0] * pitch_value :
    value * pitch_value;

function _positive(value, minimum = 0.01) = max(value, minimum);

function _rectangle_path(size_xy) = [
    [-size_xy[0] / 2, -size_xy[1] / 2],
    [ size_xy[0] / 2, -size_xy[1] / 2],
    [ size_xy[0] / 2,  size_xy[1] / 2],
    [-size_xy[0] / 2,  size_xy[1] / 2]
];

function _base_corner_radius(size_xy, nominal_radius = 3.75) =
    max(0, min(nominal_radius, size_xy[0] / 2 - 0.01, size_xy[1] / 2 - 0.01));

function _rounded_rectangle_path(size_xy, corner_radius) =
    corner_radius <= 0 ? _rectangle_path(size_xy) :
    let(
        core_size = [
            _positive(size_xy[0] - corner_radius * 2),
            _positive(size_xy[1] - corner_radius * 2)
        ]
    )
    offset(_rectangle_path(core_size), r = corner_radius, closed = true);

function _tray_profile_path(size_xy, offset_radius) =
    let(
        corner_radius = _base_corner_radius(size_xy),
        rounded_path = _rounded_rectangle_path(size_xy, corner_radius)
    )
    offset_radius == 0 ? rounded_path : offset(rounded_path, r = offset_radius, closed = true);

function _footprint_size(size_xy, offset_radius) = [
    _positive(size_xy[0] + offset_radius * 2),
    _positive(size_xy[1] + offset_radius * 2)
];

function _render_position_offset(render_position, footprint_size, pitch) =
    render_position == "center" ? [-footprint_size[0] / 2, -footprint_size[1] / 2, 0] :
    render_position == "zero" ? [0, 0, 0] :
    [-pitch[0] / 2, -pitch[1] / 2, 0];

module gridfinity_tray_raw_offset_raw(
    gridfinity_width = 2,
    gridfinity_height = 1,
    gridfinity_depth = 3,
    offset_radius = 0,
    pitch = [42, 42, 7],
    clearance = [0.5, 0.5, 0],
    render_position = "center",
    fa = 6,
    fs = 0.4,
    fn = 0
) {
    width_mm = _gridfinity_mm(gridfinity_width, pitch[0]);
    depth_mm = _gridfinity_mm(gridfinity_height, pitch[1]);
    height_mm = _gridfinity_mm(gridfinity_depth, pitch[2]);

    tray_size = [
        _positive(width_mm - clearance[0]),
        _positive(depth_mm - clearance[1])
    ];
    footprint_size = _footprint_size(tray_size, offset_radius);
    profile_path = _tray_profile_path(tray_size, offset_radius);

    $fa = fa;
    $fs = fs;
    $fn = fn;

    translate(_render_position_offset(render_position, footprint_size, pitch))
        linear_extrude(height = _positive(height_mm))
            polygon(profile_path);
}
