# Plan: Extract Remaining `opsc` Shape Code into Individual `working.py` Files

## Progress

- [x] Phase 1 batch 1 inlined into local `working.py` files:
  - `hole`
  - `tube`
  - `tube_new`
  - `slot_small`
  - `slot`
  - `rounded_rectangle`
  - `polyg`
  - `oring`
- [x] Phase 2 second-order geometry extraction:
  - `rounded_octagon`
  - `rounded_rectangle_extra`
  - `sphere_rectangle`
  - `tray`
  - `countersunk`
  - `polyg_tube`
  - `polyg_tube_half`
  - `bearing`
  - `d_shaft`
  - `text_hollow`
  - `vpulley`
- [x] Phase 3 external-SCAD and file-backed extraction:
  - `raw_scad`
  - `pulley_gt2`
  - `cycloid`
  - `gear`
- [x] Remove duplicate shape bodies from `components/_shape_renderers.py`
- [x] Remove duplicate shape bodies from `opsc.py`
- [x] Delete `components/_shape_renderers.py` or reduce it to tiny generic utilities only

## Verification Log

- [x] `rg -n "_shape_renderers|render_[a-z_]+ as render" components -g "working.py"` returned no matches
- [x] `rg -n "^def (hole|tube|tube_new|gear|countersunk|d_shaft|slot_small|slot|pulley_gt2|rounded_rectangle|rounded_octagon|tray|rounded_rectangle_extra|sphere_rectangle|cycloid|bearing|oring|vpulley|polyg_tube|polyg_tube_half|polyg|regular_polygon|text_hollow|raw_scad|import_scad_object|_write_raw_scad_source)\(" opsc.py` returned no matches
- [x] Representative `opsc.get_opsc_item(...)` smoke tests passed for:
  - `rounded_rectangle`
  - `polyg`
  - `tray`
  - `bearing`
  - `raw_scad`
  - `pulley_gt2`
  - `cycloid`
- [x] Shape lookup completeness check passed: all opsc inventory shape names resolve through `oobb._get_shape_lookup()`
- [ ] Full repo unittest suite green
  - status: not verified cleanly because the repo still has broader pre-existing test/environment failures outside this extraction change

## Goal

Finish the migration so each shape component owns its own implementation inside:

- `components/<shape>/working.py`

Specifically:

- move render logic out of `opsc.py`
- move render logic out of `components/_shape_renderers.py`
- leave `opsc.py` with backend/render-pipeline responsibilities only
- avoid replacing migrated code with mere links back to shared legacy helpers

---

## Current State

The codebase is in an intermediate state:

- shape access already goes through `components/<shape>/working.py`
- `opsc.get_opsc_item()` can already call `render()` from component modules
- many new raw-shape components exist

But the actual geometry code is still split across two shared/legacy locations:

### Still in `opsc.py`

- `hole`
- `tube`
- `tube_new`
- `gear`
- `countersunk`
- `d_shaft`
- `slot_small`
- `slot`
- `pulley_gt2`
- `rounded_rectangle`
- `rounded_octagon`
- `tray`
- `rounded_rectangle_extra`
- `sphere_rectangle`
- `cycloid`
- `bearing`
- `oring`
- `vpulley`
- `polyg_tube`
- `polyg_tube_half`
- `polyg`
- `regular_polygon`
- `text_hollow`
- `_write_raw_scad_source`
- `raw_scad`
- `import_scad_object`

### Still centralized in `components/_shape_renderers.py`

Even where the code was “migrated,” it was migrated into one shared helper file,
not into the individual `working.py` files:

- `render_hole`
- `render_tube`
- `render_tube_new`
- `render_slot_small`
- `render_slot`
- `render_rounded_rectangle`
- `render_rounded_octagon`
- `render_tray`
- `render_rounded_rectangle_extra`
- `render_sphere_rectangle`
- `render_cycloid`
- `render_bearing`
- `render_oring`
- `render_vpulley`
- `render_polyg_tube`
- `render_polyg_tube_half`
- `regular_polygon_points`
- `render_polyg`
- `render_text_hollow`
- `render_d_shaft`
- `render_gear`
- `render_countersunk`
- `_write_raw_scad_source`
- `render_raw_scad`
- `render_import_scad_object`
- `render_pulley_gt2`

That means the real ownership target has not yet been reached.

---

## Target End State

Each shape component should own its own render implementation directly in its
own `working.py`.

### Desired per-shape contract

Each geometry component should contain:

- `describe()`
- `define()`
- `action(**kwargs)`
- `render(params)` where needed

Optional local private helpers can live in the same file:

- `_regular_polygon_points(...)`
- `_resolve_scad_asset(...)`
- `_write_raw_scad_source(...)`

### What should remain in `opsc.py`

`opsc.py` should end the migration owning only backend concerns:

- `_cleanup_raw_scad_artifacts`
- `set_mode`
- component render lookup helpers
- `opsc_make_object`
- `opsc_get_object`
- `get_opsc_item`
- `get_opsc_transform`
- `opsc_easy`
- `opsc_easy_array`
- file export helpers
- `getLaser`

