$fn = 50;

difference() {
	union() {
		linear_extrude(height = 5) {
			polygon(points = [[10.0, 0.0], [-4.999999999999998, 8.660254037844387], [-5.000000000000004, -8.660254037844386]]);
		}
	}
	union();
}
