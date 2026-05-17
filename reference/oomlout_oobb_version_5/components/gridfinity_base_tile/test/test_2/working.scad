$fn = 50;

use <gridfinity_base_tile_raw_b06c903fe30da707.scad>;

difference() {
	union() {
		translate(v = [0, 0, -6.1]) {
			gridfinity_base_tile_raw(distancex = 0, distancey = 0, fitx = 0.25, fity = 0.25);
		}
	}
	union();
}
