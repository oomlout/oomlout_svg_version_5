$fn = 50;

difference() {
	union() {
		difference() {
			translate(v = [0, 0, -8]) {
				cylinder(h = 8, r = 4);
			}
			translate(v = [-4, 2, -8]) {
				cube(size = [8, 2, 8]);
			}
		}
	}
	union();
}
