# OOBB Objects

| Name | Description | Category |
|------|-------------|----------|
| [_example_shell](_example_shell/) | One sentence describing what this component produces. | OOBB Geometry Primitives |
| [bearing](bearing/) | Legacy opsc bearing profile shape migrated into the component system. | OPSC Mechanical Shapes |
| [bolt](bolt/) | Generates a hex-head bolt with specified size and length. | Fasteners |
| [countersunk](countersunk/) | Legacy opsc countersunk screw shape migrated into the component system. | OPSC Composite Shapes |
| [cube](cube/) | Basic cube primitive exposed through the component system. | OPSC Geometry Primitives |
| [cycloid](cycloid/) | Legacy opsc cycloid shape migrated into the component system. | OPSC Mechanical Shapes |
| [cylinder](cylinder/) | Basic cylinder primitive exposed through the component system. | OPSC Geometry Primitives |
| [d_shaft](d_shaft/) | Legacy opsc D-shaft shape migrated into the component system. | OPSC Mechanical Shapes |
| [gear](gear/) | Legacy opsc involute gear shape migrated into the component system. | OPSC Mechanical Shapes |
| [github_belfryscad_bosl2_screw](github_belfryscad_bosl2_screw/) | Raw OpenSCAD wrapper around BOSL2 `screw()` from `screws.scad`, using the local `git/BOSL2` clone and the repo raw_scad insertion path. | External Library Wrappers |
| [gridfinity_base_raw](gridfinity_base_raw/) | Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended baseplate generator, using repo-style width and height inputs while keeping a broad first-pass upstream option surface. | Gridfinity |
| [gridfinity_base_tile](gridfinity_base_tile/) | Returns the raw OpenSCAD source for a Gridfinity base tile. | Gridfinity |
| [gridfinity_gridflock_raw](gridfinity_gridflock_raw/) | Returns a raw OpenSCAD wrapper around the vendored GridFlock segmented baseplate generator, using repo-style public size inputs where gridfinity_width is X and gridfinity_depth is Y. | Gridfinity |
| [gridfinity_tray_default_label](gridfinity_tray_default_label/) | Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended basic cup, using repo-style public size inputs where gridfinity_width is X, gridfinity_height is Y, and gridfinity_depth is Z. | Gridfinity |
| [gridfinity_tray_fractional_test](gridfinity_tray_fractional_test/) | Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended basic cup, using repo-style public size inputs where gridfinity_width is X, gridfinity_height is Y, and gridfinity_depth is Z. | Gridfinity |
| [gridfinity_tray_raw](gridfinity_tray_raw/) | Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended basic cup, using repo-style public size inputs where gridfinity_width is X, gridfinity_height is Y, and gridfinity_depth is Z. | Gridfinity |
| [gridfinity_tray_raw_offset](gridfinity_tray_raw_offset/) | Returns a local wrapper around gridfinity_tray_raw from the tray_raw component directory, using the same repo-style public size inputs where gridfinity_width is X, gridfinity_height is Y, and gridfinity_depth is Z. | Gridfinity |
| [hole](hole/) | Legacy opsc cylindrical hole shape migrated into the component system. | OPSC Composite Shapes |
| [import_stl](import_stl/) | Imported STL primitive exposed through the component system. | OPSC Geometry Primitives |
| [oobb_circle](oobb_circle/) | Renders a cylinder (solid or cutout) sized to an OOBB grid position. | OOBB Geometry Primitives |
| [oobb_coupler_flanged](oobb_coupler_flanged/) | Flanged coupler with shaft holes and flange M3/M8 cutouts, wrapped in a rotation object. | OOBB Mechanical |
| [oobb_cube](oobb_cube/) | Cube geometry primitive; delegates to oobb_cube_center. | OOBB Geometry Primitives |
| [oobb_cube_center](oobb_cube_center/) | Center-aligned cube that shifts pos by -size/2 on x/y before passing to OpenSCAD. | OOBB Geometry Primitives |
| [oobb_cube_hexagon_cutout](oobb_cube_hexagon_cutout/) | A cube with a tiling hexagonal cutout pattern. A solid border is preserved around all edges and between neighbouring cutouts. The hex grid rotation can be adjusted with rotation_cutout. | OOBB Geometry Primitives |
| [oobb_cube_new](oobb_cube_new/) | Cube with full rotation-object support and mode filtering. | OOBB Geometry Primitives |
| [oobb_cylinder](oobb_cylinder/) | Cylinder geometry across all render modes, supporting named, explicit, or dual-end radii and z-centering. | OOBB Geometry Primitives |
| [oobb_cylinder_hollow](oobb_cylinder_hollow/) | Hollow cylinder (positive outer minus negative inner) wrapped in a rotation object. | OOBB Geometry Primitives |
| [oobb_hole](oobb_hole/) | Cylindrical screw hole for all render modes, resolved from a named or explicit radius. | OOBB Geometry Primitives |
| [oobb_hole_new](oobb_hole_new/) | Cylindrical hole with rotation-object support, mode filtering, and named/explicit radius. | OOBB Geometry Primitives |
| [oobb_holes](oobb_holes/) | Places OOBB-grid-aligned screw holes across a rectangular or circular area using named hole patterns. Use `holes` to choose one or more layouts such as `["all"]`, `["perimeter"]`, or `["single"]` with `loc=[x,y]`. | OOBB Geometry Helpers |
| [oobb_nut](oobb_nut/) | Hexagonal nut pocket with optional through-hole, overhang, and clearance, across all render modes. | Fasteners |
| [oobb_overhang](oobb_overhang/) | Two-layer 3D-print overhang bridge geometry sized to a named radius footprint. | OOBB Geometry Primitives |
| [oobb_plate](oobb_plate/) | OOBB grid-sized plate (cylinder for 1Ã—1, rounded rectangle otherwise) with optional hole pattern. | OOBB Geometry Primitives |
| [oobb_rot](oobb_rot/) | Helper that extracts and returns a [rx,ry,rz] rotation list from kwargs. | OOBB Geometry Helpers |
| [oobb_rounded_rectangle_hollow](oobb_rounded_rectangle_hollow/) | Hollow rounded rectangle (positive outer minus negative inner wall) wrapped in a rotation object. | OOBB Geometry Primitives |
| [oobb_rounded_rectangle_rounded](oobb_rounded_rectangle_rounded/) | Rounded rectangle with rounded top and bottom edges (sphere-swept corners) wrapped in a rotation object. | OOBB Geometry Primitives |
| [oobb_screw](oobb_screw/) | Screw cutout (socket_cap, countersunk, or self_tapping) with optional through-hole, nut pocket, overhang, and clearance. | Fasteners |
| [oobb_screw_countersunk](oobb_screw_countersunk/) | Countersunk screw cutout; wrapper over oobb_screw with style='countersunk' pre-set. | Fasteners |
| [oobb_screw_exact](oobb_screw_exact/) | Part builder that accepts the preferred OOBB screw naming format and maps it to the GitHub BelfrySCAD BOSL2 screw wrapper. | Fasteners |
| [oobb_screw_self_tapping](oobb_screw_self_tapping/) | Self-tapping screw cutout; wrapper over oobb_screw with style='self_tapping' pre-set. | Fasteners |
| [oobb_screw_socket_cap](oobb_screw_socket_cap/) | Socket-cap screw cutout; wrapper over oobb_screw with style='socket_cap' pre-set. | Fasteners |
| [oobb_slice](oobb_slice/) | Large cube slice used to clip/intersect geometry. | OOBB Geometry Primitives |
| [oobb_slot](oobb_slot/) | Slot (two-ended rounded cutout) with rotation-object support, mode filtering, and named/explicit radius. | OOBB Geometry Primitives |
| [oobb_sphere](oobb_sphere/) | Sphere (optionally ellipsoidal via radius_1/radius_2 scale) with z-anchor support. | OOBB Geometry Primitives |
| [oobb_text](oobb_text/) | Legacy OOBB text helper that creates centered extruded text with OOBB defaults. | OOBB Geometry Primitives |
| [oobb_tube](oobb_tube/) | Tube cutout (hollow cylinder) across all render modes, with named/explicit radius and rotation support. | OOBB Geometry Primitives |
| [oobb_tube_new](oobb_tube_new/) | Tube cutout with updated rendering pipeline; identical interface to oobb_tube. | OOBB Geometry Primitives |
| [oring](oring/) | Legacy opsc o-ring profile shape migrated into the component system. | OPSC Mechanical Shapes |
| [polyg](polyg/) | Legacy opsc polygon-prism shape migrated into the component system. | OPSC Composite Shapes |
| [polyg_tube](polyg_tube/) | Legacy opsc polygon tube shape migrated into the component system. | OPSC Composite Shapes |
| [polyg_tube_half](polyg_tube_half/) | Legacy opsc half polygon tube shape migrated into the component system. | OPSC Composite Shapes |
| [polygon](polygon/) | Extruded polygon primitive exposed through the component system. | OPSC Geometry Primitives |
| [pulley_gt2](pulley_gt2/) | Legacy opsc GT2 pulley shape migrated into the component system. | OPSC Mechanical Shapes |
| [raw_scad](raw_scad/) | Imports or inlines raw OpenSCAD modules through the component system. | OPSC Composite Shapes |
| [rounded_octagon](rounded_octagon/) | Legacy opsc rounded octagon shape migrated into the component system. | OPSC Composite Shapes |
| [rounded_rectangle](rounded_rectangle/) | Legacy opsc rounded rectangle shape migrated into the component system. | OPSC Composite Shapes |
| [rounded_rectangle_extra](rounded_rectangle_extra/) | Legacy opsc inset rounded rectangle shape migrated into the component system. | OPSC Composite Shapes |
| [slot](slot/) | Legacy opsc slot shape migrated into the component system. | OPSC Composite Shapes |
| [slot_small](slot_small/) | Legacy opsc short slot helper migrated into the component system. | OPSC Composite Shapes |
| [sphere](sphere/) | Basic sphere primitive exposed through the component system. | OPSC Geometry Primitives |
| [sphere_rectangle](sphere_rectangle/) | Legacy opsc sphere-swept rectangle shape migrated into the component system. | OPSC Composite Shapes |
| [text](text/) | Extruded or planar text primitive exposed through the component system. | OPSC Geometry Primitives |
| [text_hollow](text_hollow/) | Legacy opsc hollow-text shape migrated into the component system. | OPSC Composite Shapes |
| [tray](tray/) | Legacy opsc tray shape migrated into the component system. | OPSC Composite Shapes |
| [tube](tube/) | Legacy opsc tube shape migrated into the component system. | OPSC Composite Shapes |
| [tube_new](tube_new/) | Legacy opsc tapered tube shape migrated into the component system. | OPSC Composite Shapes |
| [vpulley](vpulley/) | Legacy opsc V-pulley profile shape migrated into the component system. | OPSC Mechanical Shapes |
