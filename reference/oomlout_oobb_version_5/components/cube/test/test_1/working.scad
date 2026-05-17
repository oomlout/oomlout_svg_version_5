$fn = 50;

difference() {
	union() {
		cube(size = [20, 20, 20]);
	}
	union();
}
