$fn = 50;

use <../scad_reference/main.scad>;

difference() {
	union() {
		main();
	}
	union();
}
