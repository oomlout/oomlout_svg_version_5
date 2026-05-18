# Plan: SVG Stylesheet System

## Status Legend
- `[ ]` not started  `[~]` in progress  `[x]` complete  `[!]` blocked

## Overall Progress
`[x]` Phase 1 — `svg_styles.py` (core module)  
`[x]` Phase 2 — Integration into `opsvg.se()` and `thing` dict  
`[x]` Phase 3 — Per-part override API  
`[x]` Phase 4 — `working.yaml` style overrides  
`[x]` Phase 5 — Demo parts refactored to use styles  
`[x]` Phase 6 — Tests  
`[x]` Phase 7 — Verify end-to-end  

---

## Resumption checklist
1. Check which phases are `[x]`.
2. Continue from first `[ ]` or `[~]`.
3. Final check: `python -m pytest tests/ -v` passes; demo parts render correctly.

---

## Design rationale

The system is modelled on CSS — named styles live in a stylesheet dict, parts can
override them, and inline kwargs always win.  Three layers of specificity:

```
inline kwarg  >  part-level style override  >  default stylesheet
```

Dot notation lets variants inherit from a base style with minimal duplication:

```python
"plate"        → full property dict (the base)
"plate.accent" → only the properties that differ from "plate"
resolve("plate.accent") merges base + variant before returning
```

No new DSL, no config files needed — plain Python dicts throughout.
File-based sheets in `styles/*.yaml` shadow built-ins of the same name.
An array of stylesheet names is accepted; sheets merge left-to-right (last wins).

---

## Phase 1 — `svg_styles.py`  `[x]`

**File:** `svg_styles.py` (project root)

Built-in stylesheets: `default`, `jazzy`  
File-based stylesheets (in `styles/`): `blueprint`, `high_contrast`, `neon`, `pastel`, `minimal`

### Public API

**`default_styles() → dict`** — returns copy of DEFAULT_STYLES  
**`get_stylesheet(name_or_names, styles_dir=None) → dict`** — str or list; list merges left-to-right  
**`list_available_stylesheets(styles_dir=None) → list[dict]`** — all sheets, file-first  
**`resolve(style_name, stylesheet) → dict`** — dot notation, returns copy  
**`merge(base, overrides) → dict`** — style-name-level shallow merge  
**`set_style(thing, name, props)`** — in-place override on thing["styles"]  
**`apply(style_name, stylesheet, **inline_kwargs) → dict`** — resolved + overrides  

### Tasks
- `[x]` 1.1 Write `svg_styles.py` with `DEFAULT_STYLES` and all functions
- `[x]` 1.2 Smoke-test passes
- `[x]` 1.3 Dot-notation resolves correctly for known + unknown names

---

## Phase 2 — Integration into `opsvg.se()` and `thing` dict  `[x]`

### Tasks
- `[x]` 2.1 `svg_help.py`: seed `thing["styles"]` in `get_default_thing()`; accept `stylesheet=` kwarg
- `[x]` 2.2 `opsvg.py`: import svg_styles
- `[x]` 2.3 Style resolution block in `svg_easy()` — `style=` kwarg stripped, resolved via `setdefault`
- `[x]` 2.4 Existing tests still pass

---

## Phase 3 — Per-part style override API  `[x]`

### Tasks
- `[x]` 3.1 `working_svg.py`: import svg_styles
- `[x]` 3.2 `make_svg_generic()`: merge `part_styles` from kwargs
- `[x]` 3.3 Pattern documented in working_svg.py comments

---

## Phase 4 — `working.yaml` style overrides  `[x]`

### Tasks
- `[x]` 4.1 `working_svg.get_parts()`: extract `svg_details["styles"]` → `kwargs["part_styles"]`
- `[x]` 4.2 `svg_details["stylesheet"]` also extracted (single or list of sheet names)

---

## Phase 5 — Demo parts refactored to use styles  `[x]`

### Tasks
- `[x]` 5.1 `get_a4_sheet()` uses named styles
- `[x]` 5.2 `get_label_76x50()` uses named styles
- `[x]` 5.3 Parts render correctly
- `[x]` 5.4 Samples regenerated
- `[x]` 5.5 Documentation regenerated

