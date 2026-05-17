# Plan: oobb_cube_hexagon_cutout Component

## What it does
A cube with a tiling hexagon cutout pattern and a solid border around all edges.

## Parameters
- `pos` — `[x,y,z]` position (default `[0,0,0]`)
- `size` — `[x,y,z]` outer cube dimensions (required)
- `hexagon_radius` — circumradius of each hex cutout (default `10`)
- `border_width` — solid border kept around the cube edges (default `10`)
- `rotation_cutout` — rotation of the hex grid in degrees (default `0`)
- `type` — `positive` or `negative` (default `"positive"`)
- `zz` — z anchor: `bottom`, `top`, `center` (default `"bottom"`)

## Progress Steps

- [ ] **Step 1** — Create `components/oobb_cube_hexagon_cutout/working.py` skeleton  
  Boilerplate: `describe()`, `define()`, stub `action()` following the same module pattern as other components.

- [x] **Step 2** — Design OpenSCAD geometry as `SCAD_SOURCE` inline string  
  - `module oobb_cube_hexagon_cutout_raw(sx, sy, sz, hex_r, border, rot_cut)`
  - All geometry inlined directly (no nested modules) — OpenSCAD nested modules don't inherit parent scope variables, which caused the cutouts to silently disappear.
  - `difference()` of outer cube minus `intersection()` of clipping cube and hex prism `for` loops.

- [x] **Step 3** — Wire `action()` to emit the `raw_scad` dict  
  Follow gridfinity pattern: extract kwargs, return dict with `shape: "raw_scad"`, `source`, `module`, `module_kwargs`, `pos`, `rot`, `type`.

- [ ] **Step 4** — Smoke-test  
  Python import + `action()` call confirms dict returned and SCAD string looks correct.
