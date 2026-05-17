$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								hull() {
									difference() {
										union() {
											translate(v = [-6.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															translate(v = [0, 0, -1.5]) {
																cylinder(h = 1.5, r = 3.0);
															}
														}
														union();
													}
												}
											}
											translate(v = [6.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															translate(v = [0, 0, -1.5]) {
																cylinder(h = 1.5, r = 3.0);
															}
														}
														union();
													}
												}
											}
										}
										union();
									}
								}
							}
						}
					}
					union();
				}
			}
		}
	}
	union();
}
