$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, -6.0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [0.5, 0, 0]) {
								cylinder(h = 12, r = 3, r1 = 3, r2 = 3);
							}
							translate(v = [-0.5, 0, 0]) {
								cylinder(h = 12, r = 3, r1 = 3, r2 = 3);
							}
						}
					}
					union();
				}
			}
		}
	}
	union();
}
