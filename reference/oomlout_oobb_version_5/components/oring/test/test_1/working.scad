$fn = 50;

difference() {
	union() {
		rotate_extrude(angle = 360) {
			translate(v = [11.0, 0, 0]) {
				circle(r = 1.0);
			}
		}
	}
	union();
}
