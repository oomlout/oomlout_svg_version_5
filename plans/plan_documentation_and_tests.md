# Plan: Documentation System + Tests + Sample Generation

## Status Legend
- `[ ]` not started  `[~]` in progress  `[x]` complete  `[!]` blocked

## Overall Progress
`[x]` Phase 0 — Understand oobb reference docs + decide styling direction  
`[x]` Phase 1 — svg_documentation.py (data extraction)  
`[x]` Phase 2 — HTML template (fresh styling)  
`[x]` Phase 3 — Sample SVG generation per component  
`[x]` Phase 4 — Tests  
`[x]` Phase 5 — Verify end-to-end  

---

## Resumption checklist
1. Check which phases are `[x]`.
2. Continue from first `[ ]` or `[~]`.
3. Final check: `python -m pytest tests/ -v` passes; `documentation.html` opens in browser.

---

## Phase 0 — Reference study + styling decision
**Already done during planning.** Notes captured here.

### What oobb_version_5 has
| file | role |
|---|---|
| `components/documentation.py` | crawls `components/*/working.py`, calls `define()`, builds JSON |
| `templates/oobb_documentation_template.html` | pastel rainbow gradient, glassmorphism cards, modal detail view, search + category filter |
| `components/documentation_data.json` | generated data blob injected into HTML |
| `components/documentation.html` | final output (template + injected data) |
| `tests/test_documentation_generation.py` | unit tests for doc generation functions |
| `tests/snapshots/` | JSON snapshots for regression |

### Styling direction — NOT pastel rainbow
oobb uses: animated gradient background, glassmorphism, Inter/Poppins fonts, pastel palette.

SVG docs will use a **technical monochrome** aesthetic:
- White background, `#111` text, `#F4F4F4` surface
- Single accent: `#E85D04` (burnt orange) — references laser-cut heat
- Monospace font (`JetBrains Mono` / `Fira Code`) for all code/values
- `Inter` for prose
- No animations on body background (CSS transitions only on hover)
- Cards: flat, 1px border, sharp 4px radius — no glass, no blur
- Inline SVG preview embedded directly in each card (no `<img>` tag)
- Click card → expand detail panel (right-hand drawer, not modal)
- No emoji in category labels

### Tasks
- `[x]` 0.1 Read oobb documentation.py + template
- `[x]` 0.2 Read oobb test_documentation_generation.py
- `[x]` 0.3 Decide styling direction (above)

---

## Phase 1 — svg_documentation.py

**File:** `svg_documentation.py` (project root, mirrors `components/documentation.py`)

### Functions

**`get_all_components_documentation(components_root="svg_components")`**  
Crawls `svg_components/*/working.py`, imports each, calls `define()`.  
Returns list of dicts with keys:
```python
{
    "name":         str,   # folder name / shape key
    "name_long":    str,
    "description":  str,
    "category":     str,
    "variables":    list[dict],   # [{name, description, type, default}, ...]
    "shape_aliases": list[str],
    "returns":      str,
    "sample_svg":   str,   # inline SVG string or "" if not yet generated
}
```

**`get_all_parts_documentation(parts_root="parts")`**  
Crawls `parts/*/working.yaml`, loads each.  
Returns list of dicts with keys: `id`, `oobb_name`, `svg_name`, `classification`, `description_main`.

**`export_documentation_json(output_path, components_root="svg_components", parts_root="parts")`**  
Writes `documentation_data.json`:
```json
{
  "generated_date": "2026-05-17",
  "total_components": 9,
  "total_parts": 3,
  "components": [...],
  "parts": [...]
}
```

**`export_documentation_html(template_path, output_path, ...)`**  
Reads template, replaces `<!-- DOCUMENTATION_DATA_PLACEHOLDER -->` with:
```html
<script>window.DOCUMENTATION_DATA = {...};</script>
```
Writes output HTML.

**`_normalise_variables(raw)`** — same defensive normalisation as oobb version.

**`main()`** — CLI entry point:
```
python svg_documentation.py                  # generates documentation.html + documentation_data.json
python svg_documentation.py --json-only      # JSON only
python svg_documentation.py --out docs/      # custom output folder
```

