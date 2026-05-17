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
											translate(v = [-5.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															cylinder(h = 3, r = 2.9);
														}
														union();
													}
												}
											}
											translate(v = [5.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															cylinder(h = 3, r = 2.9);
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
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								hull() {
									difference() {
										union() {
											translate(v = [-5.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															translate(v = [0, 0, -16.0]) {
																cylinder(h = 16, r = 1.5);
															}
														}
														union();
													}
												}
											}
											translate(v = [5.0, 0, 0]) {
												rotate(a = [0, 0, 0]) {
													difference() {
														union() {
															translate(v = [0, 0, -16.0]) {
																cylinder(h = 16, r = 1.5);
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
