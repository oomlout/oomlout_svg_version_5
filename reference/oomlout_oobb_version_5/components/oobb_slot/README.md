# oobb_slot

**OOBB Geometry Primitives: Slot**

Slot (two-ended rounded cutout) with rotation-object support, mode filtering, and named/explicit radius.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| depth | Slot depth in mm. | number | 250 |
| radius | Slot end-cap radius in mm. | number | "" |
| radius_name | Named radius for mode-aware lookup. | string | "" |
| zz | Z anchor: middle, bottom, top. | string | "middle" |
| mode | Render modes: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

OOBB Geometry Primitives
