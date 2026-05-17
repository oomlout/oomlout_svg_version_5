$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						cylinder(h = 18, r = 13.2);
					}
					union() {
						cylinder(h = 18, r = 12);
					}
				}
			}
		}
	}
	union();
}
