$fn = 50;

difference() {
	union() {
		linear_extrude(height = 4) {
			text(font = "DejaVu Sans:style=Bold", halign = "center", size = 16, text = "A", valign = "center");
		}
	}
	union();
}
