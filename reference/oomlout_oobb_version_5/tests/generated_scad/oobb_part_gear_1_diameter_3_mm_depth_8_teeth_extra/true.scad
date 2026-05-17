$fn = 50;
use <c:/Program Files/OpenSCAD/libraries/MCAD/involute_gears.scad>


difference() {
	union() {
		*color(alpha = 1.0000000000, c = "gray") {
			translate(v = [0, 7, 0]) {
				linear_extrude(height = 1) {
					text(font = "Arial:style=Bold", halign = "center", size = 4.5000000000, text = "COMMENT gear main", valign = "center");
				}
			}
		}
		gear(backlash = 0.5000000000, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0.5000000000, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 8, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
	}
	union() {
		*color(alpha = 1.0000000000, c = "gray") {
			translate(v = [0, 7, 0]) {
				linear_extrude(height = 1) {
					text(font = "Arial:style=Bold", halign = "center", size = 4.5000000000, text = "COMMENT holes main", valign = "center");
				}
			}
		}
		translate(v = [0, 0, -100.0000000000]) {
			cylinder(h = 200, r = 3.0000000000);
		}
	}
}