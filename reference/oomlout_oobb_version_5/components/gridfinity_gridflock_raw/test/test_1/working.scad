$fn = 50;

use <../scad_reference/gridfinity_gridflock_raw_generated.scad>;

difference() {
	union() {
		gridfinity_gridflock_raw_generated();
	}
	union();
}
