# Plan: Migrate opsc Shapes to Component Folders & Roll opsc into oobb.py

## Status key
- `[ ]` Not started
- `[~]` In progress
- `[x]` Complete

---

## Overview

`opsc.py` currently holds all SolidPython shape primitives (`hole`, `tube`, `bearing`, etc.) plus
rendering helpers.  The `oobb.py` dispatch (`oobb_easy()`) already supports discovering shapes from
`components/*/working.py` via `_get_shape_lookup()`.  The goal is to:

1. Give every opsc shape its own `components/<name>/working.py` file (same contract as existing
   oobb components: `describe()`, `define()`, `action(**kwargs)`).
2. Remove the fallback `import opsc; opsc.opsc_easy()` path from `oobb_easy()` — all shapes
   resolved via component discovery.
3. Inline all opsc function bodies into `oobb.py` so the project no longer depends on a separate
   `opsc.py` module; `opsc.py` becomes a thin backward-compatibility re-export shim.
4. Update all component `working.py` files that currently do `import opsc` to use `import oobb`
   instead.

### Architecture recap (unchanged after migration)

```
oobb_easy(**kwargs)
  └─ _get_shape_lookup()               # scans components/*/working.py
       └─ component action(**kwargs)   # returns list of component *dicts*
            └─ opsc_easy() equiv.      # wraps params into a single dict
                 └─ opsc_get_object()  # called at render time → SolidPython
                      └─ get_opsc_item() → shape function → SolidPython object
```

Component `action()` functions return **lists of component dicts** (not SolidPython objects).
Actual SolidPython calls only happen at render time inside `opsc_get_object()`.

---

## Phase 1 – Inventory & Coverage Audit

### 1.1 opsc shapes already covered via existing shape_aliases
- `[ ]` Confirm `hole`         → `oobb_hole`                   (aliases: `['oobb_hole', 'hole']`)
- `[ ]` Confirm `tube`         → `oobb_tube`                   (aliases: `['tube']`)
- `[ ]` Confirm `tube_new`     → `oobb_tube_new`               (aliases: `['tube_new']`)
- `[ ]` Confirm `slot`         → `oobb_slot`                   (aliases: `['slot']`)
- `[ ]` Confirm `sphere`       → `oobb_sphere`                 (aliases: `['sphere']`)

### 1.2 Existing oobb components missing their opsc alias
- `[ ]` `oobb_cube`            — add `'cube'` alias            (current: `['oobb_cube']`)
- `[ ]` `oobb_cylinder`        — add `'cylinder'` alias        (current: `[]`)
- `[ ]` `oobb_rounded_rectangle_rounded` — add `'rounded_rectangle'` alias

### 1.3 opsc shapes with NO component at all (need new folders)
Basic SolidPython primitives:
- `[ ]` `polygon`
- `[ ]` `text`
- `[ ]` `import_stl`

opsc helper / mechanical shapes:
- `[ ]` `slot_small`
- `[ ]` `text_hollow`
- `[ ]` `tray`
- `[ ]` `rounded_octagon`
- `[ ]` `rounded_rectangle_extra`
- `[ ]` `sphere_rectangle`
- `[ ]` `countersunk`
- `[ ]` `polyg`
- `[ ]` `polyg_tube`
- `[ ]` `polyg_tube_half`
- `[ ]` `bearing`
- `[ ]` `oring`
- `[ ]` `vpulley`
- `[ ]` `d_shaft`
- `[ ]` `gear`
- `[ ]` `pulley_gt2`
- `[ ]` `cycloid`
- `[ ]` `raw_scad`

---

## Phase 2 – Fix Missing Aliases on Existing Components

For each entry in §1.2, edit the relevant `working.py` to add the opsc shape name to
`d["shape_aliases"]`.

- `[ ]` `components/oobb_cube/working.py`                   — add `'cube'`
- `[ ]` `components/oobb_cylinder/working.py`               — add `'cylinder'`
- `[ ]` `components/oobb_rounded_rectangle_rounded/working.py` — add `'rounded_rectangle'`

---

## Phase 3 – Create New Component Folders

