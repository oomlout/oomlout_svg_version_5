# Plan: Full scad_help parity + working_scad style match

## Status Legend
- `[ ]` not started  `[~]` in progress  `[x]` complete  `[!]` blocked

## Overall Progress
`[x]` Phase 0 — Archive current svg_help.py + working_svg.py  
`[x]` Phase 1 — svg_help.py: add all missing scad_help functions  
`[x]` Phase 2 — Rewrite working_svg.py to match working_scad.py style  
`[x]` Phase 3 — Verify  

---

## Resumption checklist
1. Check which phases are `[x]`.
2. Continue from first `[ ]` or `[~]`.
3. Final check: `python working_svg.py` → parts written; navigation folder created.

---

## Phase 0 — Archive
- `[x]` 0.1 Copy `svg_help.py`    → `reference/old/svg_help_v1.py`
- `[x]` 0.2 Copy `working_svg.py` → `reference/old/working_svg_v3.py`

---

## Phase 1 — svg_help.py: full scad_help parity

### Functions to ADD (currently missing)

**`get_typ(**kwargs)`** — exact mirror of scad_help.get_typ  
Returns "all" | "fast" | "manual". Default = "fast".

**`get_build_variables(typ, filter="")`** — exact mirror  
Returns dict with filter / save_type / navigation / overwrite / output_formats.  
- all  → save_type="all",  navigation=True,  output_formats=[]  
- fast → save_type="none", navigation=False, output_formats=[]  
- manual → save_type="none", navigation=True, output_formats=[] (tweak inline)

**`get_navigation_sort(oobb_style=False)`** — exact mirror  
Returns sort list. Default: ["oobb_name", "width", "height"].

**`prepare_base_for_print(thing, pos, **kwargs)`** — stub  
In SCAD this flips a part for FDM printing. SVG is 2-D, so this is a no-op  
with a comment explaining why.

**`generate_navigation(folder="parts", sort=[...])`** — exact mirror  
Crawls `folder/*/working.yaml`, copies each folder into  
`navigation_svg/<sort_key_1>_<val>/<sort_key_2>_<val>/…`  
(mirrors scad_help.generate_navigation exactly, nav folder = "navigation_svg").

### Functions to UPDATE

**`make_svg_generic(part)`**  
- Change signature to match scad_help: kwargs come from `part["kwargs"]`,  
  NOT separate function params.  
- Add oomp_mode handling (project / oobb) — mirrors scad_help exactly.  
- Write `svg_details` dict into working.yaml so get_parts() can reload it.  
  `svg_details` = the minimal kwargs needed to rebuild (oobb_name + builder kwargs).

**`make_parts(**kwargs)`**  
- Add `navigation` support: if `kwargs["navigation"]` is True, call generate_navigation.  
- Keep `if True:` outer wrapper to match scad_help style.

### svg_details format written to working.yaml

```yaml
svg_details:
  oobb_name: a4_sheet
  depth: 3
  # any other kwargs the builder needs
```

This is the SVG equivalent of `oobb_details` in the SCAD pipeline.

### Tasks
- `[x]` 1.1 Add `get_typ()`
- `[x]` 1.2 Add `get_build_variables()`
- `[x]` 1.3 Add `get_navigation_sort()`
- `[x]` 1.4 Add `prepare_base_for_print()` stub
- `[x]` 1.5 Add `generate_navigation()`
- `[x]` 1.6 Update `make_svg_generic()` — new signature + svg_details write + oomp_mode
- `[x]` 1.7 Update `make_parts()` — navigation handled in working_svg.py (mirrors scad)

---

## Phase 2 — Rewrite working_svg.py to match working_scad.py

### Style rules (copy exactly from working_scad.py)

