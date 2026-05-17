$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, -3.5]) {
			union() {
				difference() {
					cylinder(h = 7, r = 22);
					cylinder(h = 7, r = 8);
				}
				difference() {
					translate(v = [0, 0, -50]) {
						cylinder(h = 100, r = 15.5);
					}
				}
			}
		}
	}
	union();
}
