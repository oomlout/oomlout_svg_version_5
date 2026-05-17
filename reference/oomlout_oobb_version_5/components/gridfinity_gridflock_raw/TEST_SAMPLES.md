# gridfinity_gridflock_raw test samples

### Sample 1: `test_1`

- Intent: Default 2x2 GridFlock baseplate using derived plate size.
- preview_rot: `[55,0,25]`
- kwargs: `{"gridfinity_width": 2, "gridfinity_depth": 2, "pos": [0, 0, 0], "rot": [0, 0, 0], "type": "positive"}`
- helper_kwargs: ``
- companion_geometry_kwargs: ``
- Implementation rule: Call `action()` and render the raw-SCAD payload directly.

### Sample 2: `test_2`

- Intent: Segmented plate with magnets, edge connectors, and a top plate wall.
- preview_rot: `[55,0,25]`
- kwargs: `{"width": 3, "depth": 2, "bed_size": [100, 100], "magnets": true, "connector_intersection_puzzle": false, "connector_edge_puzzle": true, "plate_wall_thickness": [1, 1, 1, 1], "plate_wall_height": [4, 0], "pos": [0, 0, 0], "rot": [0, 0, 0], "type": "positive"}`
- helper_kwargs: ``
- companion_geometry_kwargs: ``
- Implementation rule: Call `action()` and render the raw-SCAD payload directly.

## Folder-specific notes

- Notes: This component returns raw SCAD source through a wrapper around vendored GridFlock modules, so the test implementation should render the generated result rather than a list of primitive component dicts.