---

## Phase 6 — Tests  `[x]`

**File:** `tests/test_svg_styles.py` — 120 tests across 9 test classes, all passing.

Classes: `TestDefaultStyles`, `TestGetStylesheet`, `TestResolve`, `TestMerge`,
`TestSetStyle`, `TestApply`, `TestSeStyleIntegration`, `TestGetStylesheetArray`,
`TestYamlStyleFiles`, `TestListAvailableStylesheets`, `TestGetDefaultThingStyles`

### Tasks
- `[x]` 6.1 Write `tests/test_svg_styles.py`
- `[x]` 6.2 `python -m pytest tests/test_svg_styles.py -v` → all pass
- `[x]` 6.3 Full suite `python -m pytest tests/ -v` → 120/120 pass

---

## Phase 7 — Verify end-to-end  `[x]`

### Tasks
- `[x]` 7.1 `python working_svg.py` → parts write to `parts/`
- `[x]` 7.2 SVG renders correctly
- `[x]` 7.3 YAML `styles:` override passes `part_styles` correctly
- `[x]` 7.4 `python -m pytest tests/ -v` → 120/120 pass
- `[x]` 7.5 Snapshots remain valid (no render-output changes)
- `[x]` 7.6 `CLAUDE.md` updated with new files and usage pattern

---

## New files

| file | purpose | status |
|---|---|---|
| `svg_styles.py` | stylesheet module: built-ins + YAML loader, resolve/merge/apply API | `[x]` |
| `styles/blueprint.yaml` | Navy + cyan + gold blueprint theme | `[x]` |
| `styles/high_contrast.yaml` | Black/white, thick outlines | `[x]` |
| `styles/neon.yaml` | Dark synthwave, neon green/magenta/cyan | `[x]` |
| `styles/pastel.yaml` | Soft blush/mint/periwinkle palette | `[x]` |
| `styles/minimal.yaml` | Ultra-clean near-white, hairline borders | `[x]` |
| `tests/test_svg_styles.py` | unit + integration tests for the style system | `[x]` |
| `regenerate_docs.bat` | one-click doc regeneration (samples + HTML + JSON) | `[x]` |

## Modified files

| file | change | status |
|---|---|---|
| `svg_help.py` | seed `thing["styles"]`; accept `stylesheet=` + `part_styles=` kwargs | `[x]` |
| `opsvg.py` | resolve `style=` kwarg in `svg_easy()`; per-shape stroke in render loop | `[x]` |
| `working_svg.py` | refactor demo builders to use named styles; extract yaml styles in `get_parts()` | `[x]` |
| `svg_documentation.py` | `get_all_stylesheets_documentation()` uses `list_available_stylesheets()` | `[x]` |
| `templates/svg_documentation_template.html` | Stylesheets section with tabs + swatches | `[x]` |
| All 9 `svg_components/*/working.py` | `color`, `stroke`, `stroke_width` (+ `rot`) in `define()` + `action()` | `[x]` |

---

## Usage quick-reference

```python
import opsvg
import svg_styles

# In any builder function:
def get_my_part(thing, **kwargs):
    color = kwargs.get("color", "#333333")

    # 1. Override styles for this part (optional)
    svg_styles.set_style(thing, "plate", {"color": color})

    # 2. Use named styles — inline kwargs still override
    opsvg.se(thing, shape="oobb_plate",  style="plate",        width=2, height=2, pos=pos)
    opsvg.se(thing, shape="oobb_holes",  style="hole",         width=2, height=2, pos=pos)
    opsvg.se(thing, shape="text",        style="header.label", text="My Part",    pos=pos)
    opsvg.se(thing, shape="text",        style="label.small",  text="v1.0",
             halign="right",  # ← inline override beats style
             pos=[10, -5, 0])
```

```yaml
# working.yaml style override (no Python needed)
svg_details:
  svg_name: my_part
  stylesheet: blueprint          # single name
  # stylesheet: [default, neon]  # or a list — merges left-to-right
  styles:
    plate:
      color: "#E85D04"
    label:
      font: "JetBrains Mono, monospace"
```
