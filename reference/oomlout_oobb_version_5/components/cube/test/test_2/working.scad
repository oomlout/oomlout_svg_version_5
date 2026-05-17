$fn = 50;

difference() {
	union() {
		cube(size = [30, 18, 10]);
	}
	union();
}