Each new folder follows the standard contract.  `action(**kwargs)` should:
- Accept all kwargs the opsc function accepts
- Build and return `[opsc_easy_dict]` — a list with one component dict — using the same
  parameters that `opsc.opsc_easy(type, shape, **kwargs)` would emit.
- After Phase 5 the `import opsc` call becomes `import oobb`.

Template pattern for a simple primitive wrapper (e.g. `polygon`):

```python
def action(**kwargs):
    import opsc          # → becomes `import oobb` after Phase 5
    return [opsc.opsc_easy(
        kwargs.get("type", "positive"),
        "polygon",
        **{k: v for k, v in kwargs.items() if k not in ("type", "shape")}
    )]
```

Folders to create:

### Basic primitives
- `[ ]` `components/polygon/working.py`
- `[ ]` `components/text/working.py`
- `[ ]` `components/import_stl/working.py`

### Shape helpers
- `[ ]` `components/slot_small/working.py`
- `[ ]` `components/text_hollow/working.py`
- `[ ]` `components/tray/working.py`
- `[ ]` `components/rounded_octagon/working.py`
- `[ ]` `components/rounded_rectangle_extra/working.py`
- `[ ]` `components/sphere_rectangle/working.py`
- `[ ]` `components/countersunk/working.py`
- `[ ]` `components/polyg/working.py`
- `[ ]` `components/polyg_tube/working.py`
- `[ ]` `components/polyg_tube_half/working.py`
- `[ ]` `components/raw_scad/working.py`

### Mechanical
- `[ ]` `components/bearing/working.py`
- `[ ]` `components/oring/working.py`
- `[ ]` `components/vpulley/working.py`
- `[ ]` `components/d_shaft/working.py`
- `[ ]` `components/gear/working.py`
- `[ ]` `components/pulley_gt2/working.py`
- `[ ]` `components/cycloid/working.py`

---

## Phase 4 – Roll opsc.py into oobb.py

Move all function bodies from `opsc.py` into `oobb.py` so it becomes self-contained.

### 4.1 Move globals & imports
- `[ ]` Add `from solid import *` to `oobb.py` top (currently arrived via `from opsc import *`)
- `[ ]` Move `_RAW_SCAD_CACHE_DIR`, `radius_dict`, `countersunk_dict`, `mode` globals
- `[ ]` Move `set_mode(m)`

### 4.2 Move rendering pipeline
- `[ ]` Move `opsc_make_object()`
- `[ ]` Move `opsc_get_object()`
- `[ ]` Move `get_opsc_item()`
- `[ ]` Move `get_opsc_transform()`
- `[ ]` Move `opsc_easy()` / `opsc_easy_array()`
- `[ ]` Move `getLaser()`

### 4.3 Move shape functions (SolidPython geometry)
- `[ ]` Move `hole()`
- `[ ]` Move `tube()` / `tube_new()`
- `[ ]` Move `slot()` / `slot_small()`
- `[ ]` Move `rounded_rectangle()` / `rounded_rectangle_extra()`
- `[ ]` Move `rounded_octagon()`
- `[ ]` Move `sphere_rectangle()`
- `[ ]` Move `tray()`
- `[ ]` Move `countersunk()`
- `[ ]` Move `d_shaft()`
- `[ ]` Move `polyg()` / `polyg_tube()` / `polyg_tube_half()`
- `[ ]` Move `regular_polygon()`
- `[ ]` Move `text_hollow()`
- `[ ]` Move `bearing()`
- `[ ]` Move `oring()` / `vpulley()`
- `[ ]` Move `gear()`
- `[ ]` Move `pulley_gt2()`
- `[ ]` Move `cycloid()`
- `[ ]` Move `raw_scad()` / `_write_raw_scad_source()` / `import_scad_object()`

### 4.4 Move file export helpers
- `[ ]` Move `saveToAll` / `save_to_all`
- `[ ]` Move `saveToDxf` / `save_to_dxf`
- `[ ]` Move `saveToPng` / `save_to_png`
- `[ ]` Move `saveToStl` / `save_to_stl`
- `[ ]` Move `saveToSvg` / `save_to_svg`
- `[ ]` Move `saveToFile` / `save_to_file` / `saveToFileAll` / `save_to_file_all`