| working_scad.py pattern | working_svg.py equivalent |
|---|---|
| `import copy` / `import oobb` / `import yaml` / `import scad_help` | `import copy` / `import opsvg` / `import yaml` / `import svg_help` |
| No module docstring | No module docstring |
| `def main(**kwargs): make_scad(**kwargs)` | `def main(**kwargs): make_svg(**kwargs)` |
| `make_scad()` calls `scad_help.get_typ()` → `get_build_variables()` → `make_parts()` | Same with `svg_help.*` |
| `get_parts(kwargs, oomp_mode)` loads from `parts/*/working.yaml` via `oobb_details` | Same, loads via `svg_details` |
| `if True:` wraps every shape block | Same |
| `f"oobb_plate"` (f-string on a literal) | `f"rect"`, `f"text"` etc |
| `#p3["m"] = "#"` commented debug lines | keep equivalent commented lines |
| `#add plate` / `#add holes seperate` comments | `#add background` / `#add title text` etc |
| `pos1 = copy.deepcopy(pos)` then `p3["pos"] = pos1` | Same |
| `prepare_print = kwargs.get("prepare_print", False)` extracted but possibly unused | Same |
| `if prepare_print: scad_help.prepare_base_for_print(…)` at end of builders | Same |
| `if __name__ == '__main__': kwargs = {}; main(**kwargs)` | Same |

### Builder functions style  
Each builder opens by extracting ALL standard variables:
```python
def get_a4_sheet(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    rot = kwargs.get("rot", [0,0,0])
    pos = kwargs.get("pos", [0,0,0])
    extra = kwargs.get("extra", "")

    #add background
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"rect"
        ...
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        opsvg.se(thing, **p3)
```

### `get_parts(kwargs, oomp_mode)` — exact structural mirror of working_scad

```python
def get_parts(kwargs, oomp_mode):
    parts = []

    parts_directory = os.path.join(os.path.dirname(__file__), "parts")
    if not os.path.isdir(parts_directory):
        return parts

    for folder in os.listdir(parts_directory):
        ...
        svg_details = loaded_part.get("svg_details")
        if not isinstance(svg_details, dict):
            continue
        part = loaded_part
        part_kwargs = copy.deepcopy(kwargs)
        part_kwargs.update(copy.deepcopy(loaded_part.get("kwargs", {})))
        part_kwargs.update(copy.deepcopy(svg_details))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = part.get("oobb_name", svg_details.get("oobb_name","default"))
        parts.append(part)

    return parts
```

### Tasks
- `[x]` 2.1 Write imports + main() + make_svg() (exact working_scad mirror)
- `[x]` 2.2 Write get_parts() loading from parts/*/working.yaml via svg_details
- `[x]` 2.3 Write get_base() / get_default_part() in if True: style
- `[x]` 2.4 Write get_a4_sheet() in if True: style
- `[x]` 2.5 Write get_label_76x50() in if True: style
- `[x]` 2.6 Write __main__ block: `kwargs = {}; main(**kwargs)`

---

## Phase 3 — Verify

- `[x]` 3.1 `python working_svg.py` (typ="fast") → dry-run only (save_type="none")
- `[x]` 3.2 Edit typ to "all", run → both parts written to parts/
- `[x]` 3.3 Run again → loads from parts/*/working.yaml via svg_details ✓
- `[x]` 3.4 navigation=True run → navigation_svg/ folder created
- `[x]` 3.5 `python working_svg.py` with navigation → navigation_svg/ populated

---

## Files touched

| file | change | status |
|---|---|---|
| `reference/old/svg_help_v1.py` | archive | `[x]` |
| `reference/old/working_svg_v3.py` | archive | `[x]` |
| `svg_help.py` | REWRITE — full scad_help parity | `[x]` |
| `working_svg.py` | REWRITE — working_scad style | `[x]` |
| `parts/svg_demo_a4_a4_sheet/working.yaml` | seed file — bootstraps first run | `[x]` |
| `parts/svg_label_76x50_label_76x50/working.yaml` | seed file — bootstraps first run | `[x]` |
