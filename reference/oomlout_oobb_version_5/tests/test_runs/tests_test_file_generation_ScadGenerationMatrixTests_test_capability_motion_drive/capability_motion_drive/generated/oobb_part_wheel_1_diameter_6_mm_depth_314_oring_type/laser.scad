$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, -3.0000000000]) {
			cylinder(h = 6, r = 11.8750000000);
		}
	}
	union() {
		rotate_extrude(angle = 360) {
			translate(v = [12.8750000000, 0, 0]) {
				circle(r = 2.6650000000);
			}
		}
	}
}