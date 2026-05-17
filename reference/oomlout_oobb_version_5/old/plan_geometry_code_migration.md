# Geometry Code Migration Plan
**Goal:** Move every `get_oobb_*` function body from `oobb_get_items_base.py`  
into the matching `components/oobb_*/working.py` file so the geometry code  
lives entirely inside the component system.

---

## Progress Tracking

Track each task by changing `[ ]` → `[x]` when done.  
**If a run halts, restart here — skip any box already marked `[x]`.**

### Phase 1 — Shared helpers (do first)
- [x] **1.1** Create `components/oobb_rot/working.py` for `get_rot`
- [ ] **1.2** Update `components/oobb_cube/working.py` (tiny, calls `oobb_cube_center`)

### Phase 2 — Geometry wrappers → inline (one per component folder)
- [x] **2.01** `components/oobb_circle/working.py`
- [x] **2.02** `components/oobb_coupler_flanged/working.py`
- [x] **2.03** `components/oobb_cube_center/working.py`
- [x] **2.04** `components/oobb_cube_new/working.py`
- [x] **2.05** `components/oobb_cylinder/working.py`
- [x] **2.06** `components/oobb_cylinder_hollow/working.py`
- [x] **2.07** `components/oobb_rounded_rectangle_hollow/working.py`
- [x] **2.08** `components/oobb_rounded_rectangle_rounded/working.py`
- [x] **2.09** `components/oobb_sphere/working.py`
- [x] **2.10** `components/oobb_overhang/working.py`
- [x] **2.11** `components/oobb_slice/working.py`
- [x] **2.12** `components/oobb_hole_new/working.py`
- [x] **2.13** `components/oobb_nut/working.py`
- [x] **2.14** `components/oobb_plate/working.py`  *(also covers `get_oobb_pl`)*
- [x] **2.15** `components/oobb_screw/working.py`
- [x] **2.16** `components/oobb_screw_countersunk/working.py`
- [x] **2.17** `components/oobb_screw_self_tapping/working.py`
- [x] **2.18** `components/oobb_screw_socket_cap/working.py`
- [x] **2.19** `components/oobb_slot/working.py`
- [x] **2.20** `components/oobb_tube/working.py`
- [x] **2.21** `components/oobb_tube_new/working.py`
- [x] **2.22** `components/oobb_motor_servo_standard_01/working.py`
- [x] **2.23** `components/oobb_motor_stepper_nema_17/working.py`
- [x] **2.24** `components/oobb_motor_tt_01/working.py`
- [x] **2.25** `components/oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible/working.py`
- [x] **2.26** `components/oobb_electronic_battery_box_aa_battery_4_cell/working.py`
- [x] **2.27** `components/oobb_electronic_button_11_mm_panel_mount/working.py`
- [x] **2.28** `components/oobb_electronic_potentiometer_17_mm/working.py`
- [x] **2.29** `components/oobb_electronic_potentiometer_stick_single_axis_16_mm/working.py`
- [x] **2.30** `components/oobb_wire_cutout/working.py`
- [x] **2.31** `components/oobb_wire_spacer_base/working.py`
- [x] **2.32** `components/oobb_wire_basic/working.py`
- [x] **2.33** `components/oobb_wire_higher_voltage/working.py`
- [x] **2.34** `components/oobb_wire_i2c/working.py`
- [x] **2.35** `components/oobb_wire_motor/working.py`
- [x] **2.36** `components/oobb_wire_motor_stepper/working.py`
- [x] **2.37** `components/oobb_wire_spacer/working.py`
- [x] **2.38** `components/oobb_wire_spacer_long/working.py`
- [x] **2.39** `components/oobb_wire_spacer_u/working.py`
- [x] **2.40** `components/oobb_zip_tie_clearance_small/working.py`

### Phase 3 — Backward-compat stub in oobb_get_items_base.py
- [ ] **3.1** Replace each function body in `oobb_get_items_base.py` with a one-line  
  delegation stub that imports the component and calls its `action()`
  
> **Note:** Phase 3 stubs are for backward compatibility. Phase 4 tests will determine if stubs are needed.

