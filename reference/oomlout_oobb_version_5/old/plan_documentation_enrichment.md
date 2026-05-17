# Documentation Enrichment Plan
_Style: roboclick-parity — rich `define()` metadata in every `components/*/working.py`_

---

## Background & Context

The documentation system is already fully built:
- **`components/documentation.py`** — discovers, normalises and exports (`export_documentation_json`, `export_documentation_html`, `export_documentation_markdown`)
- **`templates/oobb_documentation_template.html`** — SPA with `<!-- DOCUMENTATION_DATA_PLACEHOLDER -->` injection point
- **`oobb_arch/catalog/object_discovery.py`** and `part_set_discovery.py` — auto-scan `components/*/working.py` files and call `define()` on each

The only gap is **data quality in `define()`**. Currently most components have:
```python
{
    "name": "oobb_cube_center",
    "name_long": "OOBB Geometry: Oobb Cube Center",
    "description": "Center-aligned cube geometry primitive.",
    "category": "OOBB Geometry Primitives",
    "shape_aliases": [],        # always empty
    # variables: missing entirely, or bare string list
    # returns: missing
}
```

The roboclick target schema requires:
```python
{
    "name": "oobb_cube_center",
    "name_long": "OOBB Geometry: Oobb Cube Center",
    "description": "Center-aligned cube geometry primitive.",
    "category": "OOBB Geometry Primitives",
    "shape_aliases": ["cube_center"],           # meaningful aliases
    "variables": [
        {"name": "pos",  "description": "3-element [x, y, z] position.", "type": "list",   "default": "[0, 0, 0]"},
        {"name": "size", "description": "3-element [x, y, z] size.",     "type": "list",   "default": "[1, 1, 1]"},
        {"name": "zz",   "description": "Vertical alignment: bottom / center / top.", "type": "string", "default": "bottom"},
    ],
    "returns": "List of geometry dicts.",
}
```

---

## What Must Be Done

### Step 1 — Wire up the regeneration script  `[x]`
Create `action_documentation_regenerate.bat` in the project root that calls `components/documentation.py` with the correct paths. This ensures running one file regenerates everything.

Produces:
- `components/documentation_data.json`
- `components/documentation.html`

### Step 2 — Enrich `define()` in geometry primitives (oobb_*) `[x]`
~40 components under `components/oobb_*/working.py`.  
Each needs: `variables` as rich dicts, `returns`, populated `shape_aliases`.

| Component | Status |
|-----------|--------|
| oobb_circle | `[ ]` |
| oobb_coupler_flanged | `[ ]` |
| oobb_cube | `[ ]` |
| oobb_cube_center | `[ ]` |
| oobb_cube_new | `[ ]` |
| oobb_cylinder | `[ ]` |
| oobb_cylinder_hollow | `[ ]` |
| oobb_electronic_arduino_nano | `[ ]` |
| oobb_electronic_arduino_uno | `[ ]` |
| oobb_electronic_pi_pico | `[ ]` |
| oobb_electronic_raspberry_pi_4 | `[ ]` |
| oobb_hole_new | `[ ]` |
| oobb_mechanical_motor_nema17 | `[ ]` |
| oobb_motor_servo_standard_01 | `[ ]` |
| oobb_motor_tt_01 | `[ ]` |
| oobb_nut | `[ ]` |
| oobb_overhang | `[ ]` |
| oobb_plate | `[ ]` |
| oobb_rot | `[ ]` |
| oobb_rounded_rectangle_hollow | `[ ]` |
| oobb_rounded_rectangle_rounded | `[ ]` |
| oobb_screw | `[ ]` |
| oobb_screw_countersunk | `[ ]` |
| oobb_screw_self_tapping | `[ ]` |
| oobb_screw_socket_cap | `[ ]` |
| oobb_slice | `[ ]` |
| oobb_slot | `[ ]` |
| oobb_sphere | `[ ]` |
| oobb_tube | `[ ]` |
| oobb_tube_new | `[ ]` |
| oobb_wire_cutout | `[ ]` |
| oobb_wire_cutout_2 | `[ ]` |
| oobb_wire_cutout_3 | `[ ]` |
| oobb_wire_cutout_lug | `[ ]` |
| oobb_wire_cutout_mains | `[ ]` |
| oobb_wire_cutout_panel | `[ ]` |
| oobb_wire_dc_barrel | `[ ]` |
| oobb_wire_d_sub | `[ ]` |
| oobb_wire_ethernet | `[ ]` |
| oobb_wire_hdmi | `[ ]` |
| oobb_wire_usb_a | `[ ]` |
| oobb_wire_usb_b | `[ ]` |
| oobb_wire_usb_c | `[ ]` |
| oobb_zip_tie_clearance_small | `[ ]` |

