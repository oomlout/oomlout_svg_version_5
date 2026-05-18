# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A fully standalone SVG rendering pipeline for OOBB (Object Oriented Building Blocks) laser-cut flat parts. It mirrors the architecture of the upstream `working_scad.py` / `scad_help.py` / `opsc.py` pipeline but outputs SVG with **zero dependency on the `oobb` package**.

| File | Role | Analogue |
|---|---|---|
| `svg_variables.py` | All constants + `gv()` / `hole_radius()` / `hole_pos()` | `oobb_variables.py` + `oobb.gv()` |
| `opsvg.py` | SVG renderer + component discovery + `se()` dispatcher | `opsc.py` |
| `svg_help.py` | Pipeline orchestrator: thing dict, parts/ output | `scad_help.py` |
| `working_svg.py` | Part definitions + builder functions | `working_scad.py` |
| `svg_styles.py` | Stylesheet system — named styles, dot-notation variants, YAML file loading | — |
| `svg_components/*/working.py` | Self-contained shape components | `components/*/working.py` |
| `svg_documentation.py` | Documentation generator (JSON + HTML) | `components/documentation.py` |
| `generate_samples.py` | Renders default sample SVG per component | — |
| `regenerate_docs.bat` | One-click: regenerate samples + documentation | — |

## Running Parts Generation

```bash
python working_svg.py          # all parts → parts/  (typ="fast" by default in svg_help.get_typ)
```

Toggle `typ` in `svg_help.get_typ()` to switch modes:
- `"fast"` — writes SVG only, no navigation
- `"all"`  — writes SVG + navigation folder
- `"manual"` — dry-run + navigation (tweak inline)

Parts are loaded from `parts/*/working.yaml` (any file with an `svg_details` section).
On first use, seed `working.yaml` files must exist in `parts/<id>/`.

## Documentation

```bash
python generate_samples.py              # render sample.svg for every component (9 files)
python generate_samples.py rect         # single component
python generate_samples.py --force      # overwrite existing samples

python svg_documentation.py             # generate documentation.html + documentation_data.json
python svg_documentation.py --json-only # JSON only
python svg_documentation.py --out docs/ # custom output folder
```

Open `documentation.html` in a browser — component cards with inline SVG previews,
search + category filter, click-to-expand detail drawer, and a Stylesheets section
showing swatches for every built-in and file-based stylesheet.

One-click regeneration (Windows):
```
regenerate_docs.bat        # runs generate_samples.py --force then svg_documentation.py
```

## Tests

```bash
python -m pytest tests/ -v
UPDATE_SNAPSHOTS=1 python -m pytest tests/test_svg_rendering.py -v   # regenerate hash snapshots
```

Four test files:
- `tests/test_svg_components.py` — component contract (define/action interface, 9+ components)
- `tests/test_documentation.py`  — doc generation (JSON/HTML export, key validation)
- `tests/test_svg_rendering.py`  — SVG validity + snapshot regression
- `tests/test_svg_styles.py`     — stylesheet system (120 tests: resolve, merge, apply, YAML loading, se() integration)

## Output structure

Each part writes to `parts/<id>/`:

```
parts/svg_demo_a4_a4_sheet/
  working.svg     ← SVG output
  working.yaml    ← part metadata + svg_details (reload source)
  thing.yaml      ← full thing dict archive
```

The folder name is built from the part descriptor's metadata fields:
`classification_type_size_color_description_main_description_extra`

## Architecture

### Data flow

1. `working_svg.py:get_parts()` — loads `parts/*/working.yaml` (svg_details required).
2. `svg_help.make_parts()` — filters + iterates; calls `make_svg_generic()` per part.
3. `svg_help.make_svg_generic()` — builds `thing` dict, dispatches to `get_<svg_name>()`.
4. Builder calls `opsvg.se(thing, **p3)` — accumulates shape descriptors.
5. `opsvg.opsvg_make_object()` — renders SVG; `svg_help` writes YAML.

### The `p3` pattern

```python
p3          = copy.deepcopy(kwargs)
p3["shape"] = f"oobb_plate"    # see shape vocabulary below
p3["style"] = "plate"          # named style (optional; inline color still wins)
p3["pos"]   = copy.deepcopy(pos)
opsvg.se(thing, **p3)          # high-level dispatcher (preferred)
```

No positive/negative type — shapes render in append order, each using its `color` kwarg
(or resolved from `style=`) as fill.  `stroke` and `stroke_width` are also supported
per-shape.

### Stylesheet system

