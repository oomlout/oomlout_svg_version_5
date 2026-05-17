# Plan: Eliminate `oomlout_opsc_version_3` Dependency

## Current State
- `opsc.py` from `oomlout_opsc_version_3` is a ~1300-line SolidPython wrapper that provides:
  - `opsc_easy()` — dict-based shape construction (most-used function)
  - `opsc_make_object()` — renders object lists to `.scad` + export formats
  - `saveToAll()` / file export helpers
  - Shape functions: `hole`, `tube`, `rounded_rectangle`, `gear`, `bearing`, `slot`, etc.
  - `opsc_get_object()`, `get_opsc_item()`, `get_opsc_transform()` — CSG dispatch
- 2 `.scad` helper files: `pulley_gt2.scad`, `cycloid.scad`
- **14 files** in this repo do `import opsc`
- Usage is almost entirely: `opsc.opsc_easy()`, `opsc.opsc_make_object()`, `opsc.saveToAll()`

## Steps

### 1. Copy `opsc.py` into this repo
Copy from `reference/oomlout_opsc_version_3/opsc.py` to repo root as `opsc.py`. It lives flat alongside `oobb_base.py` etc.

### 2. Copy `.scad` helper files
Copy `pulley_gt2.scad` and `cycloid.scad` from `reference/oomlout_opsc_version_3/` to repo root. These are `import_scad()` dependencies used by the `gear`/`pulley`/`cycloid` functions inside `opsc.py`.

### 3. Re-export opsc through `oobb.py`
Add `from opsc import *` in `oobb.py` so that all opsc functions become available via `import oobb` / `oobb.func()`.

### 4. Update all 14 files
Replace `import opsc` with `import oobb` (or remove it where `oobb` is already imported), and change `opsc.X()` calls to `oobb.X()`.

## Files to Modify

| File | Change |
|------|--------|
| `opsc.py` (new, from reference) | Copy into repo root |
| `pulley_gt2.scad` (new, from reference) | Copy into repo root |
| `cycloid.scad` (new, from reference) | Copy into repo root |
| `oobb.py` | Add `from opsc import *` |
| `oobb_base.py` | `opsc.X` → `oobb.X` (gets opsc via wildcard import chain) |
| `oobb_get_items_base_old.py` | `import opsc` → `import oobb`, `opsc.X` → `oobb.X` |
| `oobb_get_items_base.py` | `opsc.X` → `oobb.X` (gets opsc via wildcard from base_old) |
| `oobb_working_gear.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_circle.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_all.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_tray.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_mounting_plate.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_wire.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_pulley.py` | `import opsc` → remove (already imports oobb) |
| `oobb_working_plate.py` | `import opsc` → remove (already imports oobb) |
| `action_generate_bundles.py` | `import opsc` → remove (already imports oobb) |
| `action_generate_from_yaml.py` | `import opsc` → remove, `opsc.X` → `oobb.X` |
| `action_generate_from_description.py` | `import opsc` → remove, `opsc.X` → `oobb.X` |
| `oobb_corel_harvest.py` | `import opsc` → remove, `opsc.X` → `oobb.X` |

## Risk Mitigation
- The `opsc.py` local copy is byte-identical to reference — no behavior change.
- Wildcard import chain (`base_old` → `base` → `oobb_base`) already propagates everything, so `oobb.opsc_easy` will resolve through `oobb.py`'s `from opsc import *`.
- `.scad` files that reference `C:/gh/oomlout_opsc_version_3/pulley_gt2.scad` in generated test outputs will need snapshot updates (these are generated paths from SolidPython's `import_scad`, not hand-written source).

## Verification
- Run `python -m unittest discover -s tests -p "test_*.py"` after changes.
- Update snapshots with `UPDATE_SNAPSHOTS=1` if generated `.scad` path references change.
