# gridfinity_gridflock_raw

**Gridfinity: GridFlock Raw**

Returns a raw OpenSCAD wrapper around the vendored GridFlock segmented baseplate generator, using repo-style public size inputs where `gridfinity_width` is X and `gridfinity_depth` is Y.

## Returns

Raw SCAD geometry component dict.

## Notes

- Backed by the vendored GridFlock source and its vendored `gridfinity-rebuilt-openscad` dependency.
- `plate_size` is derived from the Gridfinity-unit inputs unless you pass an explicit millimeter size.
- The wrapper forces the upstream `test_pattern` off and calls GridFlock's `main()` entrypoint directly.

## Key Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| gridfinity_width | Width in Gridfinity units along X. | number | 2 |
| gridfinity_depth | Depth in Gridfinity units along Y. | number | 2 |
| plate_size | Explicit plate size [x,y] in millimeters. | list | [84,84] |
| bed_size | Printer bed size [x,y] in millimeters. | list | [250,220] |
| baseplate_dimensions | Base Gridfinity cell dimensions [x,y] in millimeters. | list | [42,42] |
| magnets | Enable Gridfinity magnet pockets. | bool | False |
| connector_intersection_puzzle | Enable intersection puzzle connectors between segments. | bool | True |
| connector_edge_puzzle | Enable edge puzzle connectors between segments. | bool | False |
| plate_wall_thickness | Plate wall thickness [north,east,south,west] in millimeters. | list | [0,0,0,0] |
| plate_wall_height | Plate wall heights [above,below] in millimeters. | list | [0,0] |
| solid_base | Solid base thickness in millimeters. | number | 0 |
| edge_adjust | Padding adjustment [north,east,south,west] in millimeters. | list | [0,0,0,0] |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |