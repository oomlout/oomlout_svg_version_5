# Plan: SVG Components Library + Rewritten Pipeline

## Goal

Three deliverables:

1. **Archive originals** — move `opsvg.py` and `working_svg.py` to `reference/old/` before any rewrites.
2. **Rewritten `opsvg.py`** — clean, components-aware rendering pipeline with discovery built in from the start. Keeps the same public surface (`svg_append`, `opsvg_make_object`, `opsvg_get_svg`) but adds `svg_easy()` / `se()` dispatcher and `_discover_components()` wiring.
3. **SVG component library** — `svg_components/<name>/working.py` for every shape, in the `components/*/working.py` contract from `oomlout_oobb_version_5`.
4. **Rewritten `working_svg.py`** — replaces the old file; uses `se()` / `svg_easy()` in the human-readable `working_scad.py` style, with an A4 sheet and a 76.2 × 50.4 mm label as demo parts.

---

## Phase 0 — Archive originals

```
reference/old/opsvg.py          ← moved from opsvg.py
reference/old/working_svg.py    ← moved from working_svg.py
```

Both files are preserved verbatim. No content changes during the move.

---

## Phase 1 — svg_components/ library

### Folder layout

```
svg_components/
  rect/working.py
  circle/working.py
  slot/working.py
  rounded_rectangle/working.py
  polygon/working.py
  text/working.py
  oobb_plate/working.py
  oobb_holes/working.py
  oobb_circle/working.py
```

### working.py contract (mirrors OOBB `components/*/working.py`)

Every file implements three functions:

```python
def describe():
    """Return a metadata dict with name, description, category, variables list."""

def define():
    """Call describe() if needed; return a copy of the metadata dict."""

def action(**kwargs):
    """
    Return a list of one or more shape-descriptor dicts.
    Each dict must contain at least:
        type   – "positive" or "negative"
        shape  – the shape key recognised by opsvg._render_shape()
        pos    – [x, y, z] in OOBB mm
    """
```

`describe()` variable entries follow the same schema used upstream:

```python
{"name": "r", "description": "Corner radius in mm", "type": "float", "default": 2.0}
```

### Component details

| component | key kwargs | notes |
|---|---|---|
| `rect` | `type`, `size=[w,h,d]`, `pos`, `rot` | raw rectangle |
| `circle` | `type`, `r`, `pos` | alias: `hole` |
| `slot` | `type`, `r`, `w`, `pos`, `rot` | capsule; rot[2]=90 → vertical |
| `rounded_rectangle` | `type`, `size=[w,h,d]`, `r`, `pos`, `rot` | corner radius |
| `polygon` | `type`, `points=[[x,y],...]`, `pos`, `rot` | arbitrary shape |
| `text` | `type`, `text`, `size`, `font`, `halign`, `valign`, `pos` | SVG text, default positive |
| `oobb_plate` | `type`, `width`, `height`, `corner_radius`, `pos` | OOBB-grid rounded rect |
| `oobb_holes` | `type`, `width`, `height`, `radius_name`, `pos` | OOBB hole grid |
| `oobb_circle` | `type`, `diameter`, `pos` | solid disc |

---

## Phase 2 — Rewritten opsvg.py

Rewrite from scratch (original archived to `reference/old/`).  
Public API is **identical** to the original — existing code calling `svg_append`, `opsvg_make_object`, `opsvg_get_svg` continues to work unchanged.

New additions:

### `_discover_components(root="svg_components")`

```python
def _discover_components(root="svg_components"):
    """
    Scan root/ for */working.py files. Import each as a module.
    Build and return a dict:  shape_name → module
    Also registers any aliases declared in define()["shape_aliases"].
    Called once at import time; result cached in _COMPONENT_MAP.
    """
```

### `svg_easy(thing, **kwargs)` / `se(thing, **kwargs)`

```python
def svg_easy(thing, **kwargs):
    """
    High-level dispatcher analogous to oobb.oobb_easy() / oe().

    1. Looks up kwargs["shape"] in _COMPONENT_MAP.
    2. Calls component.action(**kwargs) → list of shape dicts.
    3. Appends each dict to thing["svg_components"] via svg_append().

    Falls back to svg_append() directly for any shape not in the map,
    so mixing se() and svg_append() in the same builder is safe.
    """

se = svg_easy   # short alias
```

### Internal shape renderers

The `_render_shape()` internals stay the same; the only structural change is that
`_COMPONENT_MAP` is populated at import time so `se()` can dispatch through it.

### Module-level structure (new opsvg.py)

