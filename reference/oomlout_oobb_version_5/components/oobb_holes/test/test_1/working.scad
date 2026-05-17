$fn = 50;

difference() {
	union();
	union() {
		translate(v = [-15.0, -7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [-15.0, 7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [0.0, -7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [0.0, 7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [15.0, -7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
		translate(v = [15.0, 7.5, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5);
			}
		}
	}
}
