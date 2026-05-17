$fn = 50;

difference() {
	union() {
		linear_extrude(height = 3) {
			text(font = "DejaVu Sans:style=Bold", halign = "center", size = 10, text = "OOBB", valign = "center");
		}
	}
	union();
}
