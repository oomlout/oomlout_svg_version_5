$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [5.0, 0, 0]) {
				cylinder(h = 6, r = 3);
			}
			translate(v = [-5.0, 0, 0]) {
				cylinder(h = 6, r = 3);
			}
		}
	}
	union();
}
