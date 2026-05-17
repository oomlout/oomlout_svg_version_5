# oobb_screw_exact

**OOBB Part: Exact Screw**

Part builder that accepts the preferred OOBB screw naming format and maps it to the GitHub BelfrySCAD BOSL2 screw wrapper.

## Returns

Thing dict with computed GitHub/BOSL2 screw fields and generated components.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| thread_size | Preferred OOBB thread token, for example `"m2_diameter"` or `"m3_diameter"`. | string | "m3_diameter" |
| length | Preferred OOBB length token, for example `"10_mm_length"`. | string | "10_mm_length" |
| drive_style | Preferred OOBB drive token, for example `"hex_head"`, `"phillips_head"`, `"torx_head"`, `"slot_head"`. | string | "hex_head" |
| screw_style | Preferred OOBB screw head token, for example `"countersunk"`, `"socket_cap"`, `"button"`, `"pan"`. | string | "countersunk" |
| screw_color | Display color for the screw. `"black"` is softened to a dark grey to preserve visible detail. | string | "silver" |
| screw_colour | British spelling alias for `screw_color`. | string | "" |
| modes | Preferred OOBB render modes list, for example `["3dpr"]`. | list | ["3dpr"] |
| mode | Optional direct mode override passed through to the GitHub screw wrapper. | list | ["3dpr"] |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| oobb_name | Logical OOBB name for the part. Defaults to `"screw"`. | string | "screw" |
| oomp_mode | Metadata mode, usually `"project"`. | string | "project" |
| oomp_description_main | Optional OOMP main description. | string | "screw_" |
| oomp_description_extra | Optional OOMP extra description. | string | "" |