### Step 3 — Enrich `define()` in Part Set components `[x]`
~25 set components under `components/*/working.py` (plural names).  
Each needs `variables` enriched and `category` verified.

| Component | Status |
|-----------|--------|
| bearings | `[ ]` |
| bearing_circles | `[ ]` |
| bearing_plates | `[ ]` |
| circles | `[ ]` |
| gears | `[ ]` |
| holders | `[ ]` |
| jacks | `[ ]` |
| jigs | `[ ]` |
| mounting_plates | `[ ]` |
| nuts | `[ ]` |
| others | `[ ]` |
| plates | `[ ]` |
| pulleys | `[ ]` |
| screws | `[ ]` |
| shafts | `[ ]` |
| shaft_couplers | `[ ]` |
| smd_magazines | `[ ]` |
| soldering_jigs | `[ ]` |
| tests | `[ ]` |
| tool_holders | `[ ]` |
| trays | `[ ]` |
| wheels | `[ ]` |
| wires | `[ ]` |
| ziptie_holders | `[ ]` |
| buntings | `[ ]` |

### Step 4 — Enrich `define()` in Variant / Product components `[x]`
~90 product components (holders, plates, testers, etc.).  
These tend to have more parameters and are highest value for doc users.

| Component | Status |
|-----------|--------|
| bearing_plate_connecting_screw_center | `[ ]` |
| bearing_plate_hole_m3 | `[ ]` |
| bearing_plate_hole_m3_captive | `[ ]` |
| bearing_plate_hole_m4 | `[ ]` |
| bearing_plate_hole_m5 | `[ ]` |
| bearing_plate_hole_m6 | `[ ]` |
| bearing_plate_hole_m8 | `[ ]` |
| bearing_plate_jack | `[ ]` |
| bearing_plate_jack_basic | `[ ]` |
| bearing_plate_old | `[ ]` |
| bearing_plate_plate | `[ ]` |
| bearing_plate_shim | `[ ]` |
| bearing_wheel | `[ ]` |
| bolt | `[ ]` |
| bracket_2020_aluminium_extrusion | `[ ]` |
| circle_base | `[ ]` |
| circle_captive | `[ ]` |
| circle_old_1 | `[ ]` |
| ci_holes_center | `[ ]` |
| gear_double_stack | `[ ]` |
| gridfinity_base_tile | `[ ]` |
| holder_electronics_* (6 variants) | `[ ]` |
| holder_electronic_* (5 variants) | `[ ]` |
| holder_fan_120_mm | `[ ]` |
| holder_motor_* (16 variants) | `[ ]` |
| holder_old | `[ ]` |
| holder_powerbank_anker_323 | `[ ]` |
| jack_basic | `[ ]` |
| jig_screw_sorter_m3_03_03 | `[ ]` |
| jig_tray_03_03 | `[ ]` |
| mounting_plate_generic | `[ ]` |
| mounting_plate_side | `[ ]` |
| mounting_plate_top | `[ ]` |
| mounting_plate_u | `[ ]` |
| nut_m3 | `[ ]` |
| other_bolt_stacker* (2 variants) | `[ ]` |
| other_corner_cube* (3 variants) | `[ ]` |
| other_ptfe_tube_holder* (2 variants) | `[ ]` |
| other_timing_belt_clamp_gt2 | `[ ]` |
| plate_base | `[ ]` |
| plate_dict | `[ ]` |
| plate_hole_dict | `[ ]` |
| plate_l | `[ ]` |
| plate_label | `[ ]` |
| plate_ninety_degree | `[ ]` |
| plate_nut_dict | `[ ]` |
| plate_old | `[ ]` |
| plate_t | `[ ]` |
| plate_u | `[ ]` |
| plate_u_double | `[ ]` |
| pulley_gt2_shield_double | `[ ]` |
| screw_countersunk | `[ ]` |
| screw_self_tapping | `[ ]` |
| screw_socket_cap | `[ ]` |
| shaft_center | `[ ]` |
| smd_magazine_* (8 variants) | `[ ]` |
| soldering_jig_electronics_mcu_pi_pico_socket | `[ ]` |
| standoff | `[ ]` |
| test_gear | `[ ]` |
| test_hole | `[ ]` |
| test_motor_* (15 variants) | `[ ]` |
| threaded_insert | `[ ]` |
| tool_holder_* (3 variants) | `[ ]` |
| tray_* (6 variants) | `[ ]` |
| trt_old | `[ ]` |
| wheel_old_1 | `[ ]` |
| ziptie_holder_jack | `[ ]` |

