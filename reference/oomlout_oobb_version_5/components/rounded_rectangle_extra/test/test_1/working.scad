$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-8.0, 3.0, 0]) {
				cylinder(h = 6, r1 = 4, r2 = 3.0);
			}
			translate(v = [8.0, 3.0, 0]) {
				cylinder(h = 6, r1 = 4, r2 = 3.0);
			}
			translate(v = [-8.0, -3.0, 0]) {
				cylinder(h = 6, r1 = 4, r2 = 3.0);
			}
			translate(v = [8.0, -3.0, 0]) {
				cylinder(h = 6, r1 = 4, r2 = 3.0);
			}
		}
	}
	union();
}
