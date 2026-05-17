$fn = 50;

difference() {
	union() {
		hull() {
			union() {
				translate(v = [-12.0, 6.0, 4]) {
					cylinder(h = 4, r = 4);
				}
				translate(v = [-12.0, 6.0, 4]) {
					sphere(r = 4);
				}
				translate(v = [-12.0, 6.0, 8]) {
					sphere(r = 4);
				}
			}
			union() {
				translate(v = [12.0, 6.0, 4]) {
					cylinder(h = 4, r = 4);
				}
				translate(v = [12.0, 6.0, 4]) {
					sphere(r = 4);
				}
				translate(v = [12.0, 6.0, 8]) {
					sphere(r = 4);
				}
			}
			union() {
				translate(v = [-12.0, -6.0, 4]) {
					cylinder(h = 4, r = 4);
				}
				translate(v = [-12.0, -6.0, 4]) {
					sphere(r = 4);
				}
				translate(v = [-12.0, -6.0, 8]) {
					sphere(r = 4);
				}
			}
			union() {
				translate(v = [12.0, -6.0, 4]) {
					cylinder(h = 4, r = 4);
				}
				translate(v = [12.0, -6.0, 4]) {
					sphere(r = 4);
				}
				translate(v = [12.0, -6.0, 8]) {
					sphere(r = 4);
				}
			}
		}
	}
	union();
}
