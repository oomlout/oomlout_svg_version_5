$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [5.657, 5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [-5.657, -5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [5.657, -5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [-5.657, 5.657, -100.0]) {
							cylinder(h = 200, r = 1.5);
						}
						translate(v = [0, 0, -100.0]) {
							cylinder(h = 200, r = 4.0);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
