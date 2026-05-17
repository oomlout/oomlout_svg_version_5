# Documentation & Styling Plan

Goal: get all 24 components into the OOBB documentation site with good
metadata and a modern, roboclick-style pastel glassmorphism design.

---

## Progress

- [x] `describe()+define()` with `v.append()` pattern applied to all 24 real component `working.py` files
- [x] Full metadata (description, category, variables with types/defaults, returns, shape_aliases) added to all 24
- [x] Fix documentation pipeline (broken since `oobb_arch` moved to `old/`)
  - [x] Add `sys.path` setup in `components/documentation.py` so `oobb_arch` in `old/` is found
  - [x] Update `action_documentation_regenerate.bat` to pass `--objects-root components`
- [x] All 24 components confirmed in generated `components/documentation_data.json`
- [x] Create `templates/oobb_documentation_template.html` — roboclick pastel rainbow style
  - [x] Animated gradient background (`gradientShift` 20s)
  - [x] Glassmorphism cards (`rgba(255,255,255,0.65)`, `blur(16px)`)
  - [x] Inter + Poppins fonts via Google Fonts
  - [x] `fadeInUp` card animations
  - [x] Rainbow top-bar accent on each card
  - [x] Variable chips with click-to-reveal descriptions
  - [x] Search + category filter
  - [x] Stats bar (total count)
- [x] Fix `gridfinity_base_tile` — added 7 variables that were missing
- [x] Reclassify fasteners: oobb_screw, oobb_screw_countersunk, oobb_screw_self_tapping, oobb_screw_socket_cap, oobb_nut → category "Fasteners"
- [x] Regenerated docs — all 24 components with correct categories and variable counts
- [ ] Open `components/documentation.html` in browser and do final visual check

---

## 24 Real Components

| # | Component | describe() ✓ | In docs ✓ | Category |
|---|-----------|--------------|-----------|----------|
| 1 | bolt | ✓ | ✓ | Fasteners |
| 2 | gridfinity_base_tile | ✓ | ✓ | Gridfinity |
| 3 | oobb_circle | ✓ | ✓ | OOBB Geometry Primitives |
| 4 | oobb_coupler_flanged | ✓ | ✓ | OOBB Mechanical |
| 5 | oobb_cube | ✓ | ✓ | OOBB Geometry Primitives |
| 6 | oobb_cube_center | ✓ | ✓ | OOBB Geometry Primitives |
| 7 | oobb_cube_new | ✓ | ✓ | OOBB Geometry Primitives |
| 8 | oobb_cylinder | ✓ | ✓ | OOBB Geometry Primitives |
| 9 | oobb_cylinder_hollow | ✓ | ✓ | OOBB Geometry Primitives |
| 10 | oobb_hole_new | ✓ | ✓ | OOBB Geometry Primitives |
| 11 | oobb_nut | ✓ | ✓ | Fasteners |
| 12 | oobb_plate | ✓ | ✓ | OOBB Geometry Primitives |
| 13 | oobb_rot | ✓ | ✓ | OOBB Geometry Helpers |
| 14 | oobb_rounded_rectangle_hollow | ✓ | ✓ | OOBB Geometry Primitives |
| 15 | oobb_rounded_rectangle_rounded | ✓ | ✓ | OOBB Geometry Primitives |
| 16 | oobb_screw | ✓ | ✓ | Fasteners |
| 17 | oobb_screw_countersunk | ✓ | ✓ | Fasteners |
| 18 | oobb_screw_self_tapping | ✓ | ✓ | Fasteners |
| 19 | oobb_screw_socket_cap | ✓ | ✓ | Fasteners |
| 20 | oobb_slice | ✓ | ✓ | OOBB Geometry Primitives |
| 21 | oobb_slot | ✓ | ✓ | OOBB Geometry Primitives |
| 22 | oobb_sphere | ✓ | ✓ | OOBB Geometry Primitives |
| 23 | oobb_tube | ✓ | ✓ | OOBB Geometry Primitives |
| 24 | oobb_tube_new | ✓ | ✓ | OOBB Geometry Primitives |

---

## Root Causes of Broken Pipeline

1. `oobb_arch` moved to `old/oobb_arch/` — `components/documentation.py` imports it at the top level with no path setup
2. `old/oobb_arch/catalog/object_discovery.py` default `objects_root` resolves to `old/components/` (non-existent) rather than `components/`

## Fixes Applied

- `components/documentation.py` — added `sys.path.insert(0, old/)` before `oobb_arch` import
- `action_documentation_regenerate.bat` — added `--objects-root "components"`
- `templates/oobb_documentation_template.html` — created from scratch, roboclick pastel rainbow style
- `components/gridfinity_base_tile/working.py` — added 7 variables to `describe()`
- `components/oobb_{screw,screw_countersunk,screw_self_tapping,screw_socket_cap,nut}/working.py` — changed category to "Fasteners"
