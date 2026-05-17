$fn = 50;

difference() {
	union() {
		import(file = "test_assets/sample_block.stl", origin = [0, 0]);
	}
	union();
}
