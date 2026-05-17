$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [25, 20, 10]) {
				difference() {
					union() {
						translate(v = [-12.0, -9.0, -6.0]) {
							cube(size = [24, 18, 12]);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
