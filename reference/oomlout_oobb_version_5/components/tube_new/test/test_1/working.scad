$fn = 50;

difference() {
	union() {
		difference() {
			cylinder(h = 12, r = 12);
			cylinder(h = 12, r = 10);
		}
	}
	union();
}