### 4.5 Update oobb.py header
- `[ ]` Replace `from opsc import *` with `from solid import *`
- `[ ]` Remove the `import opsc` lazy reference now that functions live locally

### 4.6 Reduce opsc.py to a shim
- `[ ]` Replace opsc.py body with: `from oobb import *  # backward-compat re-export`
- `[ ]` Keep `pulley_gt2.scad` and `cycloid.scad` (external SCAD files, not Python)

---

## Phase 5 – Update Component working.py Files

All components that still do `import opsc; opsc.opsc_easy(...)` must be updated to use
`import oobb; oobb.opsc_easy(...)` (or call the local function directly).

- `[ ]` `components/oobb_hole/working.py`
- `[ ]` `components/oobb_tube/working.py`
- `[ ]` `components/oobb_tube_new/working.py`
- `[ ]` `components/oobb_slot/working.py`
- `[ ]` `components/oobb_sphere/working.py`
- `[ ]` `components/oobb_cylinder/working.py`
- `[ ]` `components/oobb_cylinder_hollow/working.py`
- `[ ]` `components/oobb_rounded_rectangle_hollow/working.py`
- `[ ]` `components/oobb_rounded_rectangle_rounded/working.py`
- `[ ]` `components/oobb_screw/working.py`
- `[ ]` `components/oobb_screw_countersunk/working.py`
- `[ ]` `components/oobb_screw_self_tapping/working.py`
- `[ ]` `components/oobb_screw_socket_cap/working.py`
- `[ ]` `components/oobb_nut/working.py`
- `[ ]` `components/oobb_plate/working.py`
- `[ ]` `components/oobb_rot/working.py`
- `[ ]` `components/bolt/working.py`
- `[ ]` All new component working.py files created in Phase 3

---

## Phase 6 – Update oobb_easy() Dispatch

`oobb_easy()` currently gates oobb_* shapes into component lookup and falls back to
`opsc.opsc_easy()` for others.  After Phase 3 every shape has a component entry, so the fallback
is no longer needed.

- `[ ]` Remove the `if "oobb" in shape or "oobe" in shape:` branch split
- `[ ]` Make ALL shapes go through `_get_shape_lookup()` uniformly
- `[ ]` Remove the `import opsc; opsc.opsc_easy(...)` fallback block
- `[ ]` Raise a clear `ValueError` if a shape is not found (already exists for oobb path)

---

## Phase 7 – Validation & Tests

- `[ ]` Run `python -m unittest discover -s tests -p "test_*.py"` — expect same pass/fail rate
- `[ ]` Smoke-test `oobb.oe(t="positive", s="hole", r=5, depth=10)` returns a list of dicts
- `[ ]` Smoke-test `oobb.oe(t="positive", s="cube", size=[10,10,10])` returns a list of dicts
- `[ ]` Smoke-test `oobb.oe(t="positive", s="bearing", id=8, od=22, depth=7, pos=[0,0,0])` works
- `[ ]` Smoke-test `oobb.oe(t="positive", s="pulley_gt2", number_of_teeth=20, depth=6)` works
- `[ ]` Confirm `from opsc import *` in legacy scripts still works via the shim
- `[ ]` Update snapshots if needed: `UPDATE_SNAPSHOTS=1 python -m unittest discover -s tests`

---

## Phase 8 – Cleanup

- `[ ]` Remove `from opsc import *` line from `oobb.py` (replaced in Phase 4.5)
- `[ ]` Add a deprecation notice comment to `opsc.py` shim
- `[ ]` Update `components/README.md` to mention opsc primitive components
- `[ ]` Update this plan file — mark all steps complete

---

## Notes

- `pulley_gt2.scad`, `cycloid.scad` remain in the repo root; the Python wrappers call them via
  `import_scad()` — no change needed to the `.scad` files themselves.
- `oobb_variables.initialize_variables()` call at module end of `oobb.py` must stay last.
- `set_mode("laser")` call at bottom of `opsc.py` must be preserved in `oobb.py` (or called
  during `initialize_variables()`).
- The `_SHAPE_LOOKUP` cache is invalidated on first access; no cache-reset needed after adding
  new component folders (process restart re-scans).
- The `old/oobb_base.py` and old release scripts still import opsc directly — the shim in
  Phase 4.6 keeps them working.
