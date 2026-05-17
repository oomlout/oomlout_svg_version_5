$fn = 50;

use <../../../../reference/oomlout_opsc_version_3/cycloid.scad>;

difference() {
	union() {
		linear_extrude(height = 4) {
			offset(r = 0.8) {
				cycloid(lobe_number = 6, radius_offset = 12, radius_pin = 3);
			}
		}
	}
	union();
}
