# plate_base

**Plates: Base Plate**

Base rectangular plate with standard OOBB holes and optional extras (gorm, slip_center, slip_end, slip_corner).

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| width | Plate width in OOBB units. | number | 1 |
| height | Plate height in OOBB units. | number | 1 |
| thickness | Plate depth in mm. | number | 3 |
| size | OOBB size variant. | string | "oobb" |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| extra | Extra variant/modifier string. | string | "" |
| holes | Include hole geometry. | bool | True |
| both_holes | Add holes on both faces. | bool | True |

## Category

Plates
