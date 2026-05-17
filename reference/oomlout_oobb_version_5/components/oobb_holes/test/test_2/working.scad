$fn = 50;

difference() {
	union();
	union() {
		translate(v = [-15.0, -15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, 0.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [-15.0, 15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, -15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, 0.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [0.0, 15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, -15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, 0.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
		translate(v = [15.0, 15.0, -100.0]) {
			cylinder(h = 200, r = 1.5);
		}
	}
}
