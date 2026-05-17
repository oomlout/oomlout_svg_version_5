# oobb_tube

**OOBB Geometry Primitives: Tube**

Tube cutout (hollow cylinder) across all render modes, with named/explicit radius and rotation support.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| r | Outer radius in mm. | number | "" |
| radius_name | Named radius for mode-aware lookup. | string | "" |
| wall_thickness | Wall thickness for inner cylinder. | number | 0.5 |
| depth | Tube height in mm. | number | 250 |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

OOBB Geometry Primitives
