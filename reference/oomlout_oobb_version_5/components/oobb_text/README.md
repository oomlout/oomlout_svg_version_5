# oobb_text

**OOBB Geometry Primitives: Text**

Legacy OOBB text helper that creates centered extruded text with OOBB defaults.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| text | Text string to render. | string | "" |
| concate | Legacy abbreviation flag: keep the first character and each character after an underscore. | bool | False |
| height | Extrusion height in mm. depth and h are accepted as aliases. | number | 0.3 |
| depth | Alias for height, with priority over h and height when supplied. | number |  |
| h | Alias for height, used when depth is not supplied. | number |  |
| size | OpenSCAD text size. | number | 7 |
| font | OpenSCAD font name. | string | "Candara:Light" |
| halign | Horizontal alignment: left, center, or right. | string | "center" |
| valign | Vertical alignment: top, center, baseline, or bottom. | string | "center" |
| type | Geometry type/modifier context, usually positive or negative. | string | "positive" |
| m | OpenSCAD modifier prefix, e.g. #, %, *. | string | "" |

## Category

OOBB Geometry Primitives

