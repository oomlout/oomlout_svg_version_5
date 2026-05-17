# oobb_screw

**OOBB Geometry Primitives: Screw**

Screw cutout (socket_cap, countersunk, or self_tapping) with optional through-hole, nut pocket, overhang, and clearance.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| radius_name | Named radius key, e.g. m3, m6. | string | "m3" |
| style | Screw head style: socket_cap, countersunk, self_tapping. | string | "socket_cap" |
| depth | Shaft hole depth in mm. | number | 250 |
| zz | Z anchor: none, top, bottom. | string | "none" |
| hole | Include a through shaft hole. | bool | True |
| clearance | Clearance extension sides: top, bottom. | string | "" |
| nut_include | Include a nut pocket. | bool | False |
| overhang | Add overhang geometry. | bool | True |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

Fasteners
