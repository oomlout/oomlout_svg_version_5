$fn = 50;

difference() {
	union() {
		rotate(a = [30, 20, 10]) {
			cube(size = [24, 18, 12]);
		}
	}
	union();
}
