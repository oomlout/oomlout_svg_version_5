$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 18.0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -18.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										linear_extrude(height = 2.5) {
											polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
										}
										translate(v = [0, 0, -100.0]) {
											cylinder(h = 200, r = 1.5);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 0, -1.7]) {
							cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
						}
						cylinder(h = 250, r = 2.9);
						translate(v = [0, 0, -18.0]) {
							cylinder(h = 18, r = 1.5);
						}
					}
					union();
				}
			}
		}
	}
	union();
}
