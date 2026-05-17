$fn = 50;

use <../scad_reference/oobb_cube_hexagon_cutout_raw.scad>;

difference() {
	union() {
		oobb_cube_hexagon_cutout_raw(border = 2.4, cut_sx = 49.64101615137755, cut_sy = 45.98076211353316, cut_sz = 20.0, hex_r = 4, rot_cut = [0, 0, 30], sx = 40, sy = 30, sz = 20);
	}
	union();
}
