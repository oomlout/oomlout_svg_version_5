$fn = 50;

difference() {
	union() {
		difference() {
			linear_extrude(height = 4) {
				text(font = "DejaVu Sans:style=Bold", halign = "center", size = 16, text = "A", valign = "center");
			}
			translate(v = [0, 0, 1]) {
				linear_extrude(height = 3) {
					offset(r = -1) {
						text(font = "DejaVu Sans:style=Bold", halign = "center", size = 16, text = "A", valign = "center");
					}
				}
			}
		}
	}
	union();
}
