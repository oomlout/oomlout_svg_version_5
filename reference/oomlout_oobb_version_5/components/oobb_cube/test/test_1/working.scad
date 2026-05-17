$fn = 50;

difference() {
	union() {
		translate(v = [-12.0, -12.0, 0]) {
			cube(size = [24, 24, 12]);
		}
	}
	union();
}
