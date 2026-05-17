$fn = 50;

difference() {
	union() {
		cylinder(h = 18, r1 = 10, r2 = 4);
	}
	union();
}
