$fn = 50;
use <c:/Program Files/OpenSCAD/libraries/MCAD/involute_gears.scad>


difference() {
	union() {
		gear(backlash = 0, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		translate(v = [0, 100, 0]) {
			gear(backlash = 0, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0.5000000000, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [0, 200, 0]) {
			gear(backlash = 0, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [0, 300, 0]) {
			gear(backlash = 0, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 2, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [0, 400, 0]) {
			gear(backlash = 0, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = -1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [100, 0, 0]) {
			gear(backlash = 0.5000000000, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [100, 100, 0]) {
			gear(backlash = 0.5000000000, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0.5000000000, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [100, 200, 0]) {
			gear(backlash = 0.5000000000, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [100, 300, 0]) {
			gear(backlash = 0.5000000000, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 2, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [100, 400, 0]) {
			gear(backlash = 0.5000000000, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = -1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [200, 0, 0]) {
			gear(backlash = 1, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [200, 100, 0]) {
			gear(backlash = 1, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0.5000000000, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [200, 200, 0]) {
			gear(backlash = 1, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [200, 300, 0]) {
			gear(backlash = 1, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 2, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [200, 400, 0]) {
			gear(backlash = 1, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = -1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [300, 0, 0]) {
			gear(backlash = 5, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [300, 100, 0]) {
			gear(backlash = 5, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 0.5000000000, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [300, 200, 0]) {
			gear(backlash = 5, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [300, 300, 0]) {
			gear(backlash = 5, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = 2, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
		translate(v = [300, 400, 0]) {
			gear(backlash = 5, bore_diameter = 0, circles = 0, circular_pitch = false, clearance = -1, diametral_pitch = 0.5333333300, flat = false, gear_thickness = 3, hub_diameter = 0, hub_thickness = 0, involute_facets = 0, number_of_teeth = 24, pressure_angle = 20, rim_thickness = 3, rim_width = 0, twist = 0);
		}
	}
	union();
}