$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-14.0, 5.0, 0]) {
				cylinder(h = 5, r = 4);
			}
			translate(v = [14.0, 5.0, 0]) {
				cylinder(h = 5, r = 4);
			}
			translate(v = [-14.0, -5.0, 0]) {
				cylinder(h = 5, r = 4);
			}
			translate(v = [14.0, -5.0, 0]) {
				cylinder(h = 5, r = 4);
			}
		}
	}
	union();
}
