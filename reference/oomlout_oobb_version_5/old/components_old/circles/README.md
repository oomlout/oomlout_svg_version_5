# circles

**Part Sets: Circles**

Dispatches to a get_plate_<extra> function or falls back to get_circle_base based on the extra field.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| extra | Extra variant/modifier string. | string | "" |
| thickness | Plate depth used to compute z-position offsets. | number | 3 |
| zz | Vertical anchor: bottom, middle, top. | string | "bottom" |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |

## Category

Part Sets