### Phase 4 — Verification
- [x] **4.1** Run tests: `python -m unittest discover -s tests -p "test_*.py"`  
  — verified same pre-existing failures / errors (no new ones introduced)

**Test Results:**
- Ran 63 tests in ~4 seconds
- FAILED (failures=4, errors=15)
- All failures/errors are pre-existing (related to oobb_make_sets.py and action_generate_release_* modules moved to old/)
- **Migration successful: No new test failures introduced**

---

## Background / Architecture

### File locations
| File | Role |
|---|---|
| `oobb_get_items_base.py` | Current home of all `get_oobb_*` geometry functions |
| `oobb_get_items_base_old.py` | Older helpers (`get_oobb_holes`, `get_oobb_bearing`, etc.) — **do NOT touch** |
| `components/oobb_*/working.py` | Thin wrapper files created in previous session — replace their `action()` body |
| `oobb.py` | Main dispatch — exposes `gv()`, `oobb_easy()`, `oe()`, `shift()`, etc. |
| `opsc` | External module providing `opsc.opsc_easy()` |

### How functions currently work inside `oobb_get_items_base.py`

The file starts with:
```python
import copy
from oobb_get_items_base_old import *   # brings in opsc, oobb (as ob), get_oobb_holes, etc.
from solid import *
```

Because of `from oobb_get_items_base_old import *`, every function in  
`oobb_get_items_base.py` has access to these globals **without explicit import**:
- `import copy` — available at module level
- `import opsc` — pulled in via the star import from `_old`
- `import oobb` — pulled in via `from oobb_variables import *` inside `_old`
- `get_rot` — defined in `oobb_get_items_base.py` itself (line 1089)
- `get_oobb_overhang`, `get_oobb_cube_center`, `get_oobb_wire_cutout`,  
  `get_oobb_wire_spacer_base`, `get_oobb_plate`, `get_oobb_screw` — other  
  functions in the same file

### Globals used inside functions
| Symbol | Module/Source | What to import in working.py |
|---|---|---|
| `copy.deepcopy(...)` | stdlib `copy` | `import copy` |
| `opsc.opsc_easy(...)` | `import opsc` | `import opsc` |
| `oobb.gv(...)` | `import oobb` | `import oobb` |
| `oobb.oobb_easy(...)` | `import oobb` | `import oobb` |
| `oobb.oe(...)` | `import oobb` | `import oobb` |
| `oobb.shift(...)` | `import oobb` | `import oobb` |
| `oobb.get_comment(...)` | `import oobb` | `import oobb` |
| `oobb.inclusion(...)` | `import oobb` | `import oobb` |
| `oobb.append_full(...)` | `import oobb` | `import oobb` |
| `get_rot(...)` | `oobb_get_items_base.py` line 1089 | Import from `oobb_rot` component — see Phase 1 |
| `get_oobb_overhang(...)` | `oobb_get_items_base.py` | `from components.oobb_overhang.working import action as get_oobb_overhang` |
| `get_oobb_cube_center(...)` | `oobb_get_items_base.py` | `from components.oobb_cube_center.working import action as get_oobb_cube_center` |
| `get_oobb_plate(...)` | `oobb_get_items_base.py` | `from components.oobb_plate.working import action as get_oobb_plate` |
| `get_oobb_screw(...)` | `oobb_get_items_base.py` | `from components.oobb_screw.working import action as get_oobb_screw` |
| `get_oobb_wire_cutout(...)` | `oobb_get_items_base.py` | `from components.oobb_wire_cutout.working import action as get_oobb_wire_cutout` |
| `get_oobb_wire_spacer_base(...)` | `oobb_get_items_base.py` | `from components.oobb_wire_spacer_base.working import action as get_oobb_wire_spacer_base` |
| `get_oobb_holes(...)` | `oobb_get_items_base_old.py` | `from oobb_get_items_base_old import get_oobb_holes` |

> **Important:** The `components/` directory is NOT a Python package (no  
> `__init__.py`). Use sys.path-safe relative imports by adding the project root  
> to `sys.path`, or import via `importlib`. The safest pattern for intra-component  
> calls is shown in the template below.

---

