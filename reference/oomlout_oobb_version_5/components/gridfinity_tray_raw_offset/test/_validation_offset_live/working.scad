$fn = 50;

use <../scad_reference/gridfinity_tray_raw_offset_raw.scad>;

difference() {
	union() {
		gridfinity_tray_raw_offset_raw(clearance = [0.5, 0.5, 0], fa = 6, fn = 0, fs = 0.4, gridfinity_depth = 3, gridfinity_height = 1, gridfinity_width = 2, offset_radius = 3, pitch = [42, 42, 7], render_position = "center");
	}
	union();
}
