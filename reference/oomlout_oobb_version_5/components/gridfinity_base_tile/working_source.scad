// ===== INFORMATION ===== //
/*
 IMPORTANT: rendering will be better in development builds and not the official release of OpenSCAD, but it makes rendering only take a couple seconds, even for comically large bins.

https://github.com/kennetek/gridfinity-rebuilt-openscad

STANDALONE VERSION - All dependencies inlined
*/

// ===== INLINED DEPENDENCIES ===== //

// ==== BEGIN: src/core/standard.scad ====

// minimum wall thickness
d_wall = 0.95;

// internal fillet radius
r_f2 = 2.8;

// width of divider between compartments
d_div = 1.2;

/**
 * @brief Size of a single gridfinity unit. [Length, Width] In millimeters.
 */
GRID_DIMENSIONS_MM = [42, 42];

// Tollerance to make sure cuts don't leave a sliver behind,
// and that items are properly connected to each other.
TOLLERANCE = 0.02;

// ****************************************
// Magnet / Screw Hole Constants
// ****************************************
LAYER_HEIGHT = 0.2;
MAGNET_HEIGHT = 2;

SCREW_HOLE_RADIUS = 3 / 2;
MAGNET_HOLE_RADIUS = 6.5 / 2;
MAGNET_HOLE_DEPTH = MAGNET_HEIGHT + (LAYER_HEIGHT * 2);

// distance of hole from side of bin
d_hole_from_side=8;

// Based on https://gridfinity.xyz/specification/
HOLE_DISTANCE_FROM_BOTTOM_EDGE = 4.8;

// Meassured diameter in Fusion360.
// Smaller than the magnet to keep it squeezed.
REFINED_HOLE_RADIUS = 5.86 / 2;
REFINED_HOLE_HEIGHT = MAGNET_HEIGHT - 0.1;
// How many layers are between a Gridfinity Refined Hole and the bottom
REFINED_HOLE_BOTTOM_LAYERS = 2;

// Experimentally chosen for a press fit.
MAGNET_HOLE_CRUSH_RIB_INNER_RADIUS = 5.9 / 2;
// Mostly arbitrarily chosen.
// 30 ribs does not print with a 0.4mm nozzle.
// Anything 5 or under produces a hole that is not round.
MAGNET_HOLE_CRUSH_RIB_COUNT = 8;

// Radius to add when chamfering magnet and screw holes.
CHAMFER_ADDITIONAL_RADIUS = 0.8;
CHAMFER_ANGLE = 45;

// When countersinking the baseplate, how much to add to the screw radius.
BASEPLATE_SCREW_COUNTERSINK_ADDITIONAL_RADIUS = 5/2;
BASEPLATE_SCREW_COUNTERBORE_RADIUS = 5.5/2;
BASEPLATE_SCREW_COUNTERBORE_HEIGHT = 3;

// ****************************************
// Tab Constants
// Arbitrarily chosen.
// ****************************************

/**
 * @brief Maximum width of a tab.
 */
TAB_WIDTH_NOMINAL = 42;

 /**
 * @brief How deep the tab protrudes into the bin.
 * @details External code should use `TAB_SIZE.x` instead.
 */
_tab_depth = 15.85;

/**
 * @brief Angle of the support holding up the tab
 */
 _tab_support_angle = 36;

 /**
 * @brief Additional support height, so the end isn't a sharp angle.
 */
 _tab_support_height = 1.2;

_tab_height = tan(_tab_support_angle) * _tab_depth + _tab_support_height;
TAB_POLYGON = [
    [0, 0], // Start
    [0, _tab_height], // Up
    [_tab_depth, _tab_height], //Out
    [_tab_depth, _tab_height - _tab_support_height] // Prevent a sharp angle
    //Implicit back to start
];

/**
 * @brief Size of the tab.
 * @Details "x": How deep the tab protrudes into the bin.
 *          "y": The height of the tab.
 */
TAB_SIZE = TAB_POLYGON[2];

// ****************************************
// Stacking Lip Constants
// Based on https://gridfinity.xyz/specification/
// Also includes a support base.
// ****************************************

/**
 * @Summary Fillet so the stacking lip does not come to a sharp point.
 */
STACKING_LIP_FILLET_RADIUS = 0.6;

/**
 * @Summary Height of the innermost section. In mm.
 * @Details Used to keep the innermost lip from just being a triangle.
 *          Spec implicitly expects wall width to equal stacking lip depth, so does not define this.
 */
STACKING_LIP_SUPPORT_HEIGHT = 1.2;

/**
 * @Summary Stacking lip as defined in the spec.  No support.
 * @Details This is just a line, and will not create a solid polygon.
 */
STACKING_LIP_LINE = [
    [0, 0], // Inner tip
    [0.7, 0.7], // Go out 45 degrees
    [0.7, (0.7+1.8)], // Vertical increase
    [(0.7+1.9), (0.7+1.8+1.9)], // Go out 45 degrees
];

/**
 * @Summary Size of the stacking lip.
 * @Details "x": How deep the stacking lip protrudes into the bin.
 *               Including wall thickness.
 *          "y": The height of the stacking lip.
 * @WARNING: Height does NOT include STACKING_LIP_SUPPORT_HEIGHT.
 */
STACKING_LIP_SIZE = STACKING_LIP_LINE[3];

/**
 * @brief Height of the stacking lip.
 * @details Height does **not** include STACKING_LIP_SUPPORT_HEIGHT.
 */
STACKING_LIP_HEIGHT = STACKING_LIP_SIZE.y;

_stacking_lip_support_angle = 45;

/**
 * @Summary Calculated value for the overall height of the stacking lip.
 *          Including support.
 */
_stacking_lip_support_height_mm =
    STACKING_LIP_SUPPORT_HEIGHT
    + tan(90 - _stacking_lip_support_angle) * STACKING_LIP_SIZE.x;

/**
 * @Summary Stacking lip with a support. Used to create a polygon.
 * @Details Support is so the stacking lip is not floating in mid air when wall width is less than stacking lip depth.
 */
STACKING_LIP = concat(STACKING_LIP_LINE, [
    [STACKING_LIP_SIZE.x-TOLLERANCE, -_stacking_lip_support_height_mm], // Down to support bottom
    [0, -STACKING_LIP_SUPPORT_HEIGHT], // Up and in (to bottom inner support)
    //[0, 0] // Implicit back to start
]);

// ****************************************
// Base constants
// Based on https://gridfinity.xyz/specification/
// ****************************************

