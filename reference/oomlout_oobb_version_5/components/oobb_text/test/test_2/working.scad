$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [65, 0, 25]) {
				difference() {
					union() {
						linear_extrude(height = 1) {
							text(font = "Candara:Light", halign = "center", size = 7, text = "bps", valign = "center");
						}
					}
					union();
				}
			}
		}
	}
	union();
}
