# oobb_cube_hexagon_cutout

**OOBB Geometry Primitives: Cube with Hexagon Cutouts**

A cube with a tiling hexagonal cutout pattern. A solid border is preserved around all edges and between neighbouring cutouts. The hex grid rotation can be adjusted with rotation_cutout.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| size | [x,y,z] outer cube dimensions in mm. | list | (required) |
| hexagon_radius | Base circumradius used to lay out the hex lattice (mm). | number | 10 |
| border_width | Solid border width kept around the cube edges and between cutouts (mm). | number | 10 |
| rotation_cutout | Rotation [rx,ry,rz] for the hex grid in degrees. A scalar still maps to Z for compatibility. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |
| zz | Z anchor point: bottom, top, center/middle. | string | "bottom" |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |

## Category

OOBB Geometry Primitives
