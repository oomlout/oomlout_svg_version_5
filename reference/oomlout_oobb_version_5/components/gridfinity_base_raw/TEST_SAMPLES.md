# gridfinity_base_raw test samples

### Sample 1: `test_1`

- Intent: Default 2x1 Gridfinity Extended baseplate.
- preview_rot: `[55,0,25]`
- kwargs: `{"gridfinity_width": 2, "gridfinity_height": 1, "pos": [0, 0, 0], "rot": [0, 0, 0], "type": "positive"}`
- helper_kwargs: ``
- companion_geometry_kwargs: ``
- Implementation rule: Call `action()` and render the raw-SCAD payload directly.

### Sample 2: `test_2`

- Intent: Fractional crop baseplate with magnets, corner screws, and clip connectors enabled.
- preview_rot: `[55,0,25]`
- kwargs: `{"width": [3.5, 0], "height": [2.2, 0], "oversize_method": "crop", "enable_magnets": true, "corner_screw_enabled": true, "connector_clip_enabled": true, "connector_position": "both", "remove_bottom_taper": true, "pos": [0, 0, 0], "rot": [0, 0, 0], "type": "positive"}`
- helper_kwargs: ``
- companion_geometry_kwargs: ``
- Implementation rule: Call `action()` and render the raw-SCAD payload directly.

## Folder-specific notes

- Notes: This component returns raw SCAD through a local wrapper around vendored Gridfinity Extended baseplate modules, so the test implementation should render the generated result rather than primitive component dicts.