Everything shape-specific should leave `opsc.py`.

### What should happen to `components/_shape_renderers.py`

Preferred end state:

- delete it entirely

Acceptable temporary end state:

- reduce it to one or two truly generic utilities only

But it should not continue to own shape-specific render bodies.

---

## Principles For The Move

### 1. Move code, don’t proxy code

Bad:

- `components/polyg/working.py` importing `render_polyg` from
  `components/_shape_renderers.py`

Good:

- `components/polyg/working.py` defining `render(params)` locally

### 2. Keep helpers with the shape they belong to

Examples:

- polygon point generation should live with `polyg`
- raw SCAD file writing should live with `raw_scad`
- SCAD asset resolution should live with the shapes that need it

### 3. Duplicate lightly if it improves ownership

If a helper is only shared by two closely related shapes, duplication is often
better than preserving a big shared migration blob.

### 4. Keep `opsc.py` backend-only

The backend may dispatch to component renderers, but it should not remain the
authoritative home of any shape logic.

---

## Shape-to-File Extraction Map

## Basic / primitive component files

- `components/cube/working.py`
  - keep primitive wrapper only
  - no custom render body required unless special cube behavior is needed

- `components/cylinder/working.py`
  - keep primitive wrapper only

- `components/sphere/working.py`
  - keep primitive wrapper only

- `components/polygon/working.py`
  - keep primitive wrapper only

- `components/text/working.py`
  - keep primitive wrapper only

- `components/import_stl/working.py`
  - keep primitive wrapper only

These can remain thin because their actual rendering is the base primitive path
inside `get_opsc_item()`.

## Shape files that must gain local `render(params)`

- `components/hole/working.py`
  - move `render_hole`

- `components/tube/working.py`
  - move `render_tube`

- `components/tube_new/working.py`
  - move `render_tube_new`

- `components/slot_small/working.py`
  - move `render_slot_small`

- `components/slot/working.py`
  - move `render_slot`

- `components/rounded_rectangle/working.py`
  - move `render_rounded_rectangle`

- `components/rounded_octagon/working.py`
  - move `render_rounded_octagon`

- `components/tray/working.py`
  - move `render_tray`

- `components/rounded_rectangle_extra/working.py`
  - move `render_rounded_rectangle_extra`

- `components/sphere_rectangle/working.py`
  - move `render_sphere_rectangle`

- `components/countersunk/working.py`
  - move `render_countersunk`

- `components/polyg/working.py`
  - move `render_polyg`
  - move `regular_polygon_points` as a local helper

- `components/polyg_tube/working.py`
  - move `render_polyg_tube`

- `components/polyg_tube_half/working.py`
  - move `render_polyg_tube_half`

- `components/bearing/working.py`
  - move `render_bearing`

- `components/oring/working.py`
  - move `render_oring`

- `components/vpulley/working.py`
  - move `render_vpulley`

- `components/d_shaft/working.py`
  - move `render_d_shaft`

- `components/gear/working.py`
  - move `render_gear`

- `components/pulley_gt2/working.py`
  - move `render_pulley_gt2`
  - move `_resolve_scad_asset` or equivalent local asset-path helper

- `components/cycloid/working.py`
  - move `render_cycloid`
  - move `_resolve_scad_asset` or equivalent local asset-path helper

- `components/text_hollow/working.py`
  - move `render_text_hollow`

- `components/raw_scad/working.py`
  - move `render_raw_scad`
  - move `_write_raw_scad_source`
  - move `render_import_scad_object` if still needed

---

## Extraction Order

This order minimizes breakage and avoids circular migration problems.

### Phase 1: Remove shared ownership for foundational shapes

1. `hole`
2. `tube`
3. `tube_new`
4. `slot_small`
5. `slot`
6. `rounded_rectangle`
7. `polyg`
8. `oring`

Reason:

- many other component and render implementations depend on these

### Phase 2: Move second-order geometry

1. `rounded_octagon`
2. `rounded_rectangle_extra`
3. `sphere_rectangle`
4. `tray`
5. `countersunk`
6. `polyg_tube`
7. `polyg_tube_half`
8. `bearing`
9. `d_shaft`
10. `text_hollow`
11. `vpulley`

### Phase 3: Move external-SCAD and file-backed shapes

1. `raw_scad`
2. `pulley_gt2`
3. `cycloid`
4. `gear`

Reason:

- these have the highest environment/path sensitivity

### Phase 4: Delete legacy/shared shape bodies

1. remove matching functions from `opsc.py`
2. remove matching functions from `components/_shape_renderers.py`
3. collapse any leftover helper code into local shape files

---

## Detailed Move Instructions

## 1. Inline `render()` into each shape file

For each of the shape files listed above:

- copy the current render body from `components/_shape_renderers.py`
- paste it into the local `working.py`
- rename it to `render(params)` if needed
- move any tiny shape-specific helpers into the same file
- keep imports local to that file where practical

Implementation rule:

- after the move, `working.py` must not import a shape-specific renderer from
  `_shape_renderers.py`

## 2. Replace shared helper dependencies with local or tiny shared utilities

