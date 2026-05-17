$fn = 50;

difference() {
	union() {
		translate(v = [-18.0, -9.0, -4.0]) {
			cube(size = [36, 18, 8]);
		}
	}
	union();
}