### Tasks
- `[ ]` 1.1 Write `get_all_components_documentation()`
- `[ ]` 1.2 Write `get_all_parts_documentation()`
- `[ ]` 1.3 Write `_normalise_variables()`
- `[ ]` 1.4 Write `export_documentation_json()`
- `[ ]` 1.5 Write `export_documentation_html()`
- `[ ]` 1.6 Write `main()` CLI block
- `[ ]` 1.7 Smoke test: `python svg_documentation.py --json-only` → `documentation_data.json` written

---

## Phase 2 — HTML template

**File:** `templates/svg_documentation_template.html`

### Layout
```
┌─────────────────────────────────────────────────────┐
│  Header bar: "SVG Components"  [search]  [category] │
├──────────────────────┬──────────────────────────────┤
│  Component grid      │  Detail drawer (slide-in)    │
│  (cards, 3 col)      │  - name / aliases            │
│                      │  - description               │
│                      │  - inline SVG preview        │
│                      │  - variable table            │
│                      │  - returns                   │
├──────────────────────┴──────────────────────────────┤
│  Parts catalogue section (collapsible)              │
└─────────────────────────────────────────────────────┘
```

### Card design
- 240×200px, flat white, 1px `#E0E0E0` border, `border-radius: 4px`
- Top 100px: inline SVG preview (centred, scaled to fit)
- Bottom 100px: name (bold, `14px`), category chip (small, accent bg), aliases (mono, muted)
- Hover: `border-color: #E85D04`, `box-shadow: 0 0 0 2px #E85D04`
- Active / selected: left border `4px solid #E85D04`

### Detail drawer
- Fixed right panel, `360px` wide, slides in from right on card click
- Close on `Esc` or clicking outside
- Contains: large SVG preview, full description, variable table (Name / Type / Default / Description), returns text, shape_aliases list

### Colour palette
```css
--accent:      #E85D04;   /* burnt orange */
--accent-dim:  #FDE8D8;   /* accent tint for chips */
--surface:     #FFFFFF;
--surface-alt: #F7F7F7;
--border:      #E0E0E0;
--text:        #111111;
--text-muted:  #666666;
--code-bg:     #F0F0F0;
```

### Typography
- Prose: `Inter`, 14px / 1.5
- Code / values / aliases: `JetBrains Mono`, `Fira Code`, `monospace`
- Headings: `Inter`, weight 700

### Tasks
- `[ ]` 2.1 Write HTML skeleton + CSS variables + layout
- `[ ]` 2.2 Card grid + hover/active states
- `[ ]` 2.3 Detail drawer + variable table
- `[ ]` 2.4 Parts catalogue section (collapsible `<details>`)
- `[ ]` 2.5 Search + category filter JS
- `[ ]` 2.6 Inline SVG injection from `sample_svg` field
- `[ ]` 2.7 `<!-- DOCUMENTATION_DATA_PLACEHOLDER -->` injection point

---

## Phase 3 — Sample SVG generation

**File:** `generate_samples.py`

For each component in `svg_components/`, call `action(**default_kwargs)` using the
defaults declared in `define()["variables"]`, render the result to SVG, save as
`svg_components/<name>/sample.svg`.

### Default kwargs construction
```python
def build_default_kwargs(variables):
    kwargs = {}
    for v in variables:
        if v.get("default") not in ("", None):
            kwargs[v["name"]] = v["default"]
    return kwargs
```

### Per-component rendering
1. Build kwargs from defaults
2. Add standard keys: `pos=[0,0,0]`, `color="#333333"`
3. Call `component.action(**kwargs)` → list of descriptors
4. Pass descriptors to `opsvg.opsvg_get_svg()` → SVG string
5. Write to `svg_components/<name>/sample.svg`

### Integration with svg_documentation.py
`get_all_components_documentation()` reads `sample.svg` if it exists and embeds
the contents in the `sample_svg` field. Generation is a separate step
(not auto-run on every doc build).

### CLI
```
python generate_samples.py             # all components
python generate_samples.py rect        # single component
python generate_samples.py --force     # overwrite existing
```

### Tasks
- `[ ]` 3.1 Write `build_default_kwargs(variables)`
- `[ ]` 3.2 Write `generate_sample(component_name)` — renders + writes SVG
- `[ ]` 3.3 Write `main()` CLI (all / single / --force)
- `[ ]` 3.4 Run: `python generate_samples.py` → 9 sample SVGs written
- `[ ]` 3.5 Verify sample SVGs load correctly in browser

