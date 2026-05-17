# Plan: Standalone SVG Pipeline (no oobb dependency)

## Status Legend
- `[ ]` not started
- `[~]` in progress
- `[x]` complete
- `[!]` blocked / needs attention

## Overall Progress
`[x]` Phase 0 — Archive current opsvg.py + working_svg.py  
`[x]` Phase 1 — svg_variables.py (standalone constants, replaces oobb.gv)  
`[x]` Phase 2 — Rewrite opsvg.py (import svg_variables, no oobb at all)  
`[x]` Phase 3 — svg_help.py (orchestrator, mirrors scad_help.py)  
`[x]` Phase 4 — Rewrite working_svg.py (uses svg_help, parts/ output, png/pdf)  
`[x]` Phase 5 — Verify + update CLAUDE.md  

---

## Resumption checklist

If this session is interrupted, start here:

1. Check which phase boxes are `[x]`.
2. Find first `[ ]` or `[~]` task and continue from there.
3. Final check: `python working_svg.py` → both parts written to `parts/`.
4. Final check: `python working_svg.py all a4 png pdf` → PNG + PDF also written.

---

## Phase 0 — Archive current files

Current `opsvg.py` and `working_svg.py` still contain `try: import oobb` blocks.
Archive them before rewriting.

- `[ ]` 0.1 — Copy `opsvg.py` → `reference/old/opsvg_v2.py`
- `[ ]` 0.2 — Copy `working_svg.py` → `reference/old/working_svg_v2.py`

---

## Phase 1 — svg_variables.py

**Goal:** a completely self-contained variable store. No imports outside stdlib.
Analogous to `oobb_variables.py` but SVG / laser-only (no 3dpr / true modes).

### Variables to define

```python
# Grid
OSP       = 15.0    # OOBB standard pitch mm
OSP_MINUS = 1.0     # body shrink per side
OSP_HOLE  = "m6"    # default hole size name
OSPE      = 7.5     # half-pitch
OSPE_MINUS = 0.5

# Hole radii for laser cutting (mm radius, not diameter)
# Key = shorthand name used in radius_name kwarg
HOLE_RADII = {
    "md5":  0.25,
    "m1":   0.5,
    "m1_5": 0.8,
    "m2":   1.0,
    "m2_5": 1.25,
    "m3":   1.5,
    "m3_5": 1.75,
    "m4":   2.0,
    "m5":   2.5,
    "m6":   3.0,
    "m7":   3.5,
    "m8":   4.0,
    "m10":  5.0,
    "m12":  6.0,
}

# Visual defaults
FILL_POSITIVE = "#333333"
FILL_NEGATIVE = "#ffffff"
STROKE        = "none"
STROKE_WIDTH  = 0
PADDING_MM    = 5
CORNER_RADIUS = 2.0
```

### Public API

```python
def gv(name):
    """Get a variable by name. Raises KeyError if not found."""

def hole_radius(name):
    """
    Return laser hole radius in mm for the given shorthand name.
    Tries bare name, then strips _laser/_true/_3dpr suffix.
    """

def hole_pos(xi, yi, w, h):
    """
    Return (x_mm, y_mm) of hole grid position xi,yi in a w×h plate.
    Origin is at plate centre. Mirrors oobb.get_hole_pos().
    """
```

### Tasks
- `[ ]` 1.1 — Write `svg_variables.py` with all constants and three public functions

---

## Phase 2 — Rewrite opsvg.py

**Goal:** remove every `import oobb` (and its try/except fallback).
Use `svg_variables` instead. Public API stays identical.

### Changes from current version

| location | old | new |
|---|---|---|
| top of file | `try: import oobb as _oobb … except: _OSP=15` | `import svg_variables as _sv` |
| `_gv(name)` | oobb.gv with _laser fallback | `_sv.gv(name)` / `_sv.hole_radius(name)` |
| `_hole_pos(xi,yi,w,h)` | `_oobb.get_hole_pos(…)` | `_sv.hole_pos(xi,yi,w,h)` |
| constants `_OSP` etc. | derived from oobb | `_sv.OSP` etc. |
| `_discover_components` | unchanged | unchanged |
| everything else | unchanged | unchanged |

### Tasks
- `[ ]` 2.1 — Replace oobb import block with `import svg_variables as _sv`
- `[ ]` 2.2 — Rewrite `_gv()` to use `_sv.gv()` / `_sv.hole_radius()`
- `[ ]` 2.3 — Rewrite `_hole_pos()` to use `_sv.hole_pos()`
- `[ ]` 2.4 — Replace `_OSP`, `_OSP_MINUS` refs with `_sv.OSP`, `_sv.OSP_MINUS`
- `[ ]` 2.5 — Smoke test: `python -c "import opsvg; print(opsvg._COMPONENT_MAP.keys())"`
             Expected: 14 keys, no import errors

