# github_belfryscad_bosl2_screw

**GitHub BelfrySCAD BOSL2: Screw**

Raw OpenSCAD wrapper around BOSL2 `screw()` from `screws.scad`, using the local `git/BOSL2` clone and the repo raw_scad insertion path.

## Returns

Raw SCAD geometry component dict.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |
| color | Display color passed through to the rendered screw object. | string | "" |
| spec | BOSL2 screw specification string, for example `"M3,12"` or `"#8-32,3/4"`. | string | "M3,12" |
| head | BOSL2 head type. | string | "socket" |
| drive | BOSL2 drive type. | string | "none" |
| length | Overall screw length in mm. | number | 12 |
| l | Alias for `length`. | number | 12 |
| thread | Thread type or specification. BOSL2 default is `"coarse"`. | string | "coarse" |
| drive_size | Optional BOSL2 drive recess size override. | number | "" |
| thread_len | Threaded portion length in mm. | number | "" |
| undersize | BOSL2 screw undersize override. | number | 0 |
| shaft_undersize | BOSL2 shaft undersize override. | number | 0 |
| head_undersize | BOSL2 head undersize override. | number | 0 |
| tolerance | BOSL2 screw tolerance, e.g. `"6g"` or `"2A"`. | string | "" |
| blunt_start | If true and threaded, create blunt-start threads in BOSL2. | bool | True |
| details | If true, request BOSL2 detailed geometry. | bool | False |
| atype | BOSL2 anchor type, one of `"screw"`, `"head"`, `"shaft"`, `"threads"`, `"shank"`. | string | "screw" |
| anchor | BOSL2 anchor, for example `"center"`, `"top"`, `"bottom"`. | string | "center" |
| mode | Render modes: `"laser"`, `"3dpr"`, `"true"`. | list | ["laser","3dpr","true"] |
