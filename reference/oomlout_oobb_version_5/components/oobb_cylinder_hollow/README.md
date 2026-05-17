# oobb_cylinder_hollow

**OOBB Geometry Primitives: Hollow Cylinder**

Hollow cylinder (positive outer minus negative inner) wrapped in a rotation object.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| type | Geometry type: p/positive or n/negative. | string | p |
| r | Outer radius in mm. | number | (required) |
| wall_thickness | Wall thickness for inner cylinder. | number | 2 |
| depth | Cylinder height in mm. | number | (required) |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| rot_x | X rotation in degrees. | number | 0 |
| rot_y | Y rotation in degrees. | number | 0 |
| rot_z | Z rotation in degrees. | number | 0 |

## Category

OOBB Geometry Primitives