Shared dependencies that should be eliminated or minimized:

- `_opsc()`
- `_resolve_scad_asset`
- `regular_polygon_points`
- `_write_raw_scad_source`

Recommended replacements:

- import `opsc` directly inside the local `render(params)` body
- put `_resolve_scad_asset` in `pulley_gt2/working.py` and `cycloid/working.py`
  unless both import a tiny shared `_scad_asset_utils.py`
- put `_regular_polygon_points` in `polyg/working.py`
- put `_write_raw_scad_source` in `raw_scad/working.py`

## 3. Remove matching shape bodies from `opsc.py`

Once a shape file owns `render(params)` locally and smoke tests pass, remove the
old function from `opsc.py`.

Recommended removal batches:

- batch 1:
  - `hole`
  - `tube`
  - `tube_new`
  - `slot_small`
  - `slot`
  - `rounded_rectangle`
  - `polyg`
  - `oring`

- batch 2:
  - `rounded_octagon`
  - `rounded_rectangle_extra`
  - `sphere_rectangle`
  - `tray`
  - `countersunk`
  - `polyg_tube`
  - `polyg_tube_half`
  - `bearing`
  - `d_shaft`
  - `text_hollow`
  - `vpulley`

- batch 3:
  - `raw_scad`
  - `_write_raw_scad_source`
  - `import_scad_object`
  - `pulley_gt2`
  - `cycloid`
  - `gear`
  - `regular_polygon`

## 4. Shrink then remove `components/_shape_renderers.py`

After all component files own their render code:

- confirm no `working.py` imports from `_shape_renderers.py`
- delete the file

If a tiny shared utility remains genuinely worthwhile, split it into a narrowly
named helper file instead of keeping `_shape_renderers.py` as a dumping ground.

---

## Validation Plan

## Fast checks after each phase

Run:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import oobb; print(sorted(k for k in oobb._get_shape_lookup().keys() if k in ['hole','tube','slot','rounded_rectangle','polyg','oring']))"
```

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import opsc; print(type(opsc.get_opsc_item({'type':'positive','shape':'rounded_rectangle','size':[20,10,3],'r':3,'pos':[0,0,0]})).__name__)"
```

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import opsc; print(type(opsc.get_opsc_item({'type':'positive','shape':'polyg','r':5,'height':3,'sides':6,'pos':[0,0,0]})).__name__)"
```

## Grep checks

Use these to confirm extraction is really complete:

```powershell
rg -n "from components\\._shape_renderers|import _shape_renderers|render_[a-z_]+" components -g "working.py"
```

```powershell
rg -n "^def (hole|tube|tube_new|gear|countersunk|d_shaft|slot_small|slot|pulley_gt2|rounded_rectangle|rounded_octagon|tray|rounded_rectangle_extra|sphere_rectangle|cycloid|bearing|oring|vpulley|polyg_tube|polyg_tube_half|polyg|regular_polygon|text_hollow|raw_scad|import_scad_object)\\(" opsc.py
```

The target end state for the second grep is:

- no matches

## Full test command

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Reality note:

- this repo currently has broader pre-existing test/environment failures, so use
  the shape smoke checks as the immediate gate and treat full-suite results as
  contextual rather than binary

---

## Known Risks

### 1. Asset path logic may drift during extraction

`pulley_gt2` and `cycloid` need stable path resolution.

Guardrail:

- preserve the exact path fallback behavior while moving code local

### 2. Hidden coupling through `_opsc()`

The shared renderers currently depend on calling back into `opsc` for:

- `radius_dict`
- `countersunk_dict`
- `get_opsc_item`
- `get_opsc_transform`

Guardrail:

- keep these backend calls explicit in the local file
- do not try to replace them all in the same pass

### 3. Circular render dependencies

Some renderers call other shape names through `get_opsc_item()`.

Examples:

- `tray` -> `sphere_rectangle`
- `polyg_tube` -> `polyg`
- `rounded_rectangle` -> `hole`

Guardrail:

- migrate in dependency order
- smoke test after each batch

### 4. Shared helper deletion too early

Deleting `_shape_renderers.py` before all imports are removed will create a
half-migrated state.

Guardrail:

- only delete it after a grep confirms zero users

---

## Recommended First PR Slice

The safest first extraction PR should include only:

- inline local `render(params)` into:
  - `components/hole/working.py`
  - `components/tube/working.py`
  - `components/tube_new/working.py`
  - `components/slot_small/working.py`
  - `components/slot/working.py`
  - `components/rounded_rectangle/working.py`
  - `components/polyg/working.py`
  - `components/oring/working.py`
- remove those same functions from `components/_shape_renderers.py`
- remove those same functions from `opsc.py` if no fallback path still needs them

That gives a real ownership win without making the PR too wide.

---

## Bottom Line

The next migration step should not be “more shared helpers.” It should be:

- pull each shape’s render body into its own `working.py`
- reduce `opsc.py` to backend-only code
- delete `components/_shape_renderers.py` once the extraction is complete

That gets the project from “component access with centralized implementation”
to true per-shape ownership.