---

## Phase 3 — svg_help.py

**Goal:** orchestrator analogous to `scad_help.py`. Owns the parts/ folder
lifecycle — thing dict creation, builder dispatch, file writing, PNG/PDF export.

### File: svg_help.py

#### `get_default_thing(**kwargs)` — mirrors `oobb.get_default_thing()`

Builds the base thing dict. No oobb dependency.

```python
thing = {
    # identification
    "id":              <built from classification+type+size+…>,
    "oobb_name":       kwargs.get("oobb_name", ""),
    "type":            kwargs.get("type", ""),
    "description":     kwargs.get("description", ""),
    "classification":  kwargs.get("classification", "svg"),
    "size":            kwargs.get("size", ""),
    "color":           kwargs.get("color", ""),
    "description_main": kwargs.get("description_main", ""),
    "description_extra": kwargs.get("description_extra", ""),

    # geometry
    "width":    kwargs.get("width",  1),
    "height":   kwargs.get("height", 1),
    "depth":    kwargs.get("depth",  3),
    "extra":    kwargs.get("extra",  ""),

    # SVG components list (populated by builder)
    "svg_components": [],
}
```

#### `make_svg_generic(part, save_type="all", overwrite=True)` — mirrors `scad_help.make_scad_generic()`

Full pipeline for one part:

1. Extract `oobb_name`, `project_name`, `kwargs` from part dict
2. Build `thing` via `get_default_thing(**kwargs)`
3. Dispatch to `working_svg.get_<oobb_name>(thing, **kwargs)`
4. Build `folder = parts/<id>/` and create it
5. If `save_type == "all"`:
   - Write `parts/<id>/working.svg`
   - Write `parts/<id>/working.yaml` (kwargs only — for re-running)
   - Write `parts/<id>/thing.yaml` (full thing dict)
   - If `png` in output_formats: write `parts/<id>/working.png`
   - If `pdf` in output_formats: write `parts/<id>/working.pdf`
6. Return `thing`

#### `make_parts(**kwargs)` — mirrors `scad_help.make_parts()`

```python
def make_parts(**kwargs):
    parts      = kwargs.get("parts", [])
    filter_str = kwargs.get("filter", "")
    save_type  = kwargs.get("save_type", "all")
    overwrite  = kwargs.get("overwrite", True)
    output_formats = kwargs.get("output_formats", [])   # e.g. ["png", "pdf"]

    for part in parts:
        oobb_name = part.get("oobb_name", "default")
        extra     = part.get("kwargs", {}).get("extra", "")
        if filter_str and filter_str not in oobb_name and filter_str not in extra:
            print(f"skipping  {oobb_name}")
            continue
        print(f"making    {oobb_name}")
        make_svg_generic(part, save_type=save_type, overwrite=overwrite,
                         output_formats=output_formats)
```

#### PNG/PDF export

```python
def svg_to_png(svg_path, png_path, dpi=96):
    """
    Convert SVG → PNG.
    Uses cairosvg if available, otherwise falls back to
    Inkscape CLI (inkscape --export-png) or prints a warning.
    """

def svg_to_pdf(svg_path, pdf_path):
    """
    Convert SVG → PDF.
    Uses cairosvg if available, otherwise falls back to
    Inkscape CLI (inkscape --export-pdf) or prints a warning.
    """
```

Priority order for converters:
1. `cairosvg` (pure Python, `pip install cairosvg`)
2. `inkscape` CLI (`inkscape --export-type=png …`)
3. Warning + skip (never hard-fail)

#### `id_from_part(part)` — build the folder-safe ID

Mirrors the oomp_id construction logic in `scad_help.make_scad_generic()`:

```python
def id_from_part(part):
    """
    Build a filesystem-safe ID string from part metadata fields.
    Falls back to oobb_name + kwargs hash if metadata is sparse.
    """
    oomp_keys = ["classification", "type", "size",
                 "color", "description_main", "description_extra"]
    oomp_id = part.get("id", "")
    if not oomp_id:
        for key in oomp_keys:
            val = str(part.get(key, "")).replace(".", "_")
            if val:
                oomp_id += f"{val}_"
        oomp_id = oomp_id.rstrip("_")
    if not oomp_id:
        # final fallback
        oomp_id = part.get("oobb_name", "unnamed")
    return oomp_id
```

### Tasks
- `[ ]` 3.1 — Write `get_default_thing(**kwargs)`
- `[ ]` 3.2 — Write `id_from_part(part)`
- `[ ]` 3.3 — Write `svg_to_png()` and `svg_to_pdf()` with cairosvg + inkscape fallbacks
- `[ ]` 3.4 — Write `make_svg_generic()` (full pipeline, file writing)
- `[ ]` 3.5 — Write `make_parts()` orchestrator
- `[ ]` 3.6 — Smoke test: `python -c "import svg_help; print('ok')"`

