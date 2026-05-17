# oobb_screw_socket_cap

**OOBB Geometry Primitives: Socket Cap Screw**

Socket-cap screw cutout; wrapper over oobb_screw with style='socket_cap' pre-set.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| radius_name | Named radius key, e.g. m3, m6. | string | "m3" |
| depth | Shaft hole depth in mm. | number | 250 |
| zz | Z anchor: none, top, bottom. | string | "none" |
| hole | Include a through shaft hole. | bool | True |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

Fasteners
