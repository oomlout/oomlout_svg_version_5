$fn = 50;

difference() {
	union() {
		difference() {
			hull() {
				translate(v = [-11.0, 6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
				translate(v = [11.0, 6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
				translate(v = [-11.0, -6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
				translate(v = [11.0, -6.0, 0]) {
					cylinder(h = 10, r = 4);
				}
			}
			translate(v = [0, 0, 0.6]) {
				hull() {
					union() {
						translate(v = [-10.0, 5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [-10.0, 5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [-10.0, 5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
					union() {
						translate(v = [10.0, 5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [10.0, 5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [10.0, 5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
					union() {
						translate(v = [-10.0, -5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [-10.0, -5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [-10.0, -5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
					union() {
						translate(v = [10.0, -5.0, 4.4]) {
							cylinder(h = 101.2, r = 4.4);
						}
						translate(v = [10.0, -5.0, 4.4]) {
							sphere(r = 4.4);
						}
						translate(v = [10.0, -5.0, 105.6]) {
							sphere(r = 4.4);
						}
					}
				}
			}
		}
	}
	union();
}
