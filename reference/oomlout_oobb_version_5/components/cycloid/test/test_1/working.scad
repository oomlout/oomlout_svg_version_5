$fn = 50;

use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;

difference() {
	union() {
		linear_extrude(height = 4) {
			cycloid(lobe_number = 5, radius_offset = 10, radius_pin = 3);
		}
	}
	union();
}
