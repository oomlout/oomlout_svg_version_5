$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [7.0, 0, 0]) {
				cylinder(h = 6, r = 2.5);
			}
			translate(v = [-7.0, 0, 0]) {
				cylinder(h = 6, r = 2.5);
			}
		}
	}
	union();
}