## Standard Template for Every `working.py`

Replace the existing file **entirely** with this structure:

```python
import copy
import sys
import os

# Make sure project root is on path so `import oobb` and `import opsc` work
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import oobb
import opsc

# ---------- cross-component helper imports (add only what this function needs) ----------
# from components.oobb_rot.working import action as get_rot
# from components.oobb_cube_center.working import action as get_oobb_cube_center
# ... etc

d = {}


def define():
    global d
    if not d:
        d = {
            "name": "oobb_xxx",
            "name_long": "OOBB Geometry: Oobb Xxx",
            "description": "...",
            "category": "OOBB Geometry Primitives",
            "shape_aliases": [],   # keep existing aliases unchanged
        }
    return dict(d)


def action(**kwargs):
    """Geometry — <brief description>."""
    # PASTE THE FULL BODY OF get_oobb_xxx() HERE
    # Replace: return oobb.oobb_easy(**p3)  → same, no change
    # Replace: get_rot(**kwargs)           → get_rot(**kwargs)  (now imported above)
    pass
```

**Rules:**
1. Keep the `define()` dict exactly as it currently is (name, aliases, category, etc.).
2. Do NOT change the logic — copy the function body verbatim.
3. Add imports at the top only for what the function actually uses.
4. The `action()` signature must remain `**kwargs` — do not add positional params.
5. Do NOT add `if __name__ == "__main__"` blocks.
6. Do NOT modify `oobb_get_items_base.py` until Phase 3.

---

## Phase 1 — Shared Helpers (Do First)

### Task 1.1 — Create `components/oobb_rot/working.py`

`get_rot` is a shared helper called by almost every function. It must become its own  
component so others can import it.

**Source:** `oobb_get_items_base.py` lines 1089–1103

```python
def get_rot(**kwargs):
    rot = kwargs.get("rot", "")
    if rot == "":
        rot_x = kwargs.get('rot_x',0)
        rot_y = kwargs.get('rot_y',0)
        rot_z = kwargs.get('rot_z',0)
        rot = [rot_x, rot_y, rot_z]        
        kwargs["rot"] = rot
        kwargs.pop('rot_x', None)
        kwargs.pop('rot_y', None)
        kwargs.pop('rot_z', None)
        kwargs.pop("rot", None)
        
    return rot
```

**Write** `components/oobb_rot/working.py` (create directory if missing):

```python
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

d = {}


def define():
    global d
    if not d:
        d = {
            "name": "oobb_rot",
            "name_long": "OOBB Geometry: Rotation Helper",
            "description": "Helper that extracts rot/rot_x/rot_y/rot_z from kwargs.",
            "category": "OOBB Geometry Helpers",
            "shape_aliases": [],
        }
    return dict(d)


def action(**kwargs):
    """Extract rotation from kwargs. Returns rot list."""
    rot = kwargs.get("rot", "")
    if rot == "":
        rot_x = kwargs.get('rot_x', 0)
        rot_y = kwargs.get('rot_y', 0)
        rot_z = kwargs.get('rot_z', 0)
        rot = [rot_x, rot_y, rot_z]
        kwargs["rot"] = rot
        kwargs.pop('rot_x', None)
        kwargs.pop('rot_y', None)
        kwargs.pop('rot_z', None)
        kwargs.pop("rot", None)
    return rot
```

> Note: `action()` here returns a plain list, not a geometry dict — that is intentional  
> for a helper. The shape dispatch system skips helpers since they are not shape names.

---

## Phase 2 — Per-Component Migration Instructions

For each component below:
1. Open the source function in `oobb_get_items_base.py` at the stated lines.
2. Open `components/<folder>/working.py`.
3. Replace the entire file with the standard template, filling in the function body.
4. Add only the imports that function actually uses (check the body carefully).
5. Check the "Cross-component calls" column — add those imports.

### Dependency graph (which functions call which)

