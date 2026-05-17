
module oobb_cube_hexagon_cutout_raw(sx=100, sy=100, sz=10, cut_sx=100, cut_sy=100, cut_sz=10, hex_r=10, border=10, rot_cut=[0, 0, 0]) {
    // Flat-top hexagon tiling:
    //   col_step = hex_r * sqrt(3)   (horizontal centre-to-centre, same row)
    //   row_step = hex_r * 1.5       (vertical   centre-to-centre)
    //   odd rows are offset by col_step/2
    // Shrink the cutout hexagons relative to the lattice pitch so the
    // requested border width also appears between neighbouring cutouts.
    col_step = hex_r * sqrt(3);
    row_step = hex_r * 1.5;
    hex_cut_r = max(hex_r - border / sqrt(3), 0.01);
    usable_x = cut_sx - border * 2;
    usable_y = cut_sy - border * 2;
    cols = ceil(usable_x / col_step) + 2;
    rows = ceil(usable_y / row_step) + 2;

    // Outer cube minus only the hex-hole portion of the inner workspace.
    difference() {
        cube([sx, sy, sz], center=true);
        rotate(rot_cut)
            intersection() {
                // Inner cube clips the cutout region to keep the edge border.
                cube([usable_x, usable_y, cut_sz + 2], center=true);
                // Hex lattice clipped by the inner cube becomes the subtraction volume.
                for (row = [-rows : rows]) {
                    for (col = [-cols : cols]) {
                        x_off = (row % 2 == 0) ? 0 : col_step / 2;
                        translate([col * col_step + x_off, row * row_step, 0])
                            rotate([0, 0, 30])
                                cylinder(r=hex_cut_r, h=cut_sz + 4, center=true, $fn=6);
                    }
                }
            }
    }
}
