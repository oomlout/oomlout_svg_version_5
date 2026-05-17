$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						cylinder(h = 12, r = 10);
					}
					union() {
						cylinder(h = 12, r = 8);
					}
				}
			}
		}
	}
	union();
}
