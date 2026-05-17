$fn = 50;

difference() {
	union() {
		linear_extrude(height = 4) {
			polygon(points = [[0, 0], [20, 0], [10, 15]]);
		}
	}
	union();
}
