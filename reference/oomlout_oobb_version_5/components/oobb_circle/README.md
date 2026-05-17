# oobb_circle

**OOBB Geometry Primitives: Circle**

Renders a cylinder (solid or cutout) sized to an OOBB grid position.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| width | Width in OOBB grid units. | number | 1 |
| height | Height in OOBB grid units. | number | 1 |
| depth | Z depth (height) of the cylinder in mm. | number | 3 |
| extra_mm | Adds 1/15 to width/height for clearance fit. | bool | False |
| zz | Z anchor point: bottom, top, middle. | string | "bottom" |

## Category

OOBB Geometry Primitives
