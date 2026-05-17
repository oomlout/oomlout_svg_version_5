$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [7.0, 0, 0]) {
				cylinder(h = 6, r = 3, r1 = 3, r2 = 3);
			}
			translate(v = [-7.0, 0, 0]) {
				cylinder(h = 6, r = 3, r1 = 3, r2 = 3);
			}
		}
	}
	union();
}
