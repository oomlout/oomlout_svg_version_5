# Plan: SVG Components Library + Rewritten Pipeline

## Status Legend
- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked / needs attention

## Overall Progress
`[x]` Phase 0 — Archive originals  
`[x]` Phase 1 — svg_components/ library (9 files)  
`[x]` Phase 2 — Rewrite opsvg.py  
`[x]` Phase 3 — Rewrite working_svg.py  
`[x]` Phase 4 — Verify + update CLAUDE.md  

---

## Resumption checklist

If this session is interrupted, start here:

1. Check which tasks below are `[x]` complete.
2. Find the first `[ ]` or `[~]` task and continue from there.
3. Run `python working_svg.py` at the end to confirm both SVGs generate cleanly.

---

## Phase 0 — Archive originals

**Goal:** preserve originals verbatim before any rewrites.

- `[x]` 0.1 — Create `reference/old/` folder if it does not exist
- `[x]` 0.2 — Copy `opsvg.py` → `reference/old/opsvg.py`
- `[x]` 0.3 — Copy `working_svg.py` → `reference/old/working_svg.py`

---

## Phase 1 — svg_components/ library

**Goal:** one `working.py` per shape, following the `components/*/working.py` contract from `oomlout_oobb_version_5`.

### Contract every working.py must satisfy

```python
def describe():
    """Return metadata dict: name, description, category, variables list."""

def define():
    """Return copy of describe() dict (call describe() if needed)."""

def action(**kwargs):
    """Return list of shape-descriptor dicts for opsvg._render_shape()."""
```

`describe()` variable entries:
```python
{"name": "r", "description": "Corner radius in mm", "type": "float", "default": 2.0}
```

### Tasks

- `[ ]` 1.1 — `svg_components/rect/working.py`
  - kwargs: `type`, `size=[w,h,d]`, `pos=[0,0,0]`, `rot=[0,0,0]`
  - action: returns `[{"type":…, "shape":"rect", "size":…, "pos":…, "rot":…}]`

- `[ ]` 1.2 — `svg_components/circle/working.py`
  - kwargs: `type`, `r`, `pos=[0,0,0]`
  - shape_aliases: `["hole"]`
  - action: returns `[{"type":…, "shape":"circle", "r":…, "pos":…}]`

- `[ ]` 1.3 — `svg_components/slot/working.py`
  - kwargs: `type`, `r`, `w`, `pos=[0,0,0]`, `rot=[0,0,0]`
  - note: `rot=[0,0,90]` for vertical slot
  - action: returns `[{"type":…, "shape":"slot", "r":…, "w":…, "pos":…, "rot":…}]`

- `[ ]` 1.4 — `svg_components/rounded_rectangle/working.py`
  - kwargs: `type`, `size=[w,h,d]`, `r=2.0`, `pos=[0,0,0]`, `rot=[0,0,0]`
  - shape_aliases: `["rounded_rect", "rrect"]`
  - action: returns `[{"type":…, "shape":"rounded_rectangle", …}]`

- `[ ]` 1.5 — `svg_components/polygon/working.py`
  - kwargs: `type`, `points=[[x,y],…]`, `pos=[0,0,0]`, `rot=[0,0,0]`
  - action: returns `[{"type":…, "shape":"polygon", "points":…, "pos":…}]`

- `[ ]` 1.6 — `svg_components/text/working.py`
  - kwargs: `type="positive"`, `text=""`, `size=4.0`, `font="sans-serif"`, `halign="center"`, `valign="center"`, `color`, `pos=[0,0,0]`
  - action: returns `[{"type":…, "shape":"text", …}]`

- `[ ]` 1.7 — `svg_components/oobb_plate/working.py`
  - kwargs: `type="positive"`, `width=1`, `height=1`, `corner_radius=2.0`, `pos=[0,0,0]`
  - action: returns `[{"type":…, "shape":"oobb_plate", …}]`

- `[ ]` 1.8 — `svg_components/oobb_holes/working.py`
  - kwargs: `type="negative"`, `width=1`, `height=1`, `radius_name="m6"`, `pos=[0,0,0]`
  - action: returns `[{"type":…, "shape":"oobb_holes", …}]`

- `[ ]` 1.9 — `svg_components/oobb_circle/working.py`
  - kwargs: `type="positive"`, `diameter=1`, `pos=[0,0,0]`
  - action: returns `[{"type":…, "shape":"oobb_circle", "diameter":…, "pos":…}]`

---

## Phase 2 — Rewrite opsvg.py

**Goal:** clean rewrite. Public API identical to original. Adds component discovery
and `svg_easy()` / `se()` dispatcher. All render/bbox/helper internals kept the same.

### Module structure (top to bottom)

```
imports
module docstring
constants          (_OSP, _OSP_MINUS, _FILL_*, _PADDING_MM, _CORNER_RADIUS)
_gv() / _hole_pos()           helpers — unchanged from original
_discover_components()        NEW
_COMPONENT_MAP                populated at import time
─── Public API ───────────────────────────────────────────────────────
svg_init()
svg_append()                  unchanged
svg_easy() / se()             NEW
opsvg_make_object()           unchanged signature
opsvg_get_svg()               unchanged signature
─── Shape renderers ──────────────────────────────────────────────────
_render_shape()
_oobb_plate() / _oobb_holes()
─── Bounding box ─────────────────────────────────────────────────────
_bounding_box()
─── Internal helpers ─────────────────────────────────────────────────
_flatten() / _styled()
```

### New functions to add

**`_discover_components(root="svg_components")`**
- Walk `root/*/working.py`
- `importlib.util.spec_from_file_location` each file
- Call `module.define()` to get metadata + aliases
- Return `{shape_name: module, alias: module, …}`
- Fail gracefully (warn, skip) if a working.py is broken

