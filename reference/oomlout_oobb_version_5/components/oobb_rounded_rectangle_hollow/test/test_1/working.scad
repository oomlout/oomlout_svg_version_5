$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 8, r = 5);
							}
						}
					}
					union() {
						hull() {
							translate(v = [-10.0, 5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
							translate(v = [10.0, 5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
							translate(v = [-10.0, -5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
							translate(v = [10.0, -5.0, 0]) {
								cylinder(h = 8, r = 3);
							}
						}
					}
				}
			}
		}
	}
	union();
}
