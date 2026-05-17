$fn = 50;

difference() {
	union() {
		rotate_extrude(angle = 360) {
			translate(v = [17.5, 0, 0]) {
				circle(r = 1.5);
			}
		}
	}
	union();
}
