$fn = 50;

difference() {
	union() {
		difference() {
			translate(v = [0, 0, -10]) {
				cylinder(h = 10, r = 6);
			}
			translate(v = [-6, 3, -10]) {
				cube(size = [12, 3, 10]);
			}
		}
	}
	union();
}
