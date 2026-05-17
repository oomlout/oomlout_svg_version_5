# oobb_sphere

**OOBB Geometry Primitives: Sphere**

Sphere (optionally ellipsoidal via radius_1/radius_2 scale) with z-anchor support.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| radius | Sphere radius in mm. | number | 10 |
| radius_1 | Base radius for ellipsoid scaling. | number | (optional) |
| radius_2 | Z-scale radius for ellipsoid. | number | (optional) |
| zz | Z anchor: bottom, top, middle. | string | "bottom" |

## Category

OOBB Geometry Primitives
