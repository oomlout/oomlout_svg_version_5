# oobb_nut

**OOBB Geometry Primitives: Nut**

Hexagonal nut pocket with optional through-hole, overhang, and clearance, across all render modes.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| radius_name | Named radius key, e.g. m3, m6. | string | "m3" |
| zz | Z anchor: bottom, top, middle. | string | "bottom" |
| depth | Nut pocket depth in mm. | number | "" |
| overhang | Add overhang support geometry. | bool | False |
| clearance | Clearance extension sides. | string | "" |
| hole | Include a through-hole below the nut. | bool | False |
| extra_clearance | Extra mm added to side clearance height. | number | 0 |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

Fasteners
