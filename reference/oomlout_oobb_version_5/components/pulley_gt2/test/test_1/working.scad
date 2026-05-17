$fn = 50;

use <../../../../pulley_gt2.scad>;

difference() {
	union() {
		pulley_gt2(depth = 6, number_of_teeth = 16);
	}
	union();
}