**Built-in sheets:** `default` (technical monochrome, burnt-orange accent), `jazzy` (vivid purple/coral)  
**File-based sheets** (in `styles/`): `blueprint`, `high_contrast`, `neon`, `pastel`, `minimal`

```python
import svg_styles as _ss

# Resolve a named style (dot-notation merges base + variant)
props = _ss.resolve("plate.accent", thing["styles"])

# Merge two stylesheets (last wins per property)
merged = _ss.get_stylesheet(["default", "neon"])

# Override a style for one part
_ss.set_style(thing, "plate", {"color": "#FF6600"})
```

**In `se()` calls** — use `style=` kwarg; inline kwargs always win:
```python
opsvg.se(thing, shape="rect",    style="plate",        ...)
opsvg.se(thing, shape="text",    style="label.small",  halign="left", ...)
opsvg.se(thing, shape="oobb_plate", style="plate",     ...)
```

**In `working.yaml`** — no Python needed:
```yaml
svg_details:
  svg_name: my_part
  stylesheet: blueprint          # single name
  # stylesheet: [default, neon]  # or a list — merges left-to-right
  styles:
    plate:
      color: "#FF6600"
    label:
      font: "JetBrains Mono, monospace"
```

**Adding a custom stylesheet:** drop a `styles/mysheet.yaml` file.  It shadows any
built-in with the same name and is auto-discovered by `list_available_stylesheets()`
and the documentation generator.

### svg_details — the reload key

`svg_details` in `working.yaml` is the only criterion for loading a part from disk:

```yaml
svg_details:
  svg_name: a4_sheet   # selects builder get_a4_sheet()
  depth: 3
```

Any `working.yaml` with an `svg_details` dict is included. Dimension keys (`width`,
`height`, `depth`) are only merged into kwargs if they are numeric.

### Shape vocabulary

| shape | aliases | key params |
|---|---|---|
| `rect` | — | `size=[w,h,_]`, `color` |
| `circle` | `hole` | `r=<mm>`, `color` |
| `slot` | `capsule` | `r=<mm>`, `w=<mm>`, `color` |
| `rounded_rectangle` | `rounded_rect`, `rrect` | `size=[w,h,_]`, `r=<mm>`, `color` |
| `polygon` | — | `points=[[x,y],…]`, `color` |
| `text` | `label` | `text`, `size`, `font`, `halign`, `valign`, `color` |
| `oobb_plate` | — | `width`, `height` (OOBB units), `color` |
| `oobb_holes` | — | `width`, `height`, `radius_name`, `color` |
| `oobb_circle` | — | `diameter` (OOBB units), `color` |

### svg_variables.py public API

```python
sv.OSP                    # 15.0 mm — OOBB pitch
sv.OSP_MINUS              # 1.0 mm — body shrink
sv.gv("osp")              # variable lookup by name
sv.hole_radius("m6")      # 3.0 mm — laser hole radius
sv.hole_pos(xi, yi, w, h) # (x_mm, y_mm) — hole grid position
```

### Coordinate system

Origin at part centre, Y-up. `opsvg.py` auto-flips Y for SVG (Y-down) and
computes the viewBox from the bounding box — canvas size is never set manually.

## Adding a New Part

1. Add a seed `working.yaml` to `parts/<id>/`:
   ```yaml
   oobb_name: my_part
   classification: svg
   svg_details:
     svg_name: my_part
   kwargs:
     depth: 3
   ```
2. Write `get_my_part(thing, **kwargs)` in `working_svg.py`.
3. Run `python working_svg.py` — the part is loaded, built, and written.

## Adding a New Shape Component

1. Create `svg_components/my_shape/working.py` with `describe()`, `define()`, `action()`.
2. `action(**kwargs)` returns a list of dicts, each with `shape` and `pos` (no `type`).
3. Declare aliases in `define()["shape_aliases"]` if needed.
4. No registration step — `opsvg._discover_components()` picks it up at next import.
5. Run `python generate_samples.py my_shape` to create its `sample.svg`.

## Demo Parts

| name | size | what it demonstrates |
|---|---|---|
| `a4_sheet` | 210 × 297 mm | rect, rounded_rectangle, polygon, slot, circle, text ×3 |
| `label_76x50` | 76.2 × 50.4 mm | rounded_rectangle, rect header, circle bullet, text ×4 |

## Dependencies

| package | required | purpose |
|---|---|---|
| `pyyaml` | yes | `working.yaml` / `thing.yaml` output; `styles/*.yaml` loading |

## Reference: Upstream OOBB Project

`reference/oomlout_oobb_version_5/` — upstream project for architectural context.
`reference/old/` — archived originals of `opsvg.py`, `working_svg.py`, `svg_help.py`.
