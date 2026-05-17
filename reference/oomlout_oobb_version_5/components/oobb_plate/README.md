# oobb_plate

**OOBB Geometry Primitives: Plate**

OOBB grid-sized plate (cylinder for 1×1, rounded rectangle otherwise) with optional hole pattern.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| width | Width in OOBB grid units. | number | 1 |
| height | Height in OOBB grid units. | number | 1 |
| depth | Plate thickness in mm. | number | 3 |
| zz | Z anchor: bottom, top, middle. | string | "bottom" |
| extra_mm | Adds 1/15 to size for clearance fit. | bool | False |
| holes | Include OOBB hole pattern. | bool | False |

## Category

OOBB Geometry Primitives
