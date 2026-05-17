# oobb_hole_new

**OOBB Geometry Primitives: Hole**

Cylindrical hole with rotation-object support, mode filtering, and named/explicit radius.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| depth | Hole depth in mm. | number | 100 |
| radius_name | Named radius for mode-aware lookup. | string | "" |
| radius | Explicit radius in mm. | number | 0 |
| zz | Z anchor: bottom, top, middle. | string | "middle" |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

OOBB Geometry Primitives
