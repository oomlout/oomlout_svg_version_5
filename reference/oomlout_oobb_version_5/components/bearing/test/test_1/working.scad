$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, -2.0]) {
			union() {
				difference() {
					cylinder(h = 4, r = 11);
					cylinder(h = 4, r = 4);
				}
				difference() {
					translate(v = [0, 0, -50]) {
						cylinder(h = 100, r = 8.0);
					}
				}
			}
		}
	}
	union();
}