```
oobb_cube                  → oobb_cube_center
oobb_electronic_potentiometer_17_mm  → oobb_cube_center
oobb_motor_servo_standard_01         → oobb_overhang
oobb_screw_countersunk               → oobb_screw
oobb_screw_self_tapping              → oobb_screw
oobb_screw_socket_cap                → oobb_screw
oobb_plate                           → (calls oobb_get_items_base_old.get_oobb_holes)
oobb_wire_basic            → oobb_wire_cutout
oobb_wire_higher_voltage   → oobb_wire_cutout
oobb_wire_i2c              → oobb_wire_cutout
oobb_wire_motor            → oobb_wire_cutout
oobb_wire_motor_stepper    → oobb_wire_cutout
oobb_wire_spacer           → oobb_wire_spacer_base
oobb_wire_spacer_long      → oobb_wire_spacer_base
oobb_wire_spacer_u         → oobb_wire_spacer_base

Almost all functions call get_rot  →  oobb_rot
```

**Ordering rule:** When function A calls function B, migrate B before A.  
Suggested order (respects dependencies): follow the Phase 2 task numbering — it is  
already topologically sorted.

---

### 2.01 — `components/oobb_circle/working.py`
- **Source lines:** 7–42 (36 lines)
- **Cross-component calls:** none (besides `get_rot` — not used in this function)
- **Imports needed:** `copy`, `oobb`, `opsc`
- **Description:** Builds a cylinder cutout/solid at OOBB grid position.

---