/**
 * @Summary Profile of a Gridfinity base as described in the spec.
 * @Details This is just a line, and will not create a solid polygon.
 */
BASE_PROFILE = [
    [0, 0], // Innermost bottom point
    [0.8, 0.8], // Up and out at a 45 degree angle
    [0.8, (0.8+1.8)], // Straight up
    [(0.8+2.15), (0.8+1.8+2.15)] // Up and out at a 45 degree angle
];

/**
 * @brief Maximum [x, y] values/size of the base.
 */
_base_profile_max_mm= BASE_PROFILE[3];

/**
 * @Summary Corner radius of the top of the base.
 */
BASE_TOP_RADIUS = 7.5 / 2;

/**
 * @Summary Size of the top of the base. [Length, Width]
 * @Details Each unit's base is 41.5mm x 41.5mm
 *          Leaving 0.5mm gap with an l_grid of 42
 */
BASE_TOP_DIMENSIONS = [41.5, 41.5];

/**
 * @Summary How much overhang is expected by the standard per base.
 * @Details There should be a 0.5mm gap between each base.
 *          This must be kept constant, even at half/quarter grid sizes.
 *          Otherwise, they won't fit in normal grids.
 */
BASE_GAP_MM = GRID_DIMENSIONS_MM - BASE_TOP_DIMENSIONS;

/**
 * @brief Height of the base profile.
 * @details Does **not** include the structure tying the bases together.
 */
BASE_PROFILE_HEIGHT = _base_profile_max_mm.y;

/**
 * @Summary Height of the base.
 * @details Includes the structure tying the bases together.
 */
BASE_HEIGHT = 7;

/**
 * @Summary Height of the structure tying the bases together.
 */
BASE_BRIDGE_HEIGHT = BASE_HEIGHT - BASE_PROFILE_HEIGHT;

/**
 * @Summary Corner radius of the bottom of the base.
 * @Details This is also how much BASE_PROFILE needs to be translated
 *          to use `sweep_rounded(...)`.
 */
BASE_BOTTOM_RADIUS = BASE_TOP_RADIUS - _base_profile_max_mm.x;

/**
 * @Summary Dimensions of the bottom of the base. [Length, Width]
 * @Details Supports arbitrary top sizes.
 * @param top_dimensions [Length, Width] of the top of the base.
 */
function base_bottom_dimensions(top_dimensions = BASE_TOP_DIMENSIONS) =
    assert(is_list(top_dimensions) && len(top_dimensions) == 2
        && is_num(top_dimensions.x) && is_num(top_dimensions.y))
    top_dimensions
    - 2*[_base_profile_max_mm.x, _base_profile_max_mm.x];

// ***************
// Gridfinity Refined Thumbscrew
// See https://www.printables.com/model/413761-gridfinity-refined
// ***************

BASE_THUMBSCREW_OUTER_DIAMETER=15;
BASE_THUMBSCREW_PITCH=1.5;


// ****************************************
// Weighted Baseplate
// ****************************************

// Baseplate bottom part height (part added with weigthed=true)
bp_h_bot = 6.4;
// Baseplate bottom cutout rectangle size
bp_cut_size = 21.4;
// Baseplate bottom cutout rectangle depth
bp_cut_depth = 4;
// Baseplate bottom cutout rounded thingy width
bp_rcut_width = 8.5;
// Baseplate bottom cutout rounded thingy left
bp_rcut_length = 4.25;
// Baseplate bottom cutout rounded thingy depth
bp_rcut_depth = 2;

// ****************************************

// radius of cutout for skeletonized baseplate
r_skel = 2;
// minimum baseplate thickness (when skeletonized)
h_skel = 1;


// ****************************************
// Deprecated Values
// Will be removed / re-named in the future.
// ****************************************

// height of tab (yaxis, measured from inner wall)
d_tabh = _tab_depth;

// angle of tab
a_tab = _tab_support_angle;

/**
 * @deprecated Use GRID_DIMENSIONS_MM instead.
 */
l_grid = GRID_DIMENSIONS_MM.x;

// ==== END: src/core/standard.scad ====

// ==== BEGIN: helper functions (angles, generic-helpers, shapes) ====

/**
 * @brief `sign` function, but 0 means a positive sign.
 * @description This is useful for applying signs to trig functions.
 * @returns -1 or 1.
 */
function signp(number) =
    assert(is_num(number))
    let(n = sign(number))
    n == 0 ? 1 : n;

/*
 * @brief Convert an angle to between -180 and +180 degrees.
 */
function normalize_angle(angle) =
    assert(is_num(angle))
    let(a = angle%360)
    a > 180 ? a - 360 :
    a < -180 ? a + 360 : a;

/*
 * @brief Convert an angle to between 0 and +360 degrees.
 */
function positive_angle(angle) =
    assert(is_num(angle))
    let(a = angle%360)
    a < 0 ? (a + 360) % 360 : a;

/**
 * @brief Determines the number of fragments in a circle. Aka, Circle resolution.
 * @param r Radius of the circle.
 * @details Recommended function from the manual as a translation of the OpenSCAD function.
 *          Used to improve performance by not rendering every single degree of circles/spheres.
 * @see https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Circle_resolution:_$fa,_$fs,_and_$fn
 */
function get_fragments_from_r(r) =
    assert(r > 0)
    ($fn>0?($fn>=3?$fn:3):ceil(max(min(360/$fa,r*2*PI/$fs),5)));

function clp(x,a,b) = min(max(x,a),b);
function is_even(number) = (number%2)==0;

module copy_mirror(vec=[0,1,0]) {
    children();
    if (vec != [0,0,0])
    mirror(vec)
    children();
}

module pattern_circular(n=2) {
    for (i = [1:n])
    rotate(i*360/n)
    children();
}

/**
 * @brief Unity (no change) affine transformation matrix.
 * @details For use with multmatrix transforms.
 */
unity_matrix = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
];

/**
 * @brief Convert a vector into a unit vector.
 * @returns The unit vector.  Where total magnitude is 1.
 */
function vector_as_unit(vector) = vector / norm(vector);

function _affine_rotate_x(angle_x) = [
    [1,  0, 0, 0],
    [0, cos(angle_x), -sin(angle_x), 0],
    [0, sin(angle_x), cos(angle_x), 0],
    [0, 0, 0, 1]
];

function _affine_rotate_y(angle_y) = [
    [cos(angle_y),  0, sin(angle_y), 0],
    [0, 1, 0, 0],
    [-sin(angle_y), 0, cos(angle_y), 0],
    [0, 0, 0, 1]
];

