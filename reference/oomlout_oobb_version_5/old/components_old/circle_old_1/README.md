# circle_old_1

**Circles: Circle (Legacy)**

Legacy circular geometry builder with optional holes, both-holes, extra nut, and center-hole patterns.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| diameter | Circle diameter in OOBB units. | number | 1 |
| thickness | Circle thickness in mm. | number | 3 |
| holes | Add standard hole patterns. | bool | True |
| both_holes | Also add oobe (intermediate) holes. | bool | False |
| exclude_d3_holes | Skip diagonal 45° holes on diameter-3 circles. | bool | False |
| exclude_center_holes | Skip center-region holes. | bool | False |
| extra | Extra variant/modifier string. | string | "" |

## Category

Circles
