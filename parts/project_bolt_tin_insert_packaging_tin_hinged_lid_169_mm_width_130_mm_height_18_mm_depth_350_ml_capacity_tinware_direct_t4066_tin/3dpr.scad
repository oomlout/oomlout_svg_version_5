$fn = 50;

use <../scad_reference/components/gridfinity_base_raw/gridfinity_base_raw_wrapper.scad>;

union() {
	difference() {
		union() {
			hull() {
				translate(v = [-53.25, 73.25, 0]) {
					cylinder(h = 15.25, r = 9.0);
				}
				translate(v = [53.25, 73.25, 0]) {
					cylinder(h = 15.25, r = 9.0);
				}
				translate(v = [-53.25, -73.25, 0]) {
					cylinder(h = 15.25, r = 9.0);
				}
				translate(v = [53.25, -73.25, 0]) {
					cylinder(h = 15.25, r = 9.0);
				}
			}
			hull() {
				translate(v = [-53.25, 73.25, 0]) {
					cylinder(h = 17.5, r = 9);
				}
				translate(v = [53.25, 73.25, 0]) {
					cylinder(h = 17.5, r = 9);
				}
				translate(v = [-53.25, -73.25, 0]) {
					cylinder(h = 17.5, r = 9);
				}
				translate(v = [53.25, -73.25, 0]) {
					cylinder(h = 17.5, r = 9);
				}
			}
			translate(v = [-34.25, -83.75, 1]) {
				cube(size = [68.5, 167.5, 15.0]);
			}
			#translate(v = [-63.75, -54.25, 1]) {
				cube(size = [127.5, 108.5, 4.6]);
			}
		}
		union() {
			hull() {
				translate(v = [-58.75, 69.25, 0]) {
					cylinder(h = 17.5, r = 4.25);
				}
				translate(v = [58.75, 69.25, 0]) {
					cylinder(h = 17.5, r = 4.25);
				}
				translate(v = [-58.75, -69.25, 0]) {
					cylinder(h = 17.5, r = 4.25);
				}
				translate(v = [58.75, -69.25, 0]) {
					cylinder(h = 17.5, r = 4.25);
				}
			}
		}
	}
	union() {
		gridfinity_base_raw(center_screw_enabled = false, clearance = [0.5, 0.5, 0], connector_butterfly_enabled = false, connector_butterfly_radius = 0.1, connector_butterfly_size = [5, 4, 1.5], connector_butterfly_tolerance = 0.1, connector_clip_enabled = false, connector_clip_size = 10, connector_clip_tolerance = 0.1, connector_filament_diameter = 2, connector_filament_enabled = false, connector_filament_length = 8, connector_only = false, connector_position = "center_wall", connector_snaps_clearance = 0.5, connector_snaps_style = "disabled", corner_roles = [1, 1, 1, 1], corner_screw_enabled = false, custom_grid_enabled = false, cut = [0, 0, 0], enable_help = false, enable_magnets = false, fa = 6, fn = 0, force_render = true, fs = 0.4, grid_positions = [[1]], gridfinity_height = 3.5, gridfinity_width = 3, magnet_release_method = "none", magnet_size = [6.5, 2.4], magnet_top_cover = 0, magnet_z_offset = 0, outer_depth = [0, 0], outer_height = 0, outer_width = [0, 0], oversize_method = "fill", pitch = [42, 42, 7], plate_corner_radius = 3.75, plate_options = "default", position_fill_grid_x = "near", position_fill_grid_y = "near", position_grid_in_outer_x = "center", position_grid_in_outer_y = "center", random_seed = 0, reduce_wall_taper = false, reduced_wall_height = -1, remove_bottom_taper = false, render_position = "center", secondary_corner_radius = 3.75, set_colour = "enable", weighted_enable = false);
	}
}
