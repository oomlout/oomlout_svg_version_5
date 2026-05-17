$fn = 50;


difference() {
	union() {
		hull() {
			translate(v = [-17.0000000000, 2.0000000000, 0]) {
				cylinder(h = 1, r = 5);
			}
			translate(v = [17.0000000000, 2.0000000000, 0]) {
				cylinder(h = 1, r = 5);
			}
			translate(v = [-17.0000000000, -2.0000000000, 0]) {
				cylinder(h = 1, r = 5);
			}
			translate(v = [17.0000000000, -2.0000000000, 0]) {
				cylinder(h = 1, r = 5);
			}
		}
		translate(v = [0, -5, 0]) {
			linear_extrude(height = 1) {
				text(font = "DejaVu Sans Mono:style=Bold", halign = "center", size = 19.0000000000, text = "A", valign = "top");
			}
		}
	}
	union() {
		translate(v = [-15.0000000000, 0.0000000000, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 3.0000000000);
			}
		}
		translate(v = [0, 0, -100]) {
			cylinder(h = 200, r = 3.0000000000);
		}
		translate(v = [15.0000000000, 0.0000000000, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 3.0000000000);
			}
		}
		translate(v = [-15.0000000000, 0.0000000000, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5000000000);
			}
		}
		translate(v = [-7.5000000000, 0.0000000000, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5000000000);
			}
		}
		translate(v = [0, 0, -100]) {
			cylinder(h = 200, r = 1.5000000000);
		}
		translate(v = [7.5000000000, 0.0000000000, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5000000000);
			}
		}
		translate(v = [15.0000000000, 0.0000000000, 0]) {
			translate(v = [0, 0, -100]) {
				cylinder(h = 200, r = 1.5000000000);
			}
		}
	}
}