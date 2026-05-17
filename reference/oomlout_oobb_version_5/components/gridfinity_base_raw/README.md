# gridfinity_base_raw

**Gridfinity: Base Raw**

Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended baseplate generator, using repo-style width and height inputs while keeping a broad first-pass upstream option surface.

## Returns

Raw SCAD geometry component dict.

## Notes

- Backed by a self-contained vendored copy of `gridfinity_extended_openscad` inside this component folder.
- `gridfinity_width` and `gridfinity_height` accept either plain Gridfinity-unit numbers or upstream-style `[grid, mm]` tuples.
- Legacy `gridfinity_depth` and `depth` aliases are still accepted for compatibility.
- The wrapper bridges public width and height inputs into both `set_environment(...)` and the upstream `gridfinity_baseplate(...)` cell-count parameters.

## Key Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| gridfinity_width | Width in Gridfinity units along X, or `[grid,mm]`. | number\|list | 2 |
| gridfinity_height | Height in Gridfinity units along Y, or `[grid,mm]`. | number\|list | 1 |
| outer_width | Outer width in Gridfinity units or `[grid,mm]`. | number\|list | [0,0] |
| outer_depth | Outer depth in Gridfinity units or `[grid,mm]`. | number\|list | [0,0] |
| oversize_method | Oversize method: `fill`, `crop`, or `outer`. | string | "fill" |
| enable_magnets | Enable baseplate magnet pockets. | bool | False |
| magnet_size | Magnet diameter and height `[d,h]` in millimeters. | list | [6.5,2.4] |
| corner_screw_enabled | Enable corner screw holes. | bool | False |
| center_screw_enabled | Enable the center hold-down screw hole. | bool | False |
| weighted_enable | Enable weight cavities in the frame. | bool | False |
| plate_options | Baseplate style option, typically `default` or `cnclaser`. | string | "default" |
| custom_grid_enabled | Enable custom grid cell layout. | bool | False |
| connector_position | Frame connector position: `disabled`, `center_wall`, `intersection`, or `both`. | string | "center_wall" |
| connector_clip_enabled | Enable clip-style frame connectors. | bool | False |
| connector_butterfly_enabled | Enable butterfly frame connectors. | bool | False |
| connector_filament_enabled | Enable filament frame connectors. | bool | False |
| connector_snaps_style | Connector snap style: `disabled`, `larger`, `smaller`, or `wall`. | string | "disabled" |
| pitch | Gridfinity pitch `[x,y,z]` in millimeters. | list | [42,42,7] |
| clearance | Environment clearance `[x,y,z]` in millimeters. | list | [0.5,0.5,0] |
| pos | 3-element `[x,y,z]` position. | list | [0,0,0] |
| rot | Rotation `[rx,ry,rz]` in degrees. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |