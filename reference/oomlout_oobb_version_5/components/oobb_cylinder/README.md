# oobb_cylinder

**OOBB Geometry Primitives: Cylinder**

Cylinder geometry across all render modes, supporting named, explicit, or dual-end radii and z-centering.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| depth | Cylinder height in mm. | number | 250 |
| radius_name | Named radius for mode-aware lookup. | string | "" |
| radius | Explicit radius in mm. | number | 0 |
| radius_1 | Explicit start radius in mm for tapered cylinders. | number | 0 |
| radius_2 | Explicit end radius in mm for tapered cylinders. | number | 0 |
| zz | Z anchor point: center, bottom, top. | string | "center" |

## Category

OOBB Geometry Primitives