**`svg_easy(thing, **kwargs)` + `se = svg_easy`**
- Look up `kwargs["shape"]` in `_COMPONENT_MAP`
- If found: call `component.action(**kwargs)` → list of dicts → `svg_append` each
- If not found: fall back to `svg_append(thing, **kwargs)` directly
- Supports list values for `shape` and `pos` the same way `svg_append` does

### Tasks

- `[ ]` 2.1 — Write new `opsvg.py` with docstring, constants, `_gv`, `_hole_pos` (copy from original)
- `[ ]` 2.2 — Add `_discover_components()` + `_COMPONENT_MAP` initialisation
- `[ ]` 2.3 — Add `svg_init()`, `svg_append()` (copy from original)
- `[ ]` 2.4 — Add `svg_easy()` / `se()` dispatcher
- `[ ]` 2.5 — Add `opsvg_make_object()`, `opsvg_get_svg()` (copy from original)
- `[ ]` 2.6 — Add `_render_shape()`, `_oobb_plate()`, `_oobb_holes()` (copy from original)
- `[ ]` 2.7 — Add `_bounding_box()`, `_flatten()`, `_styled()` (copy from original)
- `[ ]` 2.8 — Smoke-test: `python -c "import opsvg; print(opsvg._COMPONENT_MAP.keys())"` — should list all 9 shapes

---

## Phase 3 — Rewrite working_svg.py

**Goal:** human-readable `working_scad.py` style. Uses `se()` throughout.
Two demo parts: A4 sheet and 76.2 × 50.4 mm label.

### Style rules

- Long descriptive variable names (no terse single-letters except `pos`)
- Each shape block: `p3 = copy.deepcopy(kwargs)` → set fields → `se(thing, **p3)`
- Builder functions: `get_<oobb_name>(thing, **kwargs)`
- Part registry: `get_parts()` returns list of `{name, oobb_name, kwargs}` dicts
- Orchestration: `make_svg()` → `make_svg_generic()` → builder dispatch
- CLI: `sys.argv[1]` = save_type, `sys.argv[2]` = filter string

### Part 1 — `get_a4_sheet` (210 × 297 mm)

```
canvas:  210 wide × 297 tall mm, origin at centre
```

| step | type | shape | detail |
|---|---|---|---|
| 3.1a | positive | rect | full A4 background, size=[210, 297, 3] |
| 3.1b | positive | rounded_rectangle | inset content area 190×277 mm, r=5 |
| 3.1c | negative | circle | corner punch-out, r=4, pos top-left |
| 3.1d | negative | slot | horizontal slot, r=3, w=40, pos bottom-centre |
| 3.1e | positive | polygon | triangle marker, points relative to pos |
| 3.1f | positive | text | title "A4 Demo Sheet", size=14, centre-top |
| 3.1g | positive | text | subtitle "oomlout SVG pipeline", size=7 |
| 3.1h | positive | text | corner label "v1.0", size=4, bottom-right |

### Part 2 — `get_label_76x50` (76.2 × 50.4 mm)

```
canvas:  76.2 wide × 50.4 tall mm, origin at centre
```

| step | type | shape | detail |
|---|---|---|---|
| 3.2a | positive | rounded_rectangle | full label outline, r=3 |
| 3.2b | positive | rect | header bar 76.2×12 mm, pos top of label |
| 3.2c | negative | rect | header cutout (slightly inset) to separate header |
| 3.2d | positive | circle | bullet mark, r=1.5, left edge body area |
| 3.2e | positive | text | "OOMLOUT" title, size=9, in header |
| 3.2f | positive | text | part name row, size=5 |
| 3.2g | positive | text | description row, size=4 |
| 3.2h | positive | text | part-number footer, size=3, bottom-right |

### Tasks

- `[ ]` 3.1 — Write `get_a4_sheet()` builder (steps 3.1a–3.1h)
- `[ ]` 3.2 — Write `get_label_76x50()` builder (steps 3.2a–3.2h)
- `[ ]` 3.3 — Write `get_parts()` registering both parts
- `[ ]` 3.4 — Write `make_svg_generic()`, `make_svg()`, `main()`, `__main__` CLI

---

## Phase 4 — Verify + update CLAUDE.md

- `[ ]` 4.1 — Run `python working_svg.py` — confirm both SVGs written to `svg_parts/`
- `[ ]` 4.2 — Run `python working_svg.py none` — confirm dry-run prints but writes nothing
- `[ ]` 4.3 — Run `python working_svg.py all label` — confirm only label SVG written
- `[ ]` 4.4 — Update `CLAUDE.md`: document `svg_components/` folder, `se()` API, two demo parts

---

## Files touched

| file | change | status |
|---|---|---|
| `reference/old/opsvg.py` | COPY of original `opsvg.py` | `[x]` |
| `reference/old/working_svg.py` | COPY of original `working_svg.py` | `[x]` |
| `opsvg.py` | REWRITE | `[x]` |
| `working_svg.py` | REWRITE | `[x]` |
| `svg_components/rect/working.py` | NEW | `[x]` |
| `svg_components/circle/working.py` | NEW | `[x]` |
| `svg_components/slot/working.py` | NEW | `[x]` |
| `svg_components/rounded_rectangle/working.py` | NEW | `[x]` |
| `svg_components/polygon/working.py` | NEW | `[x]` |
| `svg_components/text/working.py` | NEW | `[x]` |
| `svg_components/oobb_plate/working.py` | NEW | `[x]` |
| `svg_components/oobb_holes/working.py` | NEW | `[x]` |
| `svg_components/oobb_circle/working.py` | NEW | `[x]` |
| `CLAUDE.md` | UPDATE | `[x]` |
