# oobb_holes

**OOBB Geometry Helpers: Hole Array**

Places OOBB-grid-aligned screw holes across a rectangular or circular area using named hole patterns.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| holes | Hole pattern(s): all, perimeter, perimeter_miss_middle, u, top, bottom, left, right, corners, single, missing_middle, just_middle, circle. | list | ["all"] |
| width | Width in OOBB grid units. | number | 0 |
| height | Height in OOBB grid units. | number | 0 |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| depth | Hole depth in mm. | number | 100 |
| radius_name | Named radius key, e.g. m6, m3. | string | "m6" |
| middle | Include the centre hole. | bool | True |
| size | Grid spacing scale: oobb or oobe. | string | "oobb" |
| both_holes | Also add matching oobe half-grid holes. | bool | False |
| circle | Filter holes to lie inside a circle boundary. | bool | False |
| diameter | Diameter in OOBB units (overrides width/height). | number | 0 |
| diameter_clearance | Clearance from circle edge (mm) when circle=True. | number | 7.5 |
| diameter_center_clearance | Minimum distance from centre to include hole (mm). | number | 0 |
| loc | Grid location(s) [x,y] for single pattern. | list | [0,0] |

## Category

OOBB Geometry Helpers
