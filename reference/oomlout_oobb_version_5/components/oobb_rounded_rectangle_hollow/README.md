# oobb_rounded_rectangle_hollow

**OOBB Geometry Primitives: Hollow Rounded Rectangle**

Hollow rounded rectangle (positive outer minus negative inner wall) wrapped in a rotation object.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| size | Outer [x,y,z] dimensions in mm. | list | (required) |
| radius | Corner radius of outer shape. | number | (required) |
| wall_thickness | Wall thickness from outer to inner. | number | 2 |
| extra | Extra variant/modifier string. | string | "" |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

OOBB Geometry Primitives
