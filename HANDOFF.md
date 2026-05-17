# SVG Pipeline — Claude Code Handoff

## Goal
Add SVG file generation to the OOBB project (https://github.com/oobb) in
exactly the same declarative style used in `working_scad.py` / `scad_help.py`.
The SVG output targets **laser-cut flat parts** (same as the existing `laser`
mode in `opsc.py`).

---

## What Was Built

### Two new files

| File | Role | Analogue |
|---|---|---|
| `opsvg.py` | SVG rendering pipeline | `opsc.py` |
| `working_svg.py` | Part definitions | `working_scad.py` |

Both files drop straight into the project root alongside `oobb.py`, `opsc.py`
and `working_scad.py`. No changes to existing files are needed.

---

## opsvg.py — Rendering Pipeline

**Key public API:**

```python
# Store a shape onto a thing dict (mirrors oobb.append_full)
opsvg.svg_append(thing, **p3)

# Write thing["svg_components"] → an SVG file
opsvg.opsvg_make_object(filename, thing["svg_components"], overwrite=True)

# Return the SVG as a string (no file write)
opsvg.opsvg_get_svg(components)
```

**Shape vocabulary** (set via `p3["shape"]`):

| shape | params | notes |
|---|---|---|
| `rect` | `size=[w,h,_]` | axis-aligned rectangle |
| `circle` / `hole` | `r=<mm>` | filled circle |
| `slot` | `r=<mm>`, `w=<length mm>` | capsule (two semicircles + rect) |
| `rounded_rectangle` | `size=[w,h,_]`, `r=<mm>` | rect with corner radius |
| `polygon` | `points=[[x,y],...]` | arbitrary polygon |
| `text` | `text`, `size`, `font`, `halign`, `valign` | SVG text label |
| `oobb_plate` | `width`, `height` (OOBB units) | rounded-rect on 15 mm grid |
| `oobb_holes` | `width`, `height`, `radius_name` | circle grid on 15 mm grid |
| `oobb_circle` | `diameter` (OOBB units) | solid disc |

**Type values:** `"positive"` / `"p"` = material, `"negative"` / `"n"` = cutout.

**Coordinate system:** OOBB mm, origin at part centre, Y-up. The renderer
auto-flips Y for SVG (Y-down) and computes the viewBox from the bounding box.

**OOBB variable resolution:** Hole-radius variables carry mode suffixes in this
project (`hole_radius_m6_laser`, `hole_radius_m6_true`, etc.). `_gv()` in
`opsvg.py` tries the bare name first, then appends `_laser` automatically, so
`radius_name="m6"` just works.

---

## working_svg.py — Part Definitions

**Entry point:**
```bash
python working_svg.py          # generate all parts → svg_parts/<name>/<name>.svg
python working_svg.py none     # dry run, no files written
python working_svg.py all bracket   # only parts whose name contains "bracket"
```

**Pattern — identical to working_scad.py:**

```python
def get_my_part(thing, **kwargs):
    pos    = kwargs.get("pos",    [0, 0, 0])
    width  = kwargs.get("width",  2)
    height = kwargs.get("height", 1)

    # positive body
    p3 = copy.deepcopy(kwargs)
    p3["type"]  = "positive"
    p3["shape"] = "oobb_plate"     # or rect, circle, slot, rounded_rectangle …
    p3["pos"]   = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)  # ← only difference from working_scad.py

    # negative holes
    p3 = copy.deepcopy(kwargs)
    p3["type"]        = "negative"
    p3["shape"]       = "oobb_holes"
    p3["radius_name"] = "m6"
    p3["pos"]         = copy.deepcopy(pos)
    opsvg.svg_append(thing, **p3)
```

**Register a new part in `get_parts()`:**

```python
parts.append({
    "name":      "my_part_2x3",   # → svg_parts/my_part_2x3/my_part_2x3.svg
    "oobb_name": "my_part",       # → calls get_my_part(thing, **kwargs)
    "kwargs": {
        "width":  2,
        "height": 3,
        "depth":  3,
    },
})
```

**Parts built and tested (all pass):**

| name | builder | description |
|---|---|---|
| `plate_1x1` | `get_plate` | 1×1 OOBB plate, M6 holes |
| `plate_2x1` | `get_plate` | 2×1 OOBB plate, M6 holes |
| `plate_4x2` | `get_plate` | 4×2 OOBB plate, 8×M6 holes |
| `circle_dia3` | `get_oobb_circle` | 45 mm disc, centre M6 hole |
| `bracket_4x2` | `get_bracket` | L-shape from two rounded-rects |
| `mount_slot_2x1` | `get_mount_slot` | plate with vertical capsule slots |

---

## Key Design Decisions

1. **`svg_append` instead of `oobb.append_full`** — `append_full` resolves
   shape names through the component registry (`components/*/working.py`).
   That registry doesn't contain SVG-specific shapes (`rect`, `slot`, etc.),
   so we bypass it. `svg_append` stores the raw kwargs dict directly into
   `thing["svg_components"]`. Everything else (the `p3 = copy.deepcopy(kwargs)`
   / `p3["type"]` / `p3["pos"]` pattern) is identical.

2. **Painter's algorithm for positive/negative** — positives are drawn first in
   fill colour, negatives on top in background colour. Same approach as the
   existing laser DXF output in `opsc.py`.

3. **Auto bounding box** — `opsvg_get_svg` scans all components to compute
   the viewBox, so you never set canvas dimensions manually.

4. **OOBB unit sizes** — `osp=15`, `osp_minus=1`, so a 2×1 plate body is
   `(2×15-1) × (1×15-1) = 29×14 mm`.

---

## Suggested Next Steps

- **`svg_help.py`** — a `make_svg_generic` / `make_parts` orchestrator
  analogous to `scad_help.py`, so the pipeline can be driven from a single
  `get_parts()` list rather than calling `make_svg_generic` manually.
- **Additional shapes** — `polygon_tube` (ring), `text_hollow`, `arc`.
- **Colour themes** — pass `fill=` / `cut=` to `opsvg_make_object` for
  different material colours (e.g. red on white for Inkscape laser layers).
- **DXF output** — `opsvg.py`'s bounding-box + shape logic could be adapted
  to emit DXF directly, replacing the SolidPython2 → OpenSCAD → DXF chain for
  flat parts.
- **`rot` on oobb_holes** — currently holes are always axis-aligned; a `rot`
  on the group would support rotated hole patterns.

---

## File Locations

```
project/
  opsvg.py          ← NEW: SVG rendering pipeline
  working_svg.py    ← NEW: part definitions
  oobb.py           existing (unchanged)
  opsc.py           existing (unchanged)
  working_scad.py   existing (unchanged)
  scad_help.py      existing (unchanged)
  svg_parts/        generated output directory
    plate_1x1/plate_1x1.svg
    plate_2x1/plate_2x1.svg
    plate_4x2/plate_4x2.svg
    circle_dia3/circle_dia3.svg
    bracket_4x2/bracket_4x2.svg
    mount_slot_2x1/mount_slot_2x1.svg
```
