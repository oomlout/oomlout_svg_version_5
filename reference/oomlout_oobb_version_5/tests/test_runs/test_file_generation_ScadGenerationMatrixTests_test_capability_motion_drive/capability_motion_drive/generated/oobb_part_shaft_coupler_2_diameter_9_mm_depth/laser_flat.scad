$fn = 50;


union() {
	translate(v = [0, 0, 0]) {
		projection() {
			intersection() {
				translate(v = [-500, -500, -3.0000000000]) {
					cube(size = [1000, 1000, 0.1000000000]);
				}
				difference() {
					union();
					union() {
						translate(v = [0, 7.5000000000, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [7.5000000000, 0, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [-7.5000000000, 0, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [0, -7.5000000000, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
					}
				}
			}
		}
	}
	translate(v = [0, 110, 0]) {
		projection() {
			intersection() {
				translate(v = [-500, -500, 0.0000000000]) {
					cube(size = [1000, 1000, 0.1000000000]);
				}
				difference() {
					union();
					union() {
						translate(v = [0, 7.5000000000, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [7.5000000000, 0, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [-7.5000000000, 0, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [0, -7.5000000000, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
					}
				}
			}
		}
	}
	translate(v = [0, 220, 0]) {
		projection() {
			intersection() {
				translate(v = [-500, -500, 3.0000000000]) {
					cube(size = [1000, 1000, 0.1000000000]);
				}
				difference() {
					union();
					union() {
						translate(v = [0, 7.5000000000, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [7.5000000000, 0, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [-7.5000000000, 0, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
						translate(v = [0, -7.5000000000, -100.0000000000]) {
							cylinder(h = 200, r = 3.5000000000);
						}
					}
				}
			}
		}
	}
}