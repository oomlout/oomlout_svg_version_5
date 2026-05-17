$fn = 50;


difference() {
	union() {
		*color(alpha = 1.0000000000, c = "gray") {
			translate(v = [0, 7, 0]) {
				linear_extrude(height = 1) {
					text(font = "Arial:style=Bold", halign = "center", size = 4.5000000000, text = "COMMENT plate main", valign = "center");
				}
			}
		}
		cylinder(h = 3, r = 7.0000000000);
	}
	union() {
		*color(alpha = 1.0000000000, c = "gray") {
			translate(v = [0, 7, 0]) {
				linear_extrude(height = 1) {
					text(font = "Arial:style=Bold", halign = "center", size = 4.5000000000, text = "COMMENT holes main", valign = "center");
				}
			}
		}
		translate(v = [0, 0, -100]) {
			cylinder(h = 200, r = 3.2500000000);
		}
		translate(v = [0, 0, -100]) {
			cylinder(h = 200, r = 1.8000000000);
		}
	}
}