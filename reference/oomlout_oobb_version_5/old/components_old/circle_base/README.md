# circle_base

**Circles: Circle Base**

Base circular geometry builder with optional shaft hole, perimeter holes, and doughnut cutout.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| diameter | Circle diameter in OOBB units. | number | 1 |
| thickness | Circle thickness in mm. | number | 3 |
| size | OOBB grid size prefix. | string | "oobb" |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| extra | Extra variant/modifier string. | string | "" |
| shaft | Shaft type; suppresses middle hole when set. | string | "" |
| holes | Add perimeter holes. | bool | True |
| both_holes | Add both oobb and oobe holes. | bool | True |

## Category

Circles
