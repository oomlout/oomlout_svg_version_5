$fn = 50;

difference() {
	union() {
		difference() {
			cylinder(h = 18, r = 13.2);
			cylinder(h = 18, r = 12);
		}
	}
	union();
}
