$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						cylinder(h = 18, r = 12);
					}
					union() {
						cylinder(h = 18, r = 10.8);
					}
				}
			}
		}
	}
	union();
}
