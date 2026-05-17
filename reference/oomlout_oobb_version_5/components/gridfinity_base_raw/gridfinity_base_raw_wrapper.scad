include <ostat/gridfinity_extended_openscad/modules/functions_environment.scad>
use <ostat/gridfinity_extended_openscad/modules/module_gridfinity_baseplate.scad>
use <ostat/gridfinity_extended_openscad/modules/module_gridfinity_frame_connectors.scad>

function _gridfinity_dimension(value) = is_num(value) ? [value, 0] : value;

function _gridfinity_units(value, unit_size) =
    is_num(value) ? value
    : assert(is_list(value) && len(value) == 2, "Gridfinity dimensions must be numbers or [grid,mm].")
      (value[1] != 0 ? value[1] / unit_size : value[0]);

module gridfinity_base_raw(
    gridfinity_width = 2,
    gridfinity_height = 1,
    gridfinity_depth = undef,
    outer_width = [0, 0],
    outer_depth = [0, 0],
    outer_height = 0,
    oversize_method = "fill",
    position_fill_grid_x = "near",
    position_fill_grid_y = "near",
    position_grid_in_outer_x = "center",
    position_grid_in_outer_y = "center",
    plate_corner_radius = 3.75,
    secondary_corner_radius = 3.75,
    corner_roles = [1, 1, 1, 1],
    enable_magnets = false,
    magnet_size = [6.5, 2.4],
    magnet_z_offset = 0,
    magnet_top_cover = 0,
    magnet_release_method = "none",
    reduced_wall_height = -1,
    reduce_wall_taper = false,
    corner_screw_enabled = false,
    center_screw_enabled = false,
    weighted_enable = false,
    plate_options = "default",
    custom_grid_enabled = false,
    grid_positions = [[1]],
    remove_bottom_taper = false,
    connector_only = false,
    connector_position = "center_wall",
    connector_clip_enabled = false,
    connector_clip_size = 10,
    connector_clip_tolerance = 0.1,
    connector_butterfly_enabled = false,
    connector_butterfly_size = [5, 4, 1.5],
    connector_butterfly_radius = 0.1,
    connector_butterfly_tolerance = 0.1,
    connector_filament_enabled = false,
    connector_filament_diameter = 2,
    connector_filament_length = 8,
    connector_snaps_style = "disabled",
    connector_snaps_clearance = 0.5,
    pitch = [42, 42, 7],
    clearance = [0.5, 0.5, 0],
    set_colour = "enable",
    render_position = "center",
    cut = [0, 0, 0],
    enable_help = false,
    fa = 6,
    fs = 0.4,
    fn = 0,
    random_seed = 0,
    force_render = true
) {
    width_dimension = _gridfinity_dimension(gridfinity_width);
    height_dimension = _gridfinity_dimension(is_undef(gridfinity_depth) ? gridfinity_height : gridfinity_depth);
    outer_width_dimension = _gridfinity_dimension(outer_width);
    outer_depth_dimension = _gridfinity_dimension(outer_depth);

    $fa = fa;
    $fs = fs;
    $fn = fn;

    set_environment(
        width = width_dimension,
        depth = height_dimension,
        clearance = clearance,
        setColour = set_colour,
        help = enable_help,
        render_position = render_position,
        cut = cut,
        pitch = pitch,
        corner_radius = plate_corner_radius,
        randomSeed = random_seed,
        force_render = force_render
    )
    gridfinity_baseplate(
        num_x = _gridfinity_units(width_dimension, pitch[0]),
        num_y = _gridfinity_units(height_dimension, pitch[1]),
        outer_num_x = _gridfinity_units(outer_width_dimension, pitch[0]),
        outer_num_y = _gridfinity_units(outer_depth_dimension, pitch[1]),
        outer_height = outer_height,
        position_fill_grid_x = position_fill_grid_x,
        position_fill_grid_y = position_fill_grid_y,
        position_grid_in_outer_x = position_grid_in_outer_x,
        position_grid_in_outer_y = position_grid_in_outer_y,
        plate_corner_radius = plate_corner_radius,
        secondary_corner_radius = secondary_corner_radius,
        corner_roles = corner_roles,
        magnetSize = enable_magnets ? magnet_size : [0, 0],
        magnetZOffset = magnet_z_offset,
        magnetTopCover = magnet_top_cover,
        magnetReleaseMethod = magnet_release_method,
        reducedWallHeight = reduced_wall_height,
        reduceWallTaper = reduce_wall_taper,
        cornerScrewEnabled = corner_screw_enabled,
        centerScrewEnabled = center_screw_enabled,
        weightedEnable = weighted_enable,
        oversizeMethod = oversize_method,
        plateOptions = plate_options,
        customGridEnabled = custom_grid_enabled,
        gridPositions = grid_positions,
        remove_bottom_taper = remove_bottom_taper,
        frameConnectorSettings = FrameConnectorSettings(
            connectorOnly = connector_only,
            connectorPosition = connector_position,
            connectorClipEnabled = connector_clip_enabled,
            connectorClipSize = connector_clip_size,
            connectorClipTolerance = connector_clip_tolerance,
            connectorButterflyEnabled = connector_butterfly_enabled,
            connectorButterflySize = connector_butterfly_size,
            connectorButterflyRadius = connector_butterfly_radius,
            connectorButterflyTolerance = connector_butterfly_tolerance,
            connectorFilamentEnabled = connector_filament_enabled,
            connectorFilamentDiameter = connector_filament_diameter,
            connectorFilamentLength = connector_filament_length,
            connectorSnapsStyle = connector_snaps_style,
            connectorSnapsClearance = connector_snaps_clearance
        )
    );
}