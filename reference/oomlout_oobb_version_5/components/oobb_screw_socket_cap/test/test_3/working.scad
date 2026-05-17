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
											translate(v = [-7.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															translate(v = [0, 0, -3]) {
																cylinder(h = 3, r = 2.9);
															}
														}
														union();
													}
												}
											}
											translate(v = [7.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															translate(v = [0, 0, -3]) {
																cylinder(h = 3, r = 2.9);
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
