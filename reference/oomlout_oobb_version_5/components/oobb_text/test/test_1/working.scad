$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [65, 0, 25]) {
				difference() {
					union() {
						linear_extrude(height = 1.2) {
							text(font = "Candara:Light", halign = "center", size = 10, text = "OOBB", valign = "center");
						}
					}
					union();
				}
			}
		}
	}
	union();
}
