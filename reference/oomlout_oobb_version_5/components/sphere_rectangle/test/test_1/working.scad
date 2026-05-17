$fn = 50;

difference() {
	union() {
		hull() {
			union() {
				translate(v = [-9.0, 5.0, 3]) {
					cylinder(h = 4, r = 3);
				}
				translate(v = [-9.0, 5.0, 3]) {
					sphere(r = 3);
				}
				translate(v = [-9.0, 5.0, 7]) {
					sphere(r = 3);
				}
			}
			union() {
				translate(v = [9.0, 5.0, 3]) {
					cylinder(h = 4, r = 3);
				}
				translate(v = [9.0, 5.0, 3]) {
					sphere(r = 3);
				}
				translate(v = [9.0, 5.0, 7]) {
					sphere(r = 3);
				}
			}
			union() {
				translate(v = [-9.0, -5.0, 3]) {
					cylinder(h = 4, r = 3);
				}
				translate(v = [-9.0, -5.0, 3]) {
					sphere(r = 3);
				}
				translate(v = [-9.0, -5.0, 7]) {
					sphere(r = 3);
				}
			}
			union() {
				translate(v = [9.0, -5.0, 3]) {
					cylinder(h = 4, r = 3);
				}
				translate(v = [9.0, -5.0, 3]) {
					sphere(r = 3);
				}
				translate(v = [9.0, -5.0, 7]) {
					sphere(r = 3);
				}
			}
		}
	}
	union();
}
