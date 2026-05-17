$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						hull() {
							translate(v = [-12.0, 6.0, 0]) {
								cylinder(h = 8, r = 6);
							}
							translate(v = [12.0, 6.0, 0]) {
								cylinder(h = 8, r = 6);
							}
							translate(v = [-12.0, -6.0, 0]) {
								cylinder(h = 8, r = 6);
							}
							translate(v = [12.0, -6.0, 0]) {
								cylinder(h = 8, r = 6);
							}
						}
					}
					union() {
						hull() {
							translate(v = [-12.0, 6.000000000000001, 0]) {
								cylinder(h = 8, r = 4.8);
							}
							translate(v = [12.0, 6.000000000000001, 0]) {
								cylinder(h = 8, r = 4.8);
							}
							translate(v = [-12.0, -6.000000000000001, 0]) {
								cylinder(h = 8, r = 4.8);
							}
							translate(v = [12.0, -6.000000000000001, 0]) {
								cylinder(h = 8, r = 4.8);
							}
						}
					}
				}
			}
		}
	}
	union();
}
