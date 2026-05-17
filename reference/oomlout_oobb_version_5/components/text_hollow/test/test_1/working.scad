$fn = 50;

difference() {
	union() {
		difference() {
			linear_extrude(height = 3) {
				text(font = "DejaVu Sans:style=Bold", halign = "center", size = 10, text = "OOBB", valign = "center");
			}
			translate(v = [0, 0, -0.8]) {
				linear_extrude(height = 2.2) {
					offset(r = -0.8) {
						text(font = "DejaVu Sans:style=Bold", halign = "center", size = 10, text = "OOBB", valign = "center");
					}
				}
			}
		}
	}
	union();
}
