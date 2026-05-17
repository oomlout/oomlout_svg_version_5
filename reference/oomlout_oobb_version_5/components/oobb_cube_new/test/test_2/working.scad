$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [-15.0, -10.0, -5.0]) {
							cube(size = [30, 20, 10]);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