---

## Phase 4 — Tests

**Folder:** `tests/`

### test_svg_components.py
Unit tests for the component contract:
- `test_every_component_has_define()` — all 9 components expose `define()`
- `test_define_returns_required_keys()` — `name`, `name_long`, `description`, `category`, `variables`
- `test_every_component_has_action()` — all 9 expose `action()`
- `test_action_returns_list()` — `action()` returns a list for default kwargs
- `test_action_descriptors_have_shape_and_pos()` — each descriptor has `shape` and `pos`

### test_documentation.py
Mirrors `test_documentation_generation.py` from oobb:
- `test_get_all_components_returns_list()`
- `test_component_doc_has_required_keys()`
- `test_get_all_parts_returns_list()`
- `test_export_json_creates_file()`
- `test_json_has_required_top_level_keys()`
- `test_export_html_creates_file()`
- `test_html_contains_data_script_tag()`

### test_svg_rendering.py
Snapshot / regression tests for SVG output:
- `test_opsvg_get_svg_returns_valid_xml()` — basic well-formedness check
- `test_opsvg_get_svg_contains_viewbox()` — `viewBox` present
- `test_bounding_box_non_empty()` — bbox has positive area
- `test_sample_svgs_match_snapshots()` — compare SVG hash vs `tests/snapshots/svg_samples.json`
  - Run with `UPDATE_SNAPSHOTS=1` to regenerate

### Snapshot file: `tests/snapshots/svg_samples.json`
```json
{
  "rect":                "sha256:...",
  "circle":              "sha256:...",
  "slot":                "sha256:...",
  "rounded_rectangle":   "sha256:...",
  "polygon":             "sha256:...",
  "text":                "sha256:...",
  "oobb_plate":          "sha256:...",
  "oobb_holes":          "sha256:...",
  "oobb_circle":         "sha256:..."
}
```

### tests/__init__.py
Empty — makes `tests/` a package.

### Tasks
- `[ ]` 4.1 Create `tests/__init__.py`
- `[ ]` 4.2 Write `tests/test_svg_components.py`
- `[ ]` 4.3 Write `tests/test_documentation.py`
- `[ ]` 4.4 Write `tests/test_svg_rendering.py` (with UPDATE_SNAPSHOTS support)
- `[ ]` 4.5 Run `python -m pytest tests/ -v` → all pass
- `[ ]` 4.6 Run `UPDATE_SNAPSHOTS=1 python -m pytest tests/test_svg_rendering.py` → snapshots written

---

## Phase 5 — Verify end-to-end

- `[ ]` 5.1 `python generate_samples.py` → 9 × `svg_components/*/sample.svg` created
- `[ ]` 5.2 `python svg_documentation.py` → `documentation.html` + `documentation_data.json` created
- `[ ]` 5.3 Open `documentation.html` in browser → cards visible, SVG previews render, drawer opens
- `[ ]` 5.4 Search filters correctly, category dropdown works
- `[ ]` 5.5 `python -m pytest tests/ -v` → all pass
- `[ ]` 5.6 Update `CLAUDE.md` with new files and `python generate_samples.py` / `python svg_documentation.py` commands

---

## New files

| file | purpose | status |
|---|---|---|
| `svg_documentation.py` | data extraction + HTML/JSON export | `[ ]` |
| `templates/svg_documentation_template.html` | fresh-styled HTML template | `[ ]` |
| `generate_samples.py` | renders default sample SVG per component | `[ ]` |
| `tests/__init__.py` | makes tests a package | `[ ]` |
| `tests/test_svg_components.py` | component contract tests | `[ ]` |
| `tests/test_documentation.py` | documentation generation tests | `[ ]` |
| `tests/test_svg_rendering.py` | SVG output + snapshot tests | `[ ]` |
| `tests/snapshots/svg_samples.json` | SVG hash snapshots | `[ ]` |
| `svg_components/*/sample.svg` | per-component sample output (9 files) | `[ ]` |
| `documentation_data.json` | generated JSON data blob | `[ ]` |
| `documentation.html` | final documentation output | `[ ]` |
