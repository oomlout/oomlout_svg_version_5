$fn = 50;

difference() {
	union() {
		difference() {
			hull() {
				translate(v = [-15.0, 7.0, 0]) {
					cylinder(h = 12, r = 5);
				}
				translate(v = [15.0, 7.0, 0]) {
					cylinder(h = 12, r = 5);
				}
				translate(v = [-15.0, -7.0, 0]) {
					cylinder(h = 12, r = 5);
				}
				translate(v = [15.0, -7.0, 0]) {
					cylinder(h = 12, r = 5);
				}
			}
			translate(v = [0, 0, 0.75]) {
				hull() {
					union() {
						translate(v = [-15.0, 7.0, 4.25]) {
							cylinder(h = 103.5, r = 4.25);
						}
						translate(v = [-15.0, 7.0, 4.25]) {
							sphere(r = 4.25);
						}
						translate(v = [-15.0, 7.0, 107.75]) {
							sphere(r = 4.25);
						}
					}
					union() {
						translate(v = [15.0, 7.0, 4.25]) {
							cylinder(h = 103.5, r = 4.25);
						}
						translate(v = [15.0, 7.0, 4.25]) {
							sphere(r = 4.25);
						}
						translate(v = [15.0, 7.0, 107.75]) {
							sphere(r = 4.25);
						}
					}
					union() {
						translate(v = [-15.0, -7.0, 4.25]) {
							cylinder(h = 103.5, r = 4.25);
						}
						translate(v = [-15.0, -7.0, 4.25]) {
							sphere(r = 4.25);
						}
						translate(v = [-15.0, -7.0, 107.75]) {
							sphere(r = 4.25);
						}
					}
					union() {
						translate(v = [15.0, -7.0, 4.25]) {
							cylinder(h = 103.5, r = 4.25);
						}
						translate(v = [15.0, -7.0, 4.25]) {
							sphere(r = 4.25);
						}
						translate(v = [15.0, -7.0, 107.75]) {
							sphere(r = 4.25);
						}
					}
				}
			}
		}
	}
	union();
}
