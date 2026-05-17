$fn = 50;difference() {
	union() {
		rotate_extrude(angle = 360) {
			translate(v = [12, 0, 0]) {
				rotate(a = [0, 0, -90]) {
					polygon(points = [[3.6, 0], [12, 23], [-12, 23], [-3.6, 0]]);
				}
			}
		}
	}
	union();
}
