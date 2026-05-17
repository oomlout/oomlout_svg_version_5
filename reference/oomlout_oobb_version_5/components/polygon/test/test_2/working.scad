$fn = 50;

difference() {
	union() {
		linear_extrude(height = 5) {
			polygon(points = [[0, 0], [12, 0], [18, 8], [9, 16], [-2, 8]]);
		}
	}
	union();
}
