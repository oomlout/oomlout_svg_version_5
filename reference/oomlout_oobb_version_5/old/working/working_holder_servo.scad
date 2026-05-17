difference() {
    wid = 30;
    hei = 4;
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				hull() {
					translate(v = [wid/2, wid/2, 0]) {
						rotate(a = [0, 0, 0]) {
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder(h = hei, r = 5);
								}
							}
						}
					}
					translate(v = [wid/2, -wid/2, 0]) {
						rotate(a = [0, 0, 0]) {
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder(h = hei, r = 5);
								}
							}
						}
					}
					translate(v = [-wid/2, wid/2, 0]) {
						rotate(a = [0, 0, 0]) {
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder(h = hei, r = 5);
								}
							}
						}
					}
					translate(v = [-wid/2, -wid/2, 0]) {
						rotate(a = [0, 0, 0]) {
							translate(v = [0, 0, 0]) {
								rotate(a = [0, 0, 0]) {
									cylinder(h = hei, r = 5);
								}
							}
						}
					}
				}
			}
		}
	}
    union(){
        horn_hei = 3;
        spac = 7;
        translate([-spac,0,0]){
            cylinder(h=horn_hei, r1=4, r2=5);
            translate([0,0,-50]){
                cylinder(h=100, r=0.5);
            }
        }
        translate([0,0,0]){
            cylinder(h=horn_hei, r1=4, r2=5);
            translate([0,0,-50]){
                cylinder(h=100, r=0.5);
            }
        }
        translate([spac,0,0]){
            cylinder(h=horn_hei, r1=4, r2=5);
            translate([0,0,-50]){
                cylinder(h=100, r=0.5);
            }
        }
    }
}