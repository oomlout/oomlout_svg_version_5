$fn = 50;

difference() {
	union() {
		difference() {
			cylinder(h = 18, r1 = 13.5, r2 = 9.5);
			cylinder(h = 18, r1 = 12, r2 = 8);
		}
	}
	union();
}
