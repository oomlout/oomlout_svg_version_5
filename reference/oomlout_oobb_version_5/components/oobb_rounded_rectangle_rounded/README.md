# oobb_rounded_rectangle_rounded

**OOBB Geometry Primitives: Rounded Rectangle (Rounded Edges)**

Rounded rectangle with rounded top and bottom edges (sphere-swept corners) wrapped in a rotation object.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| size | Overall [x,y,z] dimensions in mm. | list | [20,10,5] |
| radius | Corner radius of the base shape. | number | 5 |
| radius_rounded | Rounding radius for top/bottom edges. | number | 2.5 |
| extra | Extra variant/modifier string. | string | "" |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

OOBB Geometry Primitives
