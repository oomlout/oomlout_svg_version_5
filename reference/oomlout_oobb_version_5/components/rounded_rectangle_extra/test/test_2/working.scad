$fn = 50;

difference() {
	union() {
		rotate(a = [0, 180, 0]) {
			hull() {
				translate(v = [-8.0, 3.0, 0]) {
					rotate(a = [0, 180, 0]) {
						cylinder(h = 6, r1 = 3.0, r2 = 4);
					}
				}
				translate(v = [8.0, 3.0, 0]) {
					rotate(a = [0, 180, 0]) {
						cylinder(h = 6, r1 = 3.0, r2 = 4);
					}
				}
				translate(v = [-8.0, -3.0, 0]) {
					rotate(a = [0, 180, 0]) {
						cylinder(h = 6, r1 = 3.0, r2 = 4);
					}
				}
				translate(v = [8.0, -3.0, 0]) {
					rotate(a = [0, 180, 0]) {
						cylinder(h = 6, r1 = 3.0, r2 = 4);
					}
				}
			}
		}
	}
	union();
}
