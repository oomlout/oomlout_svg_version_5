# oobb_hole

**OOBB Geometry Primitives: Hole (legacy)**

Cylindrical screw hole for all render modes, resolved from a named or explicit radius.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| depth | Hole depth in mm. | number | 200 |
| radius_name | Named radius key, e.g. m3, m6.  Takes priority over radius. | string | "" |
| radius | Explicit radius in mm, used when radius_name is empty. | number | 0 |
| r | Alias for radius. | number | 0 |
| mode | Render modes to emit: laser, 3dpr, true. | list | ["laser","3dpr","true"] |
| m | OpenSCAD modifier prefix, e.g. #, %, *. | string | "" |

## Category

OOBB Geometry Primitives
