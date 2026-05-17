$fn = 50;

difference() {
	union() {
		union() {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.65);
			}
			cylinder(h = 1.7, r1 = 3.05, r2 = 1.65);
		}
	}
	union();
}