function _affine_rotate_z(angle_z) = [
    [cos(angle_z), -sin(angle_z), 0, 0],
    [sin(angle_z), cos(angle_z), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
];

/**
 * @brief Affine transformation matrix equivalent of `rotate`
 * @param angle_vector @see `rotate`
 * @details Equivalent to `rotate([0, angle, 0])`
 * @returns An affine transformation matrix for use with `multmatrix()`
 */
function affine_rotate(angle_vector) =
    _affine_rotate_z(angle_vector.z) *
    _affine_rotate_y(angle_vector.y) *
    _affine_rotate_x(angle_vector.x);

/**
 * @brief Affine transformation matrix equivalent of `translate`
 * @param vector @see `translate`
 * @returns An affine transformation matrix for use with `multmatrix()`
 */
function affine_translate(vector) = [
    [1, 0, 0, vector.x],
    [0, 1, 0, vector.y],
    [0, 0, 1, vector.z],
    [0, 0, 0, 1]
];

/**
 * @brief Affine transformation matrix equivalent of `scale`
 * @param vector @see `scale`
 * @returns An affine transformation matrix for use with `multmatrix()`
 */
function affine_scale(vector) = [
    [vector.x, 0, 0, 0],
    [0, vector.y, 0, 0],
    [0, 0, vector.z, 0],
    [0, 0, 0, 1]
];

/**
 * @brief Add something to each element in a list.
 * @param list The list whos elements will be modified.
 * @param to_add
 * @returns A list with `to_add` added to each element in the list.
 */
function foreach_add(list, to_add) =
    assert(is_list(list))
    assert(!is_undef(to_add))
    [for (item = list) item + to_add];

/**
 * @brief Scale each element in a vector by the corresponding element in another vector.
 * @param vector1
 * @param vector2
 * @returns The equivalent of `[vector1.x * vector2.x, vector1.y * vector2.y]`
 */
function vector_scale(vector1, vector2) = assert(len(vector1) == len(vector2))
    [for(i=[0:len(vector1)-1]) vector1[i] * vector2[i] ];


/*
 * @brief If the given vector is a valid 2d vector.
 * @details Only validates the first two elements.
 *          The list could have other things after those.
 */
function is_valid_2d(vector) =
    is_list(vector)
    && len(vector) >= 2
    && is_num(vector[0])
    && is_num(vector[1]);

/*
 * @brief If the given vector is a valid 3d vector.
 * @details This just validates the first three elements.
 *          The list could have other things after those.
 */
function is_valid_3d(vector) =
    is_valid_2d(vector)
    && len(vector) >= 3
    && is_num(vector[2]);

/*
 * @brief If all the elements in a vector are greater than zero.
 */
function is_positive(vector) =
    is_list(vector)
    && min(vector) > 0;

/**
 * @breif Simple helper to print affine matrices in an easier to read manner.
 * @details If a multidimensional matrix is provided, then each item is printed to a separate line.
 * @param object Object to print.
 */
module pprint(object) {
    if(is_list(object) && len(object) != len([for(i=object)each i])) {
        echo("[");
        for(i = object) {
            echo(i);
        };
        echo("]");
    } else {
        echo(object);
    }
}

/**
 * @brief Create a rectangle with rounded corners by sweeping a 2d object along a path.
 * @Details Centered on origin.
 *          Result is on the X,Y plane.
 *          Expects children to be a 2D shape in Quardrant 1 of the X,Y plane.
 * @param size Dimensions of the resulting object.
 *             Either a single number or [width, length]
 */
module sweep_rounded(size) {
    assert((is_num(size) && size > 0) || (
        is_list(size) && len(size) == 2 &&
        is_num(size.x) && size.x > 0 && is_num(size.y) && size.y > 0
        )
    );

    width = is_num(size) ? size : size.x;
    length = is_num(size) ? size : size.y;
    half_width = width/2;
    half_length = length/2;
    path_points = [
        [-half_width, half_length],  //Start
        [half_width, half_length], // Over
        [half_width, -half_length], //Down
        [-half_width, -half_length], // Back over
        [-half_width, half_length]  // Up to start
    ];
    path_vectors = [
        path_points[1] - path_points[0],
        path_points[2] - path_points[1],
        path_points[3] - path_points[2],
        path_points[4] - path_points[3],
    ];
    // These contain the translations, but not the rotations
    // OpenSCAD requires this hacky for loop to get accumulate to work!
    first_translation = affine_translate([path_points[0].y, 0,path_points[0].x]);
    affine_translations = concat([first_translation], [
        for (i = 0, a = first_translation;
            i < len(path_vectors);
            a=a * affine_translate([path_vectors[i].y, 0, path_vectors[i].x]), i=i+1)
        a * affine_translate([path_vectors[i].y, 0, path_vectors[i].x])
    ]);

    // Bring extrusion to the xy plane
    affine_matrix = affine_rotate([90, 0, 90]);

    walls = [
        for (i = [0 : len(path_vectors) - 1])
        affine_matrix * affine_translations[i]
        * affine_rotate([0, atan2(path_vectors[i].y, path_vectors[i].x), 0])
    ];

    union()
    {
        for (i = [0 : len(walls) - 1]){
            multmatrix(walls[i])
            linear_extrude(norm(path_vectors[i]))
            children();

            // Rounded Corners
            multmatrix(walls[i] * affine_rotate([-90, 0, 0]))
            rotate_extrude(angle = 90, convexity = 4)
            children();
        }
    }
}

// ==== Shapes modules ====

/**
 * @brief Create a cone given a radius and an angle.
 * @param bottom_radius Radius of the bottom of the cone.
 * @param angle Angle as measured from the bottom of the cone.
 * @param max_height Optional maximum height.  Cone will be cut off if higher.
 */
module cone(bottom_radius, angle, max_height=0) {
    assert(bottom_radius > 0);
    assert(angle > 0 && angle <= 90);
    assert(max_height >=0);

    height = tan(angle) * bottom_radius;
    if(max_height == 0 || height < max_height) {
        // Normal Cone
        cylinder(h = height, r1 = bottom_radius, r2 = 0, center = false);
    } else {
        top_angle = 90 - angle;
        top_radius = bottom_radius - tan(top_angle) * max_height;
        cylinder(h = max_height, r1 = bottom_radius, r2 = top_radius, center = false);
    }
}

/**
 * @brief Create `square`, with rounded corners.
 * @param size Same as `square`.
 * @param radius Radius of the corners. 0 is the same as just calling `square`
 * @param center Same as `square`.
 */
module rounded_square(size, radius, center = false) {
    assert(is_num(size) ||
        (is_list(size) && (
            (len(size) == 2 && is_num(size.x) && is_num(size.y))
        ))
    );
    assert(is_num(radius) && radius >= 0);
    assert(is_bool(center));

    // Make sure something is produced.
    if (is_num(size)) {
        assert((size/2) > radius);
    } else {
        assert((size.x/2) > radius && (size.y/2 > radius),
            str("Cannot create a rounded_square smaller than the corner radius (", radius,").")
        );
    }
    size_l = is_num(size) ? [size, size] : size;
    diameter_2d = 2 * [radius, radius];

    offset(radius)
    square(size_l - diameter_2d, center = center);
}

// ==== END: helper functions ====

// ===== PARAMETERS ===== //

/* [Setup Parameters] */
$fa = 8;
$fs = 0.25;

/* [General Settings] */
// number of bases along x-axis
gridx = 1;
// number of bases along y-axis
gridy = 1;

/* [Screw Together Settings - Defaults work for M3 and 4-40] */
// screw diameter
d_screw = 3.35;
// screw head diameter
d_screw_head = 5;
// screw spacing distance
screw_spacing = .5;
// number of screws per grid block
n_screws = 1; // [1:3]


/* [Fit to Drawer] */
// minimum length of baseplate along x (leave zero to ignore, will automatically fill area if gridx is zero)
distancex = 0;
// minimum length of baseplate along y (leave zero to ignore, will automatically fill area if gridy is zero)
distancey = 0;

// where to align extra space along x
fitx = 0; // [-1:0.1:1]
// where to align extra space along y
fity = 0; // [-1:0.1:1]


/* [Styles] */

// baseplate styles
style_plate = 0; // [0: thin, 1:weighted, 2:skeletonized, 3: screw together, 4: screw together minimal]


// hole styles
style_hole = 0; // [0:none, 1:countersink, 2:counterbore]

/* [Magnet Hole] */
// Baseplate will have holes for 6mm Diameter x 2mm high magnets.
enable_magnet = true;
// Magnet holes will have crush ribs to hold the magnet.
crush_ribs = true;
// Magnet holes will have a chamfer to ease insertion.
chamfer_holes = true;

// ==== BEGIN: Baseplate modules and hole modules ====

// ****************************************
// Baseplate constants
// Based on https://gridfinity.xyz/specification/
// ****************************************

/**
 * @Summary Length & Width of a single baseplate.
 */
BASEPLATE_DIMENSIONS = [42, 42];
BASEPLATE_DIMENSIONS_HALF = [21, 42];

/**
 * @Summary Minimum height of a baseplate.
 * @Details Ads clearance height to the polygon, and
 *          ensures the base makes contact with the baseplate lip.
 */
BASEPLATE_HEIGHT = 4.631;

/**
 * @Summary Corner diameter of the outside of the baseplate.
 */
BASEPLATE_OUTER_DIAMETER = 8;

/**
 * @Summary Profile of a Gridfinity baseplate as described in the spec.
 * @Details This is just a line, and will not create a solid polygon.
 *          Does NOT include the clearance height.
 */
_BASEPLATE_PROFILE = [
    [0, 0], // Innermost bottom point
    [0.7, 0.7], // Up and out at a 45 degree angle
    [0.7, (0.7+1.8)], // Straight up
    [(0.7+2.15), (0.7+1.8+2.15)], // Up and out at a 45 degree angle
];

// ****************************************
// Calculations
// ****************************************

/**
 * @Summary Corner radius of the outside of the baseplate.
 */
BASEPLATE_OUTER_RADIUS = BASEPLATE_OUTER_DIAMETER / 2;

///**
// * @Summary Corner radius of the inside of the baseplate.
// * @Details This is also how much _BASEPLATE_PROFILE needs to be translated
// *          to use `sweep_rounded(...)`.
// */
BASEPLATE_INNER_RADIUS = BASEPLATE_OUTER_RADIUS - _BASEPLATE_PROFILE[3].x;

/**
 * @Summary Corner diameter of the inside of the baseplate.
 */
BASEPLATE_INNER_DIAMETER = BASEPLATE_INNER_RADIUS * 2;

// ****************************************
// Implementation Functions
// ****************************************

/**
 * @Summary Polygon of the negative of a baseplate.
 * @Details Includes clearance height, as required by spec.
 *          Ready to use with to use `sweep_rounded(...)`.
 * @param height Height of the baseplate's hollow section.
                 Must be the same as or larger than BASEPLATE_HEIGHT.
 */
module _baseplate_cutter_polygon(height) {
    assert(height >= BASEPLATE_HEIGHT, "_baseplate_cutter_polygon: height may not be less than BASEPLATE_HEIGHT");
    // The minimum height between the baseplate lip and anything below it.
    // Needed to make sure the base always makes contact with the baseplate lip.
    _baseplate_clearance_height = height - _BASEPLATE_PROFILE[3].y;
    assert(_baseplate_clearance_height > 0, "Baseplate too short.");

    translated_line = foreach_add(_BASEPLATE_PROFILE,
        [BASEPLATE_INNER_RADIUS, _baseplate_clearance_height]);

    polygon(concat(translated_line, [
            [0, height],  // Go in to form a solid polygon
            [0, 0],  // Straight down
            [translated_line[0].x, 0] // Out to the translated start.
        ]));
}

/**
 * @Summary Inner size of the baseplate.
 * @param size [width, length] of a single baseplate.
 *             Only set if deviating from the standard!
 * @Details To be used with `rounded_square(...)` from generic-helpers.
 * @Example `rounded_square(baseplate_inner_size(), BASEPLATE_INNER_RADIUS, center=true);`
 */
function baseplate_inner_size(size=BASEPLATE_DIMENSIONS) = foreach_add(size, BASEPLATE_INNER_DIAMETER - BASEPLATE_OUTER_DIAMETER);

/**
 * @Summary The negative of a single baseplate.
 * @param size [width, length] of a single baseplate.
 *             Only set if deviating from the standard!
 * @param height Height of the baseplate's hollow section.
                 Must be the same as or larger than BASEPLATE_HEIGHT.
 * @Details Use with `difference()`.
 */
module baseplate_cutter(size=BASEPLATE_DIMENSIONS, height=BASEPLATE_HEIGHT) {
    //aaron add a 42 x 42 cube 5 high
        
    assert(
        is_list(size) &&
        len(size) == 2 &&
        size.x > BASEPLATE_OUTER_DIAMETER &&
        size.y > BASEPLATE_OUTER_DIAMETER,
        "baseplate_cutter: argument 'dimensions' less than BASEPLATE_OUTER_DIAMETER.");
    assert(height >= BASEPLATE_HEIGHT, "baseplate_cutter: height may not be less than BASEPLATE_HEIGHT");

    inner_dimensions = foreach_add(size, -BASEPLATE_OUTER_DIAMETER);

    //Cube's dimensions are set to ensure overlap with `sweep_rounded(...)`
    //without using `rounded_square(...)`.
    inner_size = baseplate_inner_size(size);
    cube_dimensions = [
            inner_size.x - BASEPLATE_INNER_RADIUS,
            inner_size.y - BASEPLATE_INNER_RADIUS,
            height
        ];
    union(){
        sweep_rounded(inner_dimensions){
            _baseplate_cutter_polygon(height);
        }

        translate([0, 0, height/2])
        cube(cube_dimensions, center = true);
    }
}

/**
 * @brief Wave generation function for wrapping a circle.
 * @param t An angle of the circle.  Between 0 and 360 degrees.
 * @param count The number of **full** waves in a 360 degree circle.
 * @param range **Half** the difference between minimum and maximum values.
 * @param vertical_offset Added to the output.
 *                        When wrapping a circle, radius of that circle.
 */
function wave_function(t, count, range, vertical_offset) =
    (sin(t * count) * range) + vertical_offset;

/**
 * @brief A circle with crush ribs to give a tighter press fit.
 * @details Extrude and use as a negative modifier.
 *          Idea based on Slant3D's video at 5:20 https://youtu.be/Bd7Yyn61XWQ?t=320
 *          Implementaiton is completely different.
 *          Important: Lower ribs numbers just result in a deformed circle.
 * @param outer_radius Final outer radius.
 * @param inner_radius Final inner radius.
 * @param ribs Number of crush ribs the circle has.
**/
module ribbed_circle(outer_radius, inner_radius, ribs) {
    assert(outer_radius > 0, "outer_radius must be positive");
    assert(inner_radius > 0, "inner_radius must be positive");
    assert(ribs > 0, "ribs must be positive");
    assert(outer_radius > inner_radius, "outer_radius must be larger than inner_radius");

    wave_range = (outer_radius - inner_radius) / 2;
    wave_vertical_offset = inner_radius + wave_range;
    fragments=get_fragments_from_r(wave_vertical_offset);
    degrees_per_fragment = 360/fragments;

    // Circe with a wave wrapped around it
    wrapped_circle = [ for (i = [0:degrees_per_fragment:360])
        [sin(i), cos(i)] * wave_function(i, ribs, wave_range, wave_vertical_offset)
    ];

    polygon(wrapped_circle);
}

/**
 * @brief A cylinder with crush ribs to give a tighter press fit.
 * @details To be used as the negative for a hole.
 * @see ribbed_circle
 * @param outer_radius Outer Radius of the crush ribs.
 * @param inner_radius Inner Radius of the crush ribs.
 * @param height Cylinder's height.
 * @param ribs Number of crush ribs.
 */
module ribbed_cylinder(outer_radius, inner_radius, height, ribs) {
    assert(height > 0, "height must be positive");
    linear_extrude(height)
    ribbed_circle(
        outer_radius,
        inner_radius,
        ribs
    );
}

/**
 * @brief Make a hole printable without suports.
 * @see https://www.youtube.com/watch?v=W8FbHTcB05w
 * @param inner_radius Radius of the inner hole.
 * @param outer_radius Radius of the outer hole.
 * @param outer_height Height of the outer hole.
 * @param layers Number of layers to make printable.
 * @details This is the negative designed to be cut out of the magnet hole.
 *          Use it with `difference()`.
 *          Special handling is done to support a single layer,
 *          and because the last layer (unless there is only one) has a different shape.
 */
module make_hole_printable(inner_radius, outer_radius, outer_height, layers=2) {
    assert(inner_radius > 0, "inner_radius must be positive");
    assert(outer_radius > 0, "outer_radius must be positive");
    assert(layers > 0);

    height_adjustment = outer_height - (layers * LAYER_HEIGHT);

    // Needed, since the last layer should not be used for calculations,
    // unless there is a single layer.
    calculation_layers = max(layers-1, 1);

    cube_height = LAYER_HEIGHT + 2*TOLLERANCE;
    inner_diameter = 2*(inner_radius+TOLLERANCE);
    outer_diameter = 2*(outer_radius+TOLLERANCE);
    per_layer_difference = (outer_diameter-inner_diameter) / calculation_layers;

    initial_matrix = affine_translate([0, 0, cube_height/2-TOLLERANCE + height_adjustment]);

    // Produces data in the form [affine_matrix, [cube_dimensions]]
    // If layers > 1, the last item produced has an invalid "affine_matrix.y", because it is beyond calculation_layers.
    // That is handled in a special case to avoid doing a check every loop.
    cutout_information = [
        for(i=0; i <= layers; i=i+1)
        [
            initial_matrix * affine_translate([0, 0, (i-1)*LAYER_HEIGHT]) *
                affine_rotate([0, 0, is_even(i) ? 90 : 0]),
            [outer_diameter-per_layer_difference*(i-1),
                outer_diameter-per_layer_difference*i,
                cube_height]
        ]
    ];

    difference() {
        translate([0, 0, layers*cube_height/2 + height_adjustment])
        cube([outer_diameter+TOLLERANCE, outer_diameter+TOLLERANCE, layers*cube_height], center = true);

        for (i = [1 : calculation_layers]){
            data = cutout_information[i];
            multmatrix(data[0])
            cube(data[1], center = true);
        }
        if(layers > 1) {
            data = cutout_information[len(cutout_information)-1];
            multmatrix(data[0])
            cube([data[1].x, data[1].x, data[1].z], center = true);
        }
    }
}

/**
* @brief Refined hole based on Printables @grizzie17's Gridfinity Refined
* @details Magnet is pushed in from +X direction, and held in by friction.
*          Small slit on the bottom allows removing the magnet.
* @see https://www.printables.com/model/413761-gridfinity-refined
*/
module refined_hole() {
    refined_offset = LAYER_HEIGHT * REFINED_HOLE_BOTTOM_LAYERS;

    // Poke through - For removing a magnet using a toothpick
    ptl = refined_offset + LAYER_HEIGHT; // Additional layer just in case
    poke_through_height = REFINED_HOLE_HEIGHT + ptl;
    poke_hole_radius = 2.5;
    magic_constant = 5.60;
    poke_hole_center = [-12.53 + magic_constant, 0, -ptl];

    translate([0, 0, refined_offset])
    union() {
        // Magnet hole
        translate([0, -REFINED_HOLE_RADIUS, 0])
        cube([11, REFINED_HOLE_RADIUS*2, REFINED_HOLE_HEIGHT]);
        cylinder(REFINED_HOLE_HEIGHT, r=REFINED_HOLE_RADIUS);

        // Poke hole
        translate([poke_hole_center.x, -poke_hole_radius/2, poke_hole_center.z])
        cube([10 - magic_constant, poke_hole_radius, poke_through_height]);
        translate(poke_hole_center)
        cylinder(poke_through_height, d=poke_hole_radius);
    }
}

/**
 * @brief Create a screw hole
 * @param radius Radius of the hole.
 * @param height Height of the hole.
 * @param supportless If the hole is designed to be printed without supports.
 * @param chamfer_radius If the hole should be chamfered, then how much should be added to radius.  0 means don't chamfer
 * @param chamfer_angle If the hole should be chamfered, then what angle should it be chamfered at.  Ignored if chamfer_radius is 0.
 */
module screw_hole(radius, height, supportless=false, chamfer_radius=0, chamfer_angle = 45) {
    assert(radius > 0);
    assert(height > 0);
    assert(chamfer_radius >= 0);

    union(){
        difference() {
            cylinder(h = height, r = radius);
            if (supportless) {
                rotate([0, 0, 90])
                make_hole_printable(0.5, radius, height, 3);
            }
        }
        if (chamfer_radius > 0) {
            cone(radius + chamfer_radius, chamfer_angle, height);
        }
    }
}

/**
 * @brief Create an options list used to configure bin holes.
 * @param refined_hole Use gridfinity refined hole type.  Not compatible with "magnet_hole".
 * @param magnet_hole Create a hole for a 6mm magnet.
 * @param screw_hole Create a hole for a M3 screw.
 * @param crush_ribs If the magnet hole should have crush ribs for a press fit.
 * @param chamfer Add a chamfer to the magnet/screw hole.
 * @param supportless If the magnet/screw hole should be printed in such a way that the screw hole does not require supports.
 */
function bundle_hole_options(refined_hole=false, magnet_hole=false, screw_hole=false, crush_ribs=false, chamfer=false, supportless=false) =
    assert(is_bool(refined_hole))
    assert(is_bool(magnet_hole))
    assert(is_bool(screw_hole))
    assert(is_bool(crush_ribs))
    assert(is_bool(chamfer))
    assert(is_bool(supportless))
    assert(!refined_hole
        || (refined_hole && !magnet_hole),
    "magnet_hole is not compatible with refined_hole")
    [
        "hole_options_struct",
        refined_hole,
        magnet_hole,
        screw_hole,
        crush_ribs,
        chamfer,
        supportless
    ];

/**
 * @brief If the object is a "hole_options".
 * @param hole_options The object to check.
 */
function is_hole_options(hole_options) =
    is_list(hole_options)
    && len(hole_options) == 7
    && hole_options[0] == "hole_options_struct";

/**
 * @brief A single magnet/screw hole.  To be cut out of the base.
 * @details Supports multiple options that can be mixed and matched.
 * @pram hole_options @see bundle_hole_options
 * @param o offset Grows or shrinks the final shapes.  Similar to `scale`, but in mm.
 */
module block_base_hole(hole_options, o=0) {
    assert(is_hole_options(hole_options));
    assert(is_num(o));

    // Destructure the options
    refined_hole = hole_options[1];
    magnet_hole = hole_options[2];
    screw_hole = hole_options[3];
    crush_ribs = hole_options[4];
    chamfer = hole_options[5];
    supportless = hole_options[6];

    screw_radius = SCREW_HOLE_RADIUS - (o/2);
    magnet_radius = MAGNET_HOLE_RADIUS - (o/2);
    magnet_inner_radius = MAGNET_HOLE_CRUSH_RIB_INNER_RADIUS - (o/2);
    screw_depth = BASE_HEIGHT - o;
    // If using supportless / printable mode, need to add additional layers, so they can be removed later.
    supportless_additional_layers = screw_hole ? 2 : 3;
    magnet_depth = MAGNET_HOLE_DEPTH - o +
        (supportless ? supportless_additional_layers*LAYER_HEIGHT : 0);

    union() {
        if(refined_hole) {
            refined_hole();
        }

        if(magnet_hole) {
            difference() {
                if(crush_ribs) {
                    ribbed_cylinder(magnet_radius, magnet_inner_radius, magnet_depth, MAGNET_HOLE_CRUSH_RIB_COUNT);
                } else {
                    cylinder(h = magnet_depth, r=magnet_radius);
                }

                if(supportless) {
                    make_hole_printable(
                    screw_hole ? screw_radius : 1, magnet_radius, magnet_depth, supportless_additional_layers);
                }
            }

            if(chamfer) {
                 cone(magnet_radius + CHAMFER_ADDITIONAL_RADIUS, CHAMFER_ANGLE, MAGNET_HOLE_DEPTH - o);
            }
        }
        if(screw_hole) {
            screw_hole(screw_radius, screw_depth, supportless,
                chamfer ? CHAMFER_ADDITIONAL_RADIUS : 0, CHAMFER_ANGLE);
        }
    }
}

// ==== Grid system functions ====

_is_valid_perimeter = function(element_dimensions, perimeter)
    assert(is_list(element_dimensions))
    let(rank=len(element_dimensions))
    is_undef(perimeter) || (
    is_list(perimeter)
    && len(perimeter) == 2 * rank
    && min([for(i=[0:rank-1])
        perimeter[i] + perimeter[i+rank] < element_dimensions[i]
        || (element_dimensions[i] ==0
            && perimeter[i] + perimeter[i+rank] == 0
        ) ? 1 : 0]) != 0
    );

function new_grid(
    num_elements,
    element_dimensions,
    center=false,
    perimeter=undef
    ) =
    assert(is_list(num_elements)
        && len(num_elements) >= 2
        && min(num_elements) >= 0)
    assert(is_list(element_dimensions)
        && len(element_dimensions) == len(num_elements)
        && min(element_dimensions) >= 0)
    assert(is_bool(center))
    assert(_is_valid_perimeter(element_dimensions, perimeter),
    str("perimeter must have ", len(element_dimensions) * 2," items, and must be smaller than an element."))
    [
        "grid_struct",
        num_elements,
        element_dimensions,
        center,
        !is_undef(perimeter) ? perimeter
            : [for(i=[0:2*len(element_dimensions)-1]) 0]
    ];

function is_grid(grid) =
    is_list(grid) && len(grid) == 5
    && grid[0] == "grid_struct";

module pattern_grid(num_elements, element_dimensions, center=false, center_elements=false) {
    grid = new_grid(num_elements, element_dimensions, center);
    grid_foreach(grid, center_elements) {
        children();
    }
}

module grid_foreach(grid, center_elements=false) {
    assert(is_grid(grid), "Not a grid.");
    num_elements = grid[1];

    count = grid_get_element_count(grid);
    rank = len(num_elements);

    for(sequence_number = [0:count-1]) {
        //Goes x -> y -> z
        index = [
            for(d=0,i=sequence_number;
                d<rank;
                i=floor(i/num_elements[d]), d=d+1
            )
            i % num_elements[d]
        ];

        grid_translate(grid, index, center_elements)
        children();
    }
}

function grid_get_element_count(grid) =
    assert(is_grid(grid), "Not a grid.")
    let(num_elements = grid[1])
    let(rank=len(num_elements))
    [for(i=0,a=1;i<rank;a=a*num_elements[i],i=i+1)
        a*num_elements[i]
    ][rank-1];

module grid_translate(grid, index, center=false) {
    element = grid_get_element(grid, index, center);
    $_grid_element = element;

    index_real = grid_element_get_index(element);
    partial_index = index - index_real;
    element_dimensions = grid_get_element_dimensions(grid);
    offset = [for(i=[0:len(index)-1])
        partial_index[i] * element_dimensions[i]
    ];

    translate(grid_element_get_position(element) + offset)
    children();
}

function grid_get_element_dimensions(grid) =
    assert(is_grid(grid), "Not a grid.")
    let(element_dimensions = grid[2])
    element_dimensions;

function grid_get_element(grid, index, center=false) =
    assert(is_grid(grid), "Not a grid.")
    let(num_elements = grid[1])

    assert(is_list(index) && len(index) == len(num_elements),
        str("index must be a list with ", len(num_elements), " items."))
    assert(min(index) >= 0, "index may not contain negative values.")
    assert(min([
            for(d=[0:len(index)-1])
            index[d] < num_elements[d] ? 1 : 0
        ]) == 1,
        str("index must be below ", num_elements))
    assert(is_bool(center))
    let(index_real = [for(i=index) floor(i)])
    [
        "grid_element_struct",
        grid,
        index_real,
        center // Return position as center of the element or not.
    ];

// Grid element accessors (minimal set needed)
function grid_element_get_index(element) =
    assert(is_grid_element(element), "Not a grid element.")
    let(grid=element[1])
    let(index=element[2])
    let(centered=element[3])
    index;

function is_grid_element(element) =
    is_list(element)
    && element[0] == "grid_element_struct"
    && len(element) == 4;

function grid_element_get_position(element) =
    assert(is_grid_element(element), "Not a grid element.")
    let(grid=element[1])
    let(index=element[2])
    let(centered=element[3])
    let(raw_element_dimensions = grid_get_element_dimensions(grid))
    let(raw_element_offset = [
        index.x * raw_element_dimensions.x,
        index.y * raw_element_dimensions.y,
        len(index) >= 3 ? index.z * raw_element_dimensions.z : 0
    ])
    raw_element_offset;

// ==== END: Baseplate modules and hole modules ====

hole_options = bundle_hole_options(refined_hole=false, magnet_hole=enable_magnet, screw_hole=false, crush_ribs=crush_ribs, chamfer=chamfer_holes, supportless=false);

// ===== IMPLEMENTATION ===== //

//color("tomato")
gridfinityBaseplate([gridx, gridy], l_grid, [distancex, distancey], style_plate, hole_options, style_hole, [fitx, fity]);

// ===== CONSTRUCTION ===== //

/**
 * @brief Create a baseplate.
 * @param grid_size_bases Number of Gridfinity bases.
 *        2d Vector. [x, y].
 *        Set to [0, 0] to auto calculate using min_size_mm.
 * @param length X,Y size of a single Gridfinity base.
 * @param min_size_mm Minimum size of the baseplate. [x, y]
 *                    Extra space is filled with solid material.
 *                    Enables "Fit to Drawer."
 * @param sp Baseplate Style
 * @param hole_options
 * @param sh Style of screw hole allowing the baseplate to be mounted to something.
 * @param fit_offset Determines where padding is added.
 */
module gridfinityBaseplate(grid_size_bases, length, min_size_mm, sp, hole_options, sh, fit_offset = [0, 0]) {

    assert(is_list(grid_size_bases) && len(grid_size_bases) == 2,
        "grid_size_bases must be a 2d list");
    assert(is_list(min_size_mm) && len(min_size_mm) == 2,
        "min_size_mm must be a 2d list");
    assert(is_list(fit_offset) && len(fit_offset) == 2,
        "fit_offset must be a 2d list");
    assert(grid_size_bases.x > 0 || min_size_mm.x > 0,
        "Must have positive x grid amount!");
    assert(grid_size_bases.y > 0 || min_size_mm.y > 0,
        "Must have positive y grid amount!");

    additional_height = calculate_offset(sp, hole_options[1], sh);

    // Final height of the baseplate. In mm.
    //baseplate_height_mm = additional_height + BASEPLATE_HEIGHT;
    baseplate_height_mm = BASEPLATE_HEIGHT;

    // Final size in number of bases
    grid_size = [for (i = [0:1])
        grid_size_bases[i] == 0 ? floor(min_size_mm[i]/length) : grid_size_bases[i]];

    // Final size of the base before padding. In mm.
    grid_size_mm = concat(grid_size * length, [baseplate_height_mm]);

    // Final size, including padding. In mm.
    size_mm = [
        max(grid_size_mm.x, min_size_mm.x),
        max(grid_size_mm.y, min_size_mm.y),
        baseplate_height_mm
    ];

    // Amount of padding needed to fit to a specific drawer size. In mm.
    padding_mm = size_mm - grid_size_mm;

    is_padding_needed = padding_mm != [0, 0, 0];

    //Convert the fit offset to percent of how much will be added to the positive axes.
    // -1 : 1 -> 0 : 1
    fit_percent_positive = [for (i = [0:1]) (fit_offset[i] + 1) / 2];

    padding_start_point = -grid_size_mm/2 -
        [
            padding_mm.x * (1 - fit_percent_positive.x),
            padding_mm.y * (1 - fit_percent_positive.y),
            -grid_size_mm.z/2
        ];

    corner_points = [
        padding_start_point + [size_mm.x, size_mm.y, 0],
        padding_start_point + [0, size_mm.y, 0],
        padding_start_point,
        padding_start_point + [size_mm.x, 0, 0],
    ];

    echo(str("Number of Grids per axes (X, Y)]: ", grid_size));
    echo(str("Final size (in mm): ", size_mm));
    if (is_padding_needed) {
        echo(str("Padding +X (in mm): ", padding_mm.x * fit_percent_positive.x));
        echo(str("Padding -X (in mm): ", padding_mm.x * (1 - fit_percent_positive.x)));
        echo(str("Padding +Y (in mm): ", padding_mm.y * fit_percent_positive.y));
        echo(str("Padding -Y (in mm): ", padding_mm.y * (1 - fit_percent_positive.y)));
    }

    screw_together = sp == 3 || sp == 4;
    minimal = sp == 0 || sp == 4;

    difference() {
        union() {
            // Baseplate itself
            
                



                translate(padding_start_point)
                //echo size mm aaron3
                //cube([42,42,5]);
                // union(){
                //     cube([42,42,5], center = false);
                //     cube([44,42,5], center = false);
                // }
                // Replicated Single Baseplate piece
                pattern_grid(grid_size, [length, length], true, true) {
                    if (minimal) {
                        translate([0, 0, -TOLLERANCE/2])
                        baseplate_cutter([length, length], baseplate_height_mm+TOLLERANCE);
                    } 
                }
            
        }

        // Round the outside corners (Including Padding)
        // for(i = [0:len(corner_points) - 1]) {
        //         point = corner_points[i];
        //         translate([
        //         point.x + (BASEPLATE_OUTER_RADIUS * -sign(point.x)),
        //         point.y + (BASEPLATE_OUTER_RADIUS * -sign(point.y)),
        //         0
        //     ])
        //     rotate([0, 0, i*90])
        //     square_baseplate_corner(additional_height, true);
        // }

        if (screw_together) {
            translate([0, 0, additional_height/2])
            cutter_screw_together(grid_size.x, grid_size.y, length);
        }
    }
}

function calculate_offset(style_plate, enable_magnet, style_hole) =
    assert(style_plate >=0 && style_plate <=4)
    let (screw_together = style_plate == 3 || style_plate == 4)
    screw_together ? 6.75 :
    style_plate==0 ? 0 :
    style_plate==1 ? bp_h_bot :
    calculate_offset_skeletonized(enable_magnet, style_hole);

function calculate_offset_skeletonized(enable_magnet, style_hole) =
    h_skel + (enable_magnet ? MAGNET_HOLE_DEPTH : 0) +
    (
        style_hole==0 ? d_screw :
        style_hole==1 ? BASEPLATE_SCREW_COUNTERSINK_ADDITIONAL_RADIUS : // Only works because countersink is at 45 degree angle!
        BASEPLATE_SCREW_COUNTERBORE_HEIGHT
    );

module cutter_weight() {
    union() {
        linear_extrude(bp_cut_depth*2,center=true)
        square(bp_cut_size, center=true);
        pattern_circular(4)
        translate([0,10,0])
        linear_extrude(bp_rcut_depth*2,center=true)
        union() {
            square([bp_rcut_width, bp_rcut_length], center=true);
            translate([0,bp_rcut_length/2,0])
            circle(d=bp_rcut_width);
        }
    }
}
module hole_pattern(){
    pattern_circular(4)
    translate([l_grid/2-d_hole_from_side, l_grid/2-d_hole_from_side, 0]) {
        render();
        children();
    }
}

module cutter_countersink(){
    screw_hole(SCREW_HOLE_RADIUS + TOLLERANCE, 2*BASE_PROFILE_HEIGHT,
        false, BASEPLATE_SCREW_COUNTERSINK_ADDITIONAL_RADIUS);
}

module cutter_counterbore(){
    screw_radius = SCREW_HOLE_RADIUS + TOLLERANCE;
    counterbore_height = BASEPLATE_SCREW_COUNTERBORE_HEIGHT + 2*LAYER_HEIGHT;
    union(){
        cylinder(h=2*BASE_PROFILE_HEIGHT, r=screw_radius);
        difference() {
            cylinder(h = counterbore_height, r=BASEPLATE_SCREW_COUNTERBORE_RADIUS);
            make_hole_printable(screw_radius, BASEPLATE_SCREW_COUNTERBORE_RADIUS, counterbore_height);
        }
    }
}

/**
 * @brief Added or removed from the baseplate to square off or round the corners.
 * @param height Baseplate's height, excluding lip and clearance height.
 * @param subtract If the corner should be scaled to allow subtraction.
 */
module square_baseplate_corner(height=0, subtract=false) {
    assert(height >= 0);
    assert(is_bool(subtract));

    subtract_ammount = subtract ? TOLLERANCE : 0;

    translate([0, 0, -subtract_ammount])
    linear_extrude(height + BASEPLATE_HEIGHT + (2 * subtract_ammount))
    difference() {
        square(BASEPLATE_OUTER_RADIUS + subtract_ammount , center=false);
        // TOLLERANCE needed to prevent a gap
        circle(r=BASEPLATE_OUTER_RADIUS - TOLLERANCE);
    }
}

/**
 * @brief 2d Cutter to skeletonize the baseplate.
 * @param size Width/Length of a single baseplate.  Only set if deviating from the standard!
 * @example difference(){
 *              cube(large_number);
 *              linear_extrude(large_number+TOLLERANCE)
 *              profile_skeleton();
 *          }
 */
module profile_skeleton(size=l_grid) {
    l = baseplate_inner_size([size, size]).x;

    offset(r_skel)
    difference() {
        square(l-2*r_skel, center = true);

        hole_pattern()
        offset(MAGNET_HOLE_RADIUS+r_skel+2)
        square([l,l]);
    }
}

module cutter_screw_together(gx, gy, size = l_grid) {

    screw(gx, gy);
    rotate([0,0,90])
    screw(gy, gx);

    module screw(a, b) {
        copy_mirror([1,0,0])
        translate([a*size/2, 0, 0])
        pattern_grid([1, b], [1, size], true, true)
        pattern_grid([1, n_screws], [1, d_screw_head + screw_spacing], true, true)
        rotate([0,90,0])
        cylinder(h=size/2, d=d_screw, center = true);
    }
}
