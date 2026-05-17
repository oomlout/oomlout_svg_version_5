# Plan: Migrate All `opsc` Shapes into `components/*/working.py`

## Goal

Make every shape currently accessed through `opsc` available through the same
`components/<shape>/working.py` pattern used by the migrated OOBB geometry.

This includes:

- basic solid shapes
- composite/extended opsc shapes
- keeping the current render pipeline working during the move
- migrating shape ownership, not just adding thin aliases that still depend on
  the old `opsc.py` shape bodies

---

## What The Codebase Looks Like Today

### Current dispatch

- `oobb.py` already discovers `components/*/working.py` via `_get_shape_lookup()`.
- `oobb.oobb_easy()` first tries component lookup, then falls back to
  `opsc.opsc_easy(...)` for shapes that do not yet exist as components.
- `opsc.py` still owns:
  - the low-level render pipeline (`opsc_make_object`, `opsc_get_object`,
    `get_opsc_item`, transforms, file export helpers)
  - the full catalog of non-OOBB shape builders

### Current live coverage gap

I compared the live component lookup against the shape inventory hard-coded in
`opsc.py`.

Already reachable through component lookup:

- `sphere`
- `hole`
- `slot`
- `tube`
- `tube_new`

Missing from component lookup today:

- `cube`
- `cylinder`
- `import_stl`
- `polygon`
- `text`
- `slot_small`
- `text_hollow`
- `tray`
- `rounded_rectangle`
- `rounded_octagon`
- `rounded_rectangle_extra`
- `sphere_rectangle`
- `countersunk`
- `polyg`
- `polyg_tube`
- `polyg_tube_half`
- `bearing`
- `oring`
- `vpulley`
- `d_shaft`
- `gear`
- `pulley_gt2`
- `cycloid`
- `raw_scad`

### Existing components that still depend on the fallback

Several current component files already emit shapes like `cube`, `cylinder`,
`rounded_rectangle`, `polyg`, `oring`, and `raw_scad`, but those names still
work only because `oobb.oobb_easy()` falls back to `opsc`.

The most important examples are:

- `components/oobb_cube_center/working.py` -> emits `shape="cube"`
- `components/oobb_circle/working.py` -> emits `shape="cylinder"`
- `components/oobb_cylinder/working.py` -> emits `shape="cylinder"`
- `components/oobb_plate/working.py` -> emits `shape="rounded_rectangle"`
- `components/oobb_nut/working.py` -> emits `shape="polyg"`
- `components/oobb_rounded_rectangle_rounded/working.py` -> emits
  `shape="rounded_rectangle"` and `shape="oring"`
- `components/oobb_cube_hexagon_cutout/working.py` -> emits `shape="raw_scad"`

That means removing the fallback too early will break existing migrated
components.

---

## Recommendation

Do **not** make this a full "`opsc.py` into `oobb.py`" migration.

That is larger than the request and creates unnecessary risk because `opsc.py`
still contains the renderer, transform logic, OpenSCAD export helpers, and the
actual SolidPython/OpenSCAD execution layer.

### Safer architecture

Use a two-layer migration:

1. `components/<shape>/working.py` becomes the canonical access point for every
   shape.
2. `opsc.py` stays as the render backend during the migration.
3. Shape-specific code moves out of `opsc.py` into the corresponding
   component folder.
4. `get_opsc_item()` is updated to resolve migrated shapes through the
   component module at render time.

### Important implementation detail

To migrate the code and not just alias it, each geometry component should own
two things:

- `action(**kwargs)` for component access and composition
- `render(params)` for SolidPython/OpenSCAD generation at render time

That gives one canonical home per shape while preserving the current separation
between:

- component dict creation time
- SolidPython object creation time

### Why this is the lowest-risk path

- It satisfies the requirement that all shapes are accessed via
  `components/*/working.py`.
- It lets us migrate shape logic out of `opsc.py` instead of merely pointing to
  it.
- It avoids rewriting the whole renderer in the same change.
- It allows the old `opsc` functions to remain as temporary fallbacks until
  parity is proven.

---

## Shape Inventory To Migrate

### Wave 1: basic solid shapes

These must exist as components even if the render backend still handles them as
base primitives:

- `components/cube/working.py`
- `components/cylinder/working.py`
- `components/sphere/working.py`
- `components/polygon/working.py`
- `components/text/working.py`
- `components/import_stl/working.py`

### Wave 2: foundational composite shapes