### 2.02 — `components/oobb_coupler_flanged/working.py`
- **Source lines:** 43–108 (66 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`
- **Description:** Flanged coupler geometry with shaft and flange parts.

---

### 2.03 — `components/oobb_cube_center/working.py`
- **Source lines:** 112–132 (21 lines)
- **Cross-component calls:** none (uses `oobb.oobb_easy`)
- **Imports needed:** `copy`, `oobb`
- **Description:** Center-aligned cube. Used by `oobb_cube`, `oobb_electronic_potentiometer_17_mm`.
- **⚠ Migrate this before 2.01 cube and 2.28 potentiometer.**

---

### 2.04 — `components/oobb_cube/working.py`
- **Source lines:** 109–111 (3 lines — just delegates to `get_oobb_cube_center`)
- **Cross-component calls:** `oobb_cube_center`
- **Imports needed:** `get_oobb_cube_center` from `oobb_cube_center`
- **Note:** The body is literally `return get_oobb_cube_center(**kwargs)`. After  
  migration it becomes `return get_oobb_cube_center(**kwargs)` where  
  `get_oobb_cube_center` is imported from the component.

---

### 2.05 — `components/oobb_cube_new/working.py`
- **Source lines:** 133–197 (65 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.06 — `components/oobb_cylinder/working.py`
- **Source lines:** 632–694 (63 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.07 — `components/oobb_cylinder_hollow/working.py`
- **Source lines:** 198–254 (57 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.08 — `components/oobb_rounded_rectangle_hollow/working.py`
- **Source lines:** 255–360 (106 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.09 — `components/oobb_rounded_rectangle_rounded/working.py`
- **Source lines:** 361–601 (241 lines)
- **Cross-component calls:** `get_rot`, `oobb.oobb_easy`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.10 — `components/oobb_sphere/working.py`
- **Source lines:** 602–631 (30 lines)
- **Cross-component calls:** none
- **Imports needed:** `copy`, `opsc`

---

### 2.11 — `components/oobb_overhang/working.py`
- **Source lines:** 1035–1088 (54 lines)
- **Cross-component calls:** none
- **Imports needed:** `copy`, `oobb`, `opsc`
- **⚠ Migrate before `oobb_motor_servo_standard_01`.**

---

### 2.12 — `components/oobb_slice/working.py`
- **Source lines:** 1104–1143 (40 lines)
- **Cross-component calls:** none
- **Imports needed:** `copy`, `oobb`, `opsc`

---

### 2.13 — `components/oobb_hole_new/working.py`
- **Source lines:** 1144–1216 (73 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.14 — `components/oobb_nut/working.py`
- **Source lines:** 1800–1948 (149 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `math`, `oobb`, `opsc`, `get_rot` from `oobb_rot`
- **Note:** Check if `math` is actually used in the body; add only if needed.

---

### 2.15 — `components/oobb_plate/working.py`
- **Source lines:** 1949–2017 (69 lines — includes `get_oobb_pl` on lines 1949–1951)
- **Cross-component calls:** `get_oobb_holes` from `oobb_get_items_base_old`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`,  
  `from oobb_get_items_base_old import get_oobb_holes`
- **shape_aliases:** keep `["oobb_pl"]`
- **Note:** `get_oobb_pl` on line 1950 is just `return get_oobb_plate(**kwargs)`.  
  The alias `oobb_pl` in `shape_aliases` already handles that. Just implement  
  the full `get_oobb_plate` body inside `action()`.

---

### 2.16 — `components/oobb_screw/working.py`
- **Source lines:** 2030–2225 (196 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`
- **⚠ Migrate before `oobb_screw_countersunk/self_tapping/socket_cap`.**

---

### 2.17 — `components/oobb_screw_countersunk/working.py`
- **Source lines:** 2018–2021 (4 lines — delegates to `get_oobb_screw`)
- **Cross-component calls:** `oobb_screw`
- **Imports needed:** `get_oobb_screw` from `oobb_screw`
- **Note:** Body is `kwargs["style"] = "countersunk"` then  
  `return get_oobb_screw(**kwargs)`.

---

### 2.18 — `components/oobb_screw_self_tapping/working.py`
- **Source lines:** 2022–2025 (4 lines — delegates to `get_oobb_screw`)
- **Cross-component calls:** `oobb_screw`
- **Imports needed:** `get_oobb_screw` from `oobb_screw`

---

### 2.19 — `components/oobb_screw_socket_cap/working.py`
- **Source lines:** 2026–2029 (4 lines — delegates to `get_oobb_screw`)
- **Cross-component calls:** `oobb_screw`
- **Imports needed:** `get_oobb_screw` from `oobb_screw`

---

### 2.20 — `components/oobb_slot/working.py`
- **Source lines:** 2226–2304 (79 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.21 — `components/oobb_tube/working.py`
- **Source lines:** 2305–2408 (104 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.22 — `components/oobb_tube_new/working.py`
- **Source lines:** 2409–2533 (125 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.23 — `components/oobb_motor_servo_standard_01/working.py`
- **Source lines:** 1217–1451 (235 lines)
- **Cross-component calls:** `get_rot`, `get_oobb_overhang`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`,  
  `from components.oobb_overhang.working import action as get_oobb_overhang`
- **Note on component import:** Because `components/` has no `__init__.py`,  
  use this pattern at the top of the file:
  ```python
  import importlib.util, os as _os
  def _import_component(rel_path):
      abs_path = _os.path.join(_PROJECT_ROOT, rel_path)
      spec = importlib.util.spec_from_file_location(rel_path, abs_path)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      return mod
  _oobb_overhang = _import_component("components/oobb_overhang/working.py")
  get_oobb_overhang = _oobb_overhang.action
  ```
  Or simply (since project root will be on sys.path after the sys.path insert at top):
  ```python
  # At top of file after sys.path insert:
  import importlib.util
  _spec = importlib.util.spec_from_file_location(
      "oobb_overhang_working",
      os.path.join(_PROJECT_ROOT, "components", "oobb_overhang", "working.py")
  )
  _mod = importlib.util.module_from_spec(_spec)
  _spec.loader.exec_module(_mod)
  get_oobb_overhang = _mod.action
  ```

---

### 2.24 — `components/oobb_motor_stepper_nema_17/working.py`
- **Source lines:** 1452–1570 (119 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.25 — `components/oobb_motor_tt_01/working.py`
- **Source lines:** 1571–1730 (160 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.26 — `components/oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible/working.py`
- **Source lines:** 1731–1799 (69 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.27 — `components/oobb_electronic_battery_box_aa_battery_4_cell/working.py`
- **Source lines:** 695–792 (98 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.28 — `components/oobb_electronic_button_11_mm_panel_mount/working.py`
- **Source lines:** 793–833 (41 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.29 — `components/oobb_electronic_potentiometer_17_mm/working.py`
- **Source lines:** 834–916 (83 lines)
- **Cross-component calls:** `get_rot`, `get_oobb_cube_center`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`,  
  + component import for `oobb_cube_center` (see pattern in 2.23)

---

### 2.30 (must do before 2.31–2.39 wire variants) — `components/oobb_electronic_potentiometer_stick_single_axis_16_mm/working.py`
- **Source lines:** 917–1034 (118 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

### 2.31 — `components/oobb_wire_cutout/working.py`  *(dependency for wire_* variants)*
- **Source lines:** 2618–2782 (165 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`
- **⚠ Migrate before all other oobb_wire_* components.**

---

### 2.32 — `components/oobb_wire_spacer_base/working.py`  *(dependency for wire_spacer variants)*
- **Source lines:** 2575–2617 (43 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`
- **⚠ Migrate before `oobb_wire_spacer`, `oobb_wire_spacer_long`, `oobb_wire_spacer_u`.**

---

### 2.33 — `components/oobb_wire_basic/working.py`
- **Source lines:** 2534–2538 (5 lines — delegates to `get_oobb_wire_cutout`)
- **Cross-component calls:** `oobb_wire_cutout`
- **Imports needed:** component import for `oobb_wire_cutout`

---

### 2.34 — `components/oobb_wire_higher_voltage/working.py`
- **Source lines:** 2539–2543 (5 lines — delegates to `get_oobb_wire_cutout`)
- **Cross-component calls:** `oobb_wire_cutout`

---

### 2.35 — `components/oobb_wire_i2c/working.py`
- **Source lines:** 2544–2548 (5 lines — delegates to `get_oobb_wire_cutout`)
- **Cross-component calls:** `oobb_wire_cutout`

---

### 2.36 — `components/oobb_wire_motor/working.py`
- **Source lines:** 2549–2553 (5 lines — delegates to `get_oobb_wire_cutout`)
- **Cross-component calls:** `oobb_wire_cutout`

---

### 2.37 — `components/oobb_wire_motor_stepper/working.py`
- **Source lines:** 2554–2558 (5 lines — delegates to `get_oobb_wire_cutout`)
- **Cross-component calls:** `oobb_wire_cutout`

---

### 2.38 — `components/oobb_wire_spacer/working.py`
- **Source lines:** 2559–2563 (5 lines — delegates to `get_oobb_wire_spacer_base`)
- **Cross-component calls:** `oobb_wire_spacer_base`

---

### 2.39 — `components/oobb_wire_spacer_long/working.py`
- **Source lines:** 2564–2568 (5 lines — delegates to `get_oobb_wire_spacer_base`)
- **Cross-component calls:** `oobb_wire_spacer_base`

---

### 2.40 — `components/oobb_wire_spacer_u/working.py`
- **Source lines:** 2569–2574 (6 lines — delegates to `get_oobb_wire_spacer_base`)
- **Cross-component calls:** `oobb_wire_spacer_base`

---

### 2.41 — `components/oobb_zip_tie_clearance_small/working.py`
- **Source lines:** 2783–2852 (70 lines)
- **Cross-component calls:** `get_rot`
- **Imports needed:** `copy`, `oobb`, `opsc`, `get_rot` from `oobb_rot`

---

## How to Import One Component from Another

Since `components/` has no `__init__.py` and is not a package, use `importlib`:

```python
# At the top of a working.py that needs another component:
import importlib.util
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Load once at module level (not inside action()):
_rot_mod = _load_component("oobb_rot")
get_rot = _rot_mod.action

_cube_center_mod = _load_component("oobb_cube_center")
get_oobb_cube_center = _cube_center_mod.action

# ... add more as needed
```

Only load components you actually call. Keep these module-level so they are  
loaded once, not on every `action()` call.

---

## Phase 3 — Stub out `oobb_get_items_base.py`

After **all** Phase 2 tasks are complete, replace each function body in  
`oobb_get_items_base.py` with a one-line delegation stub. This preserves backward  
compatibility for any code that still calls `oobb_get_items_base.get_oobb_circle(...)`.

**Template for a stub:**

```python
def get_oobb_circle(**kwargs):
    """Delegated to components/oobb_circle/working.py."""
    from components.oobb_circle import working as _m
    return _m.action(**kwargs)
```

> Do NOT delete the old function bodies yet — do Phase 3 only after Phase 2 is  
> complete and tests pass. Optionally keep the old bodies commented out.

**Also add a stub for `get_rot`:**

```python
def get_rot(**kwargs):
    from components.oobb_rot import working as _m
    return _m.action(**kwargs)
```

---

## Phase 4 — Verification

Run:
```
cd c:\gh\oomlout_oobb_version_5
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Expected result (same pre-existing failures, no new ones):
```
Ran 123 tests in ~10s
FAILED (failures=3, errors=7, skipped=1)
```

The 3 failures and 7 errors are ALL pre-existing from `oobb_make_sets.py` being  
moved to `old/`. Any new failure or error means something broke during migration.

---

## Common Mistakes to Avoid

1. **Don't import `from oobb_get_items_base_old import *`** in a working.py —  
   that drags in hundreds of names. Import only what you need explicitly.

2. **Don't use bare `gv(...)`** — always `oobb.gv(...)`.

3. **Don't use bare `opsc_easy(...)`** — always `opsc.opsc_easy(...)`.

4. **The `action()` signature must stay `**kwargs`** — callers pass arbitrary dicts.

5. **`get_oobb_pl` is just an alias** — it lives on line 1949–1951 and does  
   `return get_oobb_plate(**kwargs)`. The `oobb_pl` alias in `shape_aliases` already  
   handles dispatch. The `action()` in `oobb_plate/working.py` implements  
   `get_oobb_plate` body; no separate oobb_pl component is needed.

6. **Line numbers may shift** if the file was edited since this plan was written.  
   Always verify by searching for the `def get_oobb_xxx` line before copying.

7. **The `math` module** — some functions use `math.cos`, `math.sin`, etc.  
   Check the body and add `import math` only when needed.

8. **`oobb.remove_if`** — present in some functions; comes from `oobb.py`.  
   `import oobb` covers it.

---

## Quick Reference: Function Body Line Ranges in `oobb_get_items_base.py`

| Function | Lines | Component folder |
|---|---|---|
| `get_oobb_circle` | 7–42 | `oobb_circle` |
| `get_oobb_coupler_flanged` | 43–108 | `oobb_coupler_flanged` |
| `get_oobb_cube` | 109–111 | `oobb_cube` |
| `get_oobb_cube_center` | 112–132 | `oobb_cube_center` |
| `get_oobb_cube_new` | 133–197 | `oobb_cube_new` |
| `get_oobb_cylinder_hollow` | 198–254 | `oobb_cylinder_hollow` |
| `get_oobb_rounded_rectangle_hollow` | 255–360 | `oobb_rounded_rectangle_hollow` |
| `get_oobb_rounded_rectangle_rounded` | 361–601 | `oobb_rounded_rectangle_rounded` |
| `get_oobb_sphere` | 602–631 | `oobb_sphere` |
| `get_oobb_cylinder` | 632–694 | `oobb_cylinder` |
| `get_oobb_electronic_battery_box_aa_battery_4_cell` | 695–792 | `oobb_electronic_battery_box_aa_battery_4_cell` |
| `get_oobb_electronic_button_11_mm_panel_mount` | 793–833 | `oobb_electronic_button_11_mm_panel_mount` |
| `get_oobb_electronic_potentiometer_17_mm` | 834–916 | `oobb_electronic_potentiometer_17_mm` |
| `get_oobb_electronic_potentiometer_stick_single_axis_16_mm` | 917–1034 | `oobb_electronic_potentiometer_stick_single_axis_16_mm` |
| `get_oobb_overhang` | 1035–1088 | `oobb_overhang` |
| `get_rot` | 1089–1103 | `oobb_rot` *(new)* |
| `get_oobb_slice` | 1104–1143 | `oobb_slice` |
| `get_oobb_hole_new` | 1144–1216 | `oobb_hole_new` |
| `get_oobb_motor_servo_standard_01` | 1217–1451 | `oobb_motor_servo_standard_01` |
| `get_oobb_motor_stepper_nema_17` | 1452–1570 | `oobb_motor_stepper_nema_17` |
| `get_oobb_motor_tt_01` | 1571–1730 | `oobb_motor_tt_01` |
| `get_oobb_mechanical_motor_with_encoder_30_mm_diameter_cricut_maker_compatible` | 1731–1799 | `oobb_mechanical_motor_...` |
| `get_oobb_nut` | 1800–1948 | `oobb_nut` |
| `get_oobb_pl` | 1949–1951 | *(alias only — handled by oobb_plate)* |
| `get_oobb_plate` | 1952–2017 | `oobb_plate` |
| `get_oobb_screw_countersunk` | 2018–2021 | `oobb_screw_countersunk` |
| `get_oobb_screw_self_tapping` | 2022–2025 | `oobb_screw_self_tapping` |
| `get_oobb_screw_socket_cap` | 2026–2029 | `oobb_screw_socket_cap` |
| `get_oobb_screw` | 2030–2225 | `oobb_screw` |
| `get_oobb_slot` | 2226–2304 | `oobb_slot` |
| `get_oobb_tube` | 2305–2408 | `oobb_tube` |
| `get_oobb_tube_new` | 2409–2533 | `oobb_tube_new` |
| `get_oobb_wire_basic` | 2534–2538 | `oobb_wire_basic` |
| `get_oobb_wire_higher_voltage` | 2539–2543 | `oobb_wire_higher_voltage` |
| `get_oobb_wire_i2c` | 2544–2548 | `oobb_wire_i2c` |
| `get_oobb_wire_motor` | 2549–2553 | `oobb_wire_motor` |
| `get_oobb_wire_motor_stepper` | 2554–2558 | `oobb_wire_motor_stepper` |
| `get_oobb_wire_spacer` | 2559–2563 | `oobb_wire_spacer` |
| `get_oobb_wire_spacer_long` | 2564–2568 | `oobb_wire_spacer_long` |
| `get_oobb_wire_spacer_u` | 2569–2574 | `oobb_wire_spacer_u` |
| `get_oobb_wire_spacer_base` | 2575–2617 | `oobb_wire_spacer_base` |
| `get_oobb_wire_cutout` | 2618–2782 | `oobb_wire_cutout` |
| `get_oobb_zip_tie_clearance_small` | 2783–2852 | `oobb_zip_tie_clearance_small` |

---

## Example: Completed Migration of `oobb_circle`

### Before (current `components/oobb_circle/working.py`):
```python
d = {}

def define():
    global d
    if not d:
        d = {
            "name": "oobb_circle",
            ...
        }
    return dict(d)

def action(**kwargs):
    """Geometry wrapper -- delegates to oobb_get_items_base.get_oobb_circle."""
    import oobb_get_items_base
    return oobb_get_items_base.get_oobb_circle(**kwargs)
```

### After (with inline code from lines 7–42):
```python
import copy
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import oobb
import opsc

d = {}


def define():
    global d
    if not d:
        d = {
            "name": "oobb_circle",
            "name_long": "OOBB Geometry: Oobb Circle",
            "description": "Circle geometry primitive (cylinder cutout/solid).",
            "category": "OOBB Geometry Primitives",
            "shape_aliases": [],
        }
    return dict(d)


def action(**kwargs):
    """Circle geometry — cylinder cutout or solid at OOBB grid position."""
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    extra_mm = kwargs.get("extra_mm", False)
    pos = kwargs.get("pos", [0, 0, 0])
    depth = kwargs.get("depth", 3)
    zz = kwargs.get("zz", "bottom")

    if extra_mm:
        width = width + 1/15
        height = height + 1/15

    if zz == "bottom":
        pos[2] += 0
    elif zz == "top":
        pos[2] += -depth
    elif zz == "middle":
        pos[2] += -depth/2

    width_mm = width * oobb.gv("osp") - oobb.gv("osp_minus")
    height_mm = height * oobb.gv("osp") - oobb.gv("osp_minus")

    p3 = copy.deepcopy(kwargs)
    p3["shape"] = "cylinder"
    p3["r"] = (width * oobb.gv("osp") - oobb.gv("osp_minus")) / 2
    p3["h"] = depth
    return [opsc.opsc_easy(**p3)]
```