### Step 5 — Regenerate and verify `[x]`
Run `action_documentation_regenerate.bat` and open `components/documentation.html` to verify output.

---

## Enriched `define()` Schema Reference

Every `working.py` define() should match this shape:

```python
def define():
    global d
    if not d:
        d = {
            "name": "folder_name_exactly",
            "name_long": "OOBB Category: Human Name",
            "description": "One sentence describing what this produces.",
            "category": "One of: OOBB Geometry Primitives | OOBB Wire Cutouts | OOBB Electronics | OOBB Mechanical | Part Sets | Plates | Holders | Bearing Plates | Jigs | Gears | Circles | Shafts | Fasteners | Gridfinity | Other",
            "shape_aliases": ["short_alias"],   # list of short names usable in oobb_easy()
            "variables": [
                {"name": "pos",  "description": "...", "type": "list",   "default": "[0,0,0]"},
                {"name": "size", "description": "...", "type": "string", "default": "oobb"},
                # ...
            ],
            "returns": "List of geometry component dicts.",
        }
    return dict(d)
```

**Category vocabulary** (use these exact strings for consistent grouping):
- `OOBB Geometry Primitives` — basic cube/cylinder/circle/sphere shapes
- `OOBB Wire Cutouts` — oobb_wire_* components
- `OOBB Electronics` — oobb_electronic_* components
- `OOBB Mechanical` — motors, servos, bearings
- `Part Sets` — plural set builders (bearings, plates, etc.)
- `Plates` — flat plate variants
- `Holders` — part holders
- `Bearing Plates` — bearing_plate_* variants
- `Jigs` — assembly jigs
- `Gears` — gear components
- `Circles` — circle variants
- `Shafts` — shaft builders
- `Fasteners` — screws, nuts, bolts
- `Gridfinity` — gridfinity system components
- `Other` — catch-all

---

## Progress Log

| Date | Step | Notes |
|------|------|-------|
| 2026-04-19 | Plan created | Investigated roboclick reference; existing pipeline confirmed working |
| 2026-04-19 | Step 1 done | Created `action_documentation_regenerate.bat` |

---

## Status Summary

| Step | Status | Count |
|------|--------|-------|
| 1 — Create regeneration bat | `[x]` Done | 1 file |
| 2 — Enrich oobb_* geometry | `[ ]` Not started | ~44 components |
| 3 — Enrich Part Set components | `[ ]` Not started | ~25 components |
| 4 — Enrich Variant/Product components | `[ ]` Not started | ~90 components |
| 5 — Regenerate and verify | `[ ]` Not started | — |

**Total components to enrich: ~160**
