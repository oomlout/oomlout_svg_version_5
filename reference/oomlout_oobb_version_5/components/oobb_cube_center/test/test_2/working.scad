$fn = 50;

difference() {
	union() {
		translate(v = [-9.0, -9.0, -12.0]) {
			cube(size = [18, 18, 24]);
		}
	}
	union();
}
