$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 2]) {
							hull() {
								translate(v = [-10.0, 5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
								translate(v = [10.0, 5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
								translate(v = [-10.0, -5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
								translate(v = [10.0, -5.0, 0]) {
									cylinder(h = 4, r = 5);
								}
							}
						}
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 2, r = 3);
							}
						}
						translate(v = [0, 0, 6]) {
							hull() {
								translate(v = [-10.0, 5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
								translate(v = [10.0, 5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
								translate(v = [-10.0, -5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
								translate(v = [10.0, -5.0, 0]) {
									cylinder(h = 2, r = 3);
								}
							}
						}
						translate(v = [13.0, 5.0, 2.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [-13.0, 5.0, 2.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [13.0, 5.0, 6.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [-13.0, 5.0, 6.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 10, r = 2);
							}
						}
						translate(v = [-10.0, 8.0, 2.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, -8.0, 2.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, 8.0, 6.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, -8.0, 6.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 20, r = 2);
							}
						}
						translate(v = [-10.0, -5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, -5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, 5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, 5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, -5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, -5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [10.0, 5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, 5.0, 6]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
						translate(v = [-10.0, -5.0, 2]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 2.0);
								}
							}
						}
					}
					union();
				}
			}
		}
	}
	union();
}
