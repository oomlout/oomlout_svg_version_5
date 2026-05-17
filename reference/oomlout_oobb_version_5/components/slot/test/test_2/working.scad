$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [8.0, 0, 0]) {
				cylinder(h = 6, r1 = 4, r2 = 2);
			}
			translate(v = [-8.0, 0, 0]) {
				cylinder(h = 6, r1 = 4, r2 = 2);
			}
		}
	}
	union();
}