---

## Phase 4 — Rewrite working_svg.py

**Goal:** mirror `working_scad.py` exactly in structure and style.
- Uses `svg_help.make_parts()` instead of the inline orchestrator
- Parts written to `parts/<id>/` not `svg_parts/<name>/`
- PNG / PDF requested via CLI args
- Human-readable descriptive variable names throughout
- Builder functions unchanged in logic, but use `se()` via opsvg

### working_svg.py structure

```
module docstring  (matches working_scad.py docstring style)
imports: copy, sys, opsvg, svg_help

main(**kwargs)
make_svg(**kwargs)         ← calls svg_help.make_parts()
get_parts() → list[dict]   ← part registry

# builders
get_default_part(thing, **kwargs)
get_a4_sheet(thing, **kwargs)
get_label_76x50(thing, **kwargs)
```

### Part descriptor format (mirrors working_scad.py exactly)

```python
parts.append({
    "oobb_name":        "a4_sheet",
    "project_name":     "svg_demo",
    "classification":   "svg",
    "type":             "demo",
    "size":             "a4",
    "color":            "",
    "description_main": "a4_sheet",
    "description_extra": "",
    "kwargs": {
        "width":     1,
        "height":    1,
        "depth":     3,
        "save_type": "all",
        "overwrite": True,
        "modes":     ["svg"],
    },
})
```

### CLI (mirrors working_scad.py)

```
python working_svg.py                      # generate all → parts/
python working_svg.py none                 # dry run
python working_svg.py all label            # filter by name
python working_svg.py all label png        # + export PNG
python working_svg.py all label png pdf    # + export PNG and PDF
```

Parsing: `sys.argv[1]` = save_type, `sys.argv[2]` = filter, `sys.argv[3:]` = output_formats

### Tasks
- `[ ]` 4.1 — Write module docstring and imports
- `[ ]` 4.2 — Write `main()`, `make_svg()` wired to `svg_help.make_parts()`
- `[ ]` 4.3 — Write `get_parts()` with A4 and label descriptors (full oomp metadata fields)
- `[ ]` 4.4 — Write `get_default_part()` (fallback builder)
- `[ ]` 4.5 — Write `get_a4_sheet()` (unchanged logic, uses `se()`)
- `[ ]` 4.6 — Write `get_label_76x50()` (unchanged logic, uses `se()`)
- `[ ]` 4.7 — Write `__main__` CLI block with save_type / filter / output_formats args

---

## Phase 5 — Verify + update CLAUDE.md

### Verification steps

- `[ ]` 5.1 — `python -c "import opsvg"` — no import errors, no oobb warnings
- `[ ]` 5.2 — `python working_svg.py none` — dry run, prints making/skipping, no files
- `[ ]` 5.3 — `python working_svg.py` — both parts written to `parts/<id>/`
              Check: `parts/*/working.svg`, `parts/*/working.yaml`, `parts/*/thing.yaml` exist
- `[ ]` 5.4 — `python working_svg.py all a4 png` — PNG also written (or graceful warning)
- `[ ]` 5.5 — `python working_svg.py all a4 png pdf` — PDF also written (or graceful warning)
- `[ ]` 5.6 — Confirm `svg_parts/` (old output) is NOT written (parts/ only)
- `[ ]` 5.7 — Update CLAUDE.md: new files, parts/ folder, PNG/PDF CLI flags

---

## New files

| file | change | status |
|---|---|---|
| `reference/old/opsvg_v2.py` | COPY of current `opsvg.py` | `[x]` |
| `reference/old/working_svg_v2.py` | COPY of current `working_svg.py` | `[x]` |
| `svg_variables.py` | NEW — standalone constants + gv/hole_radius/hole_pos | `[x]` |
| `svg_help.py` | NEW — orchestrator (get_default_thing, make_parts, png/pdf export) | `[x]` |
| `opsvg.py` | REWRITE — use svg_variables, no oobb | `[x]` |
| `working_svg.py` | REWRITE — use svg_help, parts/ output, CLI png/pdf flags | `[x]` |
| `CLAUDE.md` | UPDATE | `[x]` |

---

## Dependency notes

- `cairosvg` is optional. Install with `pip install cairosvg`.
  If absent, PNG/PDF export falls back to Inkscape CLI, then skips with a warning.
- `inkscape` is optional. If absent and cairosvg also absent, export is skipped.
- `pyyaml` is required for working.yaml / thing.yaml output.
  Install with `pip install pyyaml`.
- No other new dependencies. `opsvg.py` and `svg_help.py` use only stdlib otherwise.
