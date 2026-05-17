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
															translate(v = [0, 0, -1.7]) {
																cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
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
															translate(v = [0, 0, -1.7]) {
																cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
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
