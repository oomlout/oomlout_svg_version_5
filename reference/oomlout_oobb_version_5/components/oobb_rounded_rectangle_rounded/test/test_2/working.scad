$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 3]) {
							hull() {
								translate(v = [-12.0, 6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
								translate(v = [12.0, 6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
								translate(v = [-12.0, -6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
								translate(v = [12.0, -6.0, 0]) {
									cylinder(h = 4, r = 6);
								}
							}
						}
						hull() {
							translate(v = [-12.0, 6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
							translate(v = [12.0, 6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
							translate(v = [-12.0, -6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
							translate(v = [12.0, -6.0, 0]) {
								cylinder(h = 3, r = 3);
							}
						}
						translate(v = [0, 0, 7]) {
							hull() {
								translate(v = [-12.0, 6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
								translate(v = [12.0, 6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
								translate(v = [-12.0, -6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
								translate(v = [12.0, -6.0, 0]) {
									cylinder(h = 3, r = 3);
								}
							}
						}
						translate(v = [15.0, 6.0, 3.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [-15.0, 6.0, 3.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [15.0, 6.0, 7.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [-15.0, 6.0, 7.0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 12, r = 3);
							}
						}
						translate(v = [-12.0, 9.0, 3.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, -9.0, 3.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, 9.0, 7.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, -9.0, 7.0]) {
							rotate(a = [0, 90, 0]) {
								cylinder(h = 24, r = 3);
							}
						}
						translate(v = [-12.0, -6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, -6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, 6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, 6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, -6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, -6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [12.0, 6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, 6.0, 7]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
								}
							}
						}
						translate(v = [-12.0, -6.0, 3]) {
							rotate_extrude(angle = 360) {
								translate(v = [3.0, 0, 0]) {
									circle(r = 3.0);
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