These are the first non-basic shapes to migrate because other components depend
on them:

- `components/hole/working.py`
- `components/slot/working.py`
- `components/slot_small/working.py`
- `components/tube/working.py`
- `components/tube_new/working.py`
- `components/rounded_rectangle/working.py`
- `components/polyg/working.py`
- `components/oring/working.py`
- `components/raw_scad/working.py`

### Wave 3: shapes built on the foundations

- `components/countersunk/working.py`
- `components/rounded_octagon/working.py`
- `components/rounded_rectangle_extra/working.py`
- `components/sphere_rectangle/working.py`
- `components/tray/working.py`
- `components/polyg_tube/working.py`
- `components/polyg_tube_half/working.py`
- `components/bearing/working.py`
- `components/d_shaft/working.py`
- `components/text_hollow/working.py`
- `components/vpulley/working.py`

### Wave 4: external-SCAD / special-case shapes

- `components/gear/working.py`
- `components/pulley_gt2/working.py`
- `components/cycloid/working.py`

These need extra path handling and parity checks.

---

## Exact Moves Required

## 1. Add a render hook to geometry components

Update the geometry-component contract so migrated shape folders can own render
logic as well as access logic.

Move:

- add `render(params)` support to shape components
- keep `action(**kwargs)` returning component dict lists
- keep `define()` / `describe()` unchanged for discovery and docs

Implementation instruction:

- `oobb` discovery remains based on `working.py`
- `render(params)` is optional
- only shape components need `render(params)`; part-builder components do not

## 2. Teach the backend how to find migrated shape renderers

Files to update:

- `oobb.py`
- `opsc.py`

Move:

- add a `_get_shape_render_lookup()` alongside `_get_shape_lookup()`
- load `render` from `components/*/working.py` when present
- update `get_opsc_item()` so the dispatch order becomes:
  1. built-in primitives (`cube`, `cylinder`, `sphere`, `polygon`, `text`,
     `import_stl`)
  2. migrated component renderers
  3. legacy `opsc.py` shape functions as temporary fallback

Implementation instruction:

- do not remove the legacy `other_shapes` branch in the first pass
- log or comment which shapes still hit legacy fallback
- only remove fallback once every opsc shape has a component renderer and tests
  pass

## 3. Create canonical shape folders for every opsc shape

Files/folders to add:

- `components/cube/working.py`
- `components/cylinder/working.py`
- `components/sphere/working.py`
- `components/polygon/working.py`
- `components/text/working.py`
- `components/import_stl/working.py`
- `components/hole/working.py`
- `components/slot/working.py`
- `components/slot_small/working.py`
- `components/tube/working.py`
- `components/tube_new/working.py`
- `components/rounded_rectangle/working.py`
- `components/rounded_octagon/working.py`
- `components/rounded_rectangle_extra/working.py`
- `components/sphere_rectangle/working.py`
- `components/tray/working.py`
- `components/countersunk/working.py`
- `components/polyg/working.py`
- `components/polyg_tube/working.py`
- `components/polyg_tube_half/working.py`
- `components/bearing/working.py`
- `components/oring/working.py`
- `components/vpulley/working.py`
- `components/d_shaft/working.py`
- `components/gear/working.py`
- `components/pulley_gt2/working.py`
- `components/cycloid/working.py`
- `components/text_hollow/working.py`
- `components/raw_scad/working.py`

Implementation instruction:

- each new folder must own the migrated logic from `opsc.py`
- do not make `action()` call back into the old `opsc.<shape>()`
- if several shapes share math/helpers, move the shared code into a local
  underscore-prefixed helper module under `components/`
- keep folder names equal to the raw shape names

## 4. Migrate the actual shape code out of `opsc.py`

The following functions should be moved into the matching component folder as
the `render(params)` implementation, with helper functions colocated where
needed:

- `hole`
- `tube`
- `tube_new`
- `slot`
- `slot_small`
- `rounded_rectangle`
- `rounded_octagon`
- `rounded_rectangle_extra`
- `sphere_rectangle`
- `tray`
- `countersunk`
- `polyg`
- `polyg_tube`
- `polyg_tube_half`
- `regular_polygon`
- `bearing`
- `oring`
- `vpulley`
- `d_shaft`
- `gear`
- `pulley_gt2`
- `cycloid`
- `text_hollow`
- `raw_scad`
- `_write_raw_scad_source`
- `import_scad_object`

Implementation instruction:

