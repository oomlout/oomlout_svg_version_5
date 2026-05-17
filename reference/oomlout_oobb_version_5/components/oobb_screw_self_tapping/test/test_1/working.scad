$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						cylinder(h = 1.5, r = 3.0);
						translate(v = [0, 0, -16.0]) {
							cylinder(h = 16, r = 1.25);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
