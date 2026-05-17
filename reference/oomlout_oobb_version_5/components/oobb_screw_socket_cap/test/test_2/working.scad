$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										linear_extrude(height = 5) {
											polygon(points = [[5.77, 0.0], [2.8850000000000002, 4.996966579836211], [-2.8849999999999985, 4.996966579836211], [-5.77, 7.066212031080227e-16], [-2.8850000000000025, -4.99696657983621], [2.884999999999996, -4.996966579836213]]);
										}
										translate(v = [0, 0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 0, 22.0]) {
							cylinder(h = 6, r = 5.0);
						}
						cylinder(h = 22, r = 3.0);
					}
					union();
				}
			}
		}
	}
	union();
}
