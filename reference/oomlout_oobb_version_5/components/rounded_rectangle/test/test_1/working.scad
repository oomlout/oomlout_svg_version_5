$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-9.0, 4.0, 0]) {
				cylinder(h = 4, r = 3);
			}
			translate(v = [9.0, 4.0, 0]) {
				cylinder(h = 4, r = 3);
			}
			translate(v = [-9.0, -4.0, 0]) {
				cylinder(h = 4, r = 3);
			}
			translate(v = [9.0, -4.0, 0]) {
				cylinder(h = 4, r = 3);
			}
		}
	}
	union();
}