- migrate helper code with the shape it belongs to; do not leave logic behind in
  `opsc.py` unless it is part of the generic renderer
- `regular_polygon()` should move with `polyg`
- `_write_raw_scad_source()` and `import_scad_object()` should move with
  `raw_scad`

## 5. Keep `opsc.py` limited to backend responsibilities

After the migration, `opsc.py` should still own only the generic backend:

- `set_mode`
- `opsc_make_object`
- `opsc_get_object`
- `get_opsc_item`
- `get_opsc_transform`
- `opsc_easy`
- `opsc_easy_array`
- file export helpers
- cache cleanup helpers

Implementation instruction:

- do not delete these while the repo still imports `opsc`
- this keeps legacy callers stable while shape ownership moves

## 6. Update existing components to use canonical shape components

Files to update immediately because they rely on missing shape names:

- `components/oobb_cube_center/working.py`
- `components/oobb_circle/working.py`
- `components/oobb_cylinder/working.py`
- `components/oobb_cylinder_hollow/working.py`
- `components/oobb_hole/working.py`
- `components/oobb_hole_new/working.py`
- `components/oobb_nut/working.py`
- `components/oobb_plate/working.py`
- `components/oobb_rounded_rectangle_hollow/working.py`
- `components/oobb_rounded_rectangle_rounded/working.py`
- `components/oobb_slice/working.py`
- `components/oobb_slot/working.py`
- `components/oobb_sphere/working.py`
- `components/oobb_tube/working.py`
- `components/oobb_tube_new/working.py`
- `components/oobb_cube_hexagon_cutout/working.py`

Files to update because they still import `opsc` directly:

- `components/_example_shell/working.py`
- `components/oobb_circle/working.py`
- `components/oobb_cylinder/working.py`
- `components/oobb_cylinder_hollow/working.py`
- `components/oobb_hole/working.py`
- `components/oobb_hole_new/working.py`
- `components/oobb_nut/working.py`
- `components/oobb_plate/working.py`
- `components/oobb_rounded_rectangle_hollow/working.py`
- `components/oobb_rounded_rectangle_rounded/working.py`
- `components/oobb_slice/working.py`
- `components/oobb_slot/working.py`
- `components/oobb_sphere/working.py`
- `components/oobb_tube/working.py`
- `components/oobb_tube_new/working.py`
- `components/oobb_screw/working.py`
- `components/oobb_holes/working.py`
- `components/oobb_coupler_flanged/working.py`
- `components/oobb_cube_new/working.py`

Implementation instruction:

- change component composition calls to `oobb.oobb_easy(...)`
- keep `opsc` imports only in modules that truly need backend-only functions
- prefer composing through shape components rather than reaching into backend
  functions directly

## 7. Decide how to handle the existing `oobb_*` geometry wrappers

The raw shape-name folders should become canonical for opsc-origin shapes.

Recommended handling:

- keep existing `oobb_*` folders for compatibility
- let them reuse the new canonical shape folders where appropriate
- do not duplicate the same geometry math in both `oobb_*` and raw-shape folders

Examples:

- `oobb_sphere` can reuse `sphere`
- `oobb_cube_center` can reuse `cube`
- `oobb_plate` can reuse `rounded_rectangle`
- `oobb_nut` can reuse `polyg`

Implementation instruction:

- reuse helpers, not backend fallbacks
- if a legacy `oobb_*` folder becomes a thin compatibility wrapper, that is
  acceptable because the migrated code now lives in the canonical raw-shape
  component

---

## Dependency Order

This order minimizes breakage.

### Phase A: groundwork

1. add `render(params)` support to discovered shape components
2. add render-lookup support to backend dispatch
3. add tests that detect whether a shape is still using legacy fallback

### Phase B: base shape components

1. `cube`
2. `cylinder`
3. `sphere`
4. `polygon`
5. `text`
6. `import_stl`
7. `raw_scad`

Reason:

- existing components already depend on these names

### Phase C: foundation composites

1. `hole`
2. `slot`
3. `slot_small`
4. `tube`
5. `tube_new`
6. `rounded_rectangle`
7. `polyg`
8. `oring`

Reason:

- these unblock `oobb_plate`, `oobb_nut`, `oobb_rounded_rectangle_rounded`, and
  several other current folders

### Phase D: second-order composites

