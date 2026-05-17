# oobb_overhang

**OOBB Geometry Primitives: Overhang Bridge**

Two-layer 3D-print overhang bridge geometry sized to a named radius footprint.

## Returns

List of geometry component dicts.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| radius_name | Named radius key: `"m3"`, `"m3_nut"`, `"m2"`, `"m6"`. | string | "m3" |
| zz | Z anchor: `"bottom"` or `"top"`. | string | "bottom" |
| type | Geometry type: positive or negative. | string | "positive" |
