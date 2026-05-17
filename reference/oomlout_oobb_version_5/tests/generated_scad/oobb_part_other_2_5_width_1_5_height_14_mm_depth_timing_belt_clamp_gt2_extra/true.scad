$fn = 50;


difference() {
	union() {
		translate(v = [0, 0, -7.0000000000]) {
			hull() {
				translate(v = [-15.2500000000, 7.7500000000, 0]) {
					cylinder(h = 14, r = 5);
				}
				translate(v = [15.2500000000, 7.7500000000, 0]) {
					cylinder(h = 14, r = 5);
				}
				translate(v = [-15.2500000000, -7.7500000000, 0]) {
					cylinder(h = 14, r = 5);
				}
				translate(v = [15.2500000000, -7.7500000000, 0]) {
					cylinder(h = 14, r = 5);
				}
			}
		}
	}
	union() {
		translate(v = [15, 7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.5000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [15, -7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.5000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, 7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.5000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, -7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.5000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15, 7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.5000000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [-15, -7.5000000000, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -50.0000000000]) {
							cylinder(h = 100, r = 1.5000000000);
						}
					}
					union();
				}
			}
		}
	}
}