1. `countersunk`
2. `rounded_octagon`
3. `rounded_rectangle_extra`
4. `sphere_rectangle`
5. `tray`
6. `polyg_tube`
7. `polyg_tube_half`
8. `bearing`
9. `d_shaft`
10. `text_hollow`
11. `vpulley`

### Phase E: external-SCAD shapes

1. `gear`
2. `pulley_gt2`
3. `cycloid`

Reason:

- these have asset-path and include-path risk

### Phase F: cleanup

1. update remaining direct `import opsc` callers
2. remove legacy `other_shapes` functions from `opsc.py`
3. remove `oobb.oobb_easy()` fallback to `opsc.opsc_easy(...)`

Only do Phase F after parity tests are green.

---

## Don’t Break Anything Rules

### Keep these compatibility points until the end

- keep `opsc.opsc_easy(...)`
- keep `get_opsc_item()` legacy function fallback
- keep existing `oobb_*` geometry components
- keep existing shape names and aliases working

### Add tests before deleting fallback

Add or extend tests for:

- shape lookup completeness against the opsc inventory
- `oobb.oobb_easy(shape="<name>")` returning a list for every migrated shape
- render parity for one representative case per shape
- docs/discovery still seeing all new components
- SCAD output parity for motion/fastener/core cases already covered in
  `tests/test_file_generation.py`

### Recommended commands for validation

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Additional targeted smoke checks:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import oobb; print(sorted(k for k in oobb._get_shape_lookup().keys() if k in ['cube','cylinder','sphere','rounded_rectangle','polyg','oring','raw_scad']))"
```

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import oobb; print(type(oobb.oobb_easy(shape='cube', type='positive', size=[10,10,10], pos=[0,0,0])))"
```

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import oobb; print(type(oobb.oobb_easy(shape='rounded_rectangle', type='positive', size=[20,10,3], r=3, pos=[0,0,0])))"
```

### Snapshot rule

- do not update snapshots until the migration branch is functionally stable
- if snapshots change, review whether it is a real geometry change or only an
  include-path / ordering change

---

## Known Risks And Blockers

### 1. `cycloid.scad` is not in the expected runtime location

`opsc.py` imports `cycloid.scad`, but this repo currently only contains that
file under:

- `reference/oomlout_opsc_version_3/cycloid.scad`

There is no root-level `cycloid.scad` alongside `pulley_gt2.scad`.

Action required:

- decide whether to copy it into repo root, move it into a dedicated assets
  folder, or switch the migrated component to `raw_scad` with an explicit path

### 2. `pulley_gt2` currently leaks absolute include paths

Generated SCAD output still references an absolute external path to an older
repo location for `pulley_gt2.scad`.

Action required:

- normalize include paths during the migration
- keep generated SCAD portable inside this repo

### 3. Existing components mutate kwargs in place

A number of current geometry components still mutate `kwargs` directly. That is
already fragile and becomes riskier during a broader shape migration.

Action required:

- standardize on `copy.deepcopy(kwargs)` before mutation in all touched files

### 4. Some current shape names are both canonical and wrapped

Examples:

- `sphere` vs `oobb_sphere`
- `cube` vs `oobb_cube_center` / `oobb_cube`
- `rounded_rectangle` vs `oobb_rounded_rectangle_*`

Action required:

- choose one canonical implementation owner
- keep wrappers for compatibility only

---

## Suggested Deliverables For The Migration PR

The first reviewable PR should include only the groundwork and Wave 1 plus Wave
2 shapes:

- render-hook support
- render lookup in backend
- new components for:
  - `cube`
  - `cylinder`
  - `sphere`
  - `polygon`
  - `text`
  - `import_stl`
  - `raw_scad`
  - `hole`
  - `slot`
  - `slot_small`
  - `tube`
  - `tube_new`
  - `rounded_rectangle`
  - `polyg`
  - `oring`
- updates to existing folders that currently depend on those shapes
- new coverage tests proving the fallback is no longer needed for those names

That is the smallest slice that materially improves the architecture without
trying to solve the entire opsc surface area in one go.

---

## Bottom Line

The migration is very doable, but the safe version is:

- move shape ownership into `components/<shape>/working.py`
- add a render hook so those folders own the actual geometry code
- keep `opsc.py` as the backend until parity is proven
- migrate foundational shapes first because existing components already depend on
  them
- treat `cycloid.scad` and `pulley_gt2.scad` pathing as explicit blockers, not
  cleanup details

If we follow that order, we can get uniform shape access without breaking the
current component migration work.