```
imports
constants  (_OSP, _OSP_MINUS, _FILL_*, _PADDING_MM, _CORNER_RADIUS)
_gv() / _hole_pos()          ← unchanged helpers
_discover_components()        ← NEW
_COMPONENT_MAP = _discover_components()   ← populated at import

# ── Public API ────────────────────────────────────────────────────────
svg_init()
svg_append()                  ← unchanged
svg_easy() / se()             ← NEW

opsvg_make_object()           ← unchanged
opsvg_get_svg()               ← unchanged

# ── Shape renderers ───────────────────────────────────────────────────
_render_shape()               ← unchanged
_oobb_plate() / _oobb_holes() ← unchanged

# ── Bounding box ──────────────────────────────────────────────────────
_bounding_box()               ← unchanged

# ── Helpers ───────────────────────────────────────────────────────────
_flatten() / _styled()        ← unchanged
```

---

## Phase 3 — Rewritten working_svg.py

Replaces the original (which is archived). Uses `se()` throughout.

### Style rules (matching working_scad.py)

- Long, descriptive variable names
- Every `p3` block: deepcopy kwargs → set type/shape/pos → call `se()`
- Parts defined in `get_parts()` as a list of `{name, oobb_name, kwargs}` dicts
- Builder functions named `get_<oobb_name>(thing, **kwargs)`
- `make_svg()` orchestrator, `make_svg_generic()` per-part dispatch
- CLI: first arg = `save_type` ("all" / "none"), second = filter string

### Two demo parts

#### Part 1 — `a4_sheet`  (210 × 297 mm)

Builder `get_a4_sheet()`. Demonstrates every generic shape:

| shape | content | pos (approx) |
|---|---|---|
| `rect` | full A4 background plate | centre [0, 0] |
| `rounded_rectangle` | inset content area (190 × 277 mm, r=5) | centre [0, 0] |
| `circle` | decorative corner disc (r=8) | top-left corner |
| `slot` | horizontal adjustment slot (r=3, w=30) | bottom centre |
| `polygon` | small triangle marker | top-right area |
| `text` | title "A4 Demo Sheet" (size 14) | upper centre |
| `text` | subtitle "oomlout SVG pipeline" (size 7) | below title |
| `text` | small corner label "v1.0" (size 4) | bottom-right |

#### Part 2 — `label_76x50`  (76.2 × 50.4 mm)

Builder `get_label_76x50()`. Demonstrates tight real-world layout:

| shape | content | pos (approx) |
|---|---|---|
| `rounded_rectangle` | full label outline (r=3) | centre [0, 0] |
| `rect` | solid header bar (76.2 × 12 mm) | top of label |
| `circle` | small bullet mark (r=2) | left of body text |
| `text` | title "OOMLOUT" (size 9, bold) | in header, white |
| `text` | part name line (size 5) | body row 1 |
| `text` | description line (size 4) | body row 2 |
| `text` | part number / footer (size 3) | bottom strip |

Note: header bar is `negative` type, text over it rendered `positive` in white colour via `color=` kwarg — painter's algorithm keeps it visible.

### CLI

```
python working_svg.py             # generate both parts → svg_parts/
python working_svg.py none        # dry run
python working_svg.py all label   # only label part
```

Output:
```
svg_parts/a4_sheet/a4_sheet.svg
svg_parts/label_76x50/label_76x50.svg
```

---

## Implementation order

1. **Archive** — copy `opsvg.py` → `reference/old/opsvg.py`, `working_svg.py` → `reference/old/working_svg.py`.
2. **Components** — create all 9 `svg_components/<name>/working.py` files.
3. **Rewrite `opsvg.py`** — copy constants/helpers verbatim, add `_discover_components` + `svg_easy`/`se`, keep all render/bbox/helpers unchanged.
4. **Rewrite `working_svg.py`** — new file using `se()`, with `get_a4_sheet` and `get_label_76x50`.
5. **Run** — `python working_svg.py` to verify both SVGs generate without errors.
6. **Update `CLAUDE.md`** — document `svg_components/`, `se()`, and the two demo parts.

---

## Files touched

| file | change |
|---|---|
| `reference/old/opsvg.py` | NEW (copy of original `opsvg.py`) |
| `reference/old/working_svg.py` | NEW (copy of original `working_svg.py`) |
| `opsvg.py` | REWRITE — add discovery + `svg_easy`/`se`, keep public API |
| `working_svg.py` | REWRITE — `se()`-based builders, A4 + label demos |
| `svg_components/rect/working.py` | NEW |
| `svg_components/circle/working.py` | NEW |
| `svg_components/slot/working.py` | NEW |
| `svg_components/rounded_rectangle/working.py` | NEW |
| `svg_components/polygon/working.py` | NEW |
| `svg_components/text/working.py` | NEW |
| `svg_components/oobb_plate/working.py` | NEW |
| `svg_components/oobb_holes/working.py` | NEW |
| `svg_components/oobb_circle/working.py` | NEW |
| `CLAUDE.md` | UPDATE |
