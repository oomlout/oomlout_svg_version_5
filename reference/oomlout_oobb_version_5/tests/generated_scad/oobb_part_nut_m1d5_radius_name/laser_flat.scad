$fn = 50;


union() {
	translate(v = [0, 0.0000000000, 0]) {
		projection() {
			intersection() {
				translate(v = [-500, -500, 0.8500000000]) {
					cube(size = [1000, 1000, 0.1000000000]);
				}
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										linear_extrude(height = 1.3000000000) {
											polygon(points = [[1.8464000000, 0.0000000000], [0.9232000000, 1.5990293055], [-0.9232000000, 1.5990293055], [-1.8464000000, 0.0000000000], [-0.9232000000, -1.5990293055], [0.9232000000, -1.5990293055]]);
										}
									}
									union();
								}
							}
						}
					}
					union() {
						cylinder(h = 100, r = 0.8000000000);
					}
				}
			}
		}
	}
}