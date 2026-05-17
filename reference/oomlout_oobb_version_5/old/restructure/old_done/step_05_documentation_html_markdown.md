# Step 5 — Documentation HTML & Markdown Export

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Step 4 (Documentation Data Model & JSON Export) must be complete and all tests passing  
> **Blocks:** Step 10 (final documentation generation)

---

## Goal

Create the HTML documentation template (a searchable, filterable page) and the Markdown README auto-generation system. Add a CLI entry point so documentation can be regenerated with a single command.

After this step, running `python part_calls/documentation.py --json --html --markdown` will produce:
1. `part_calls/documentation_data.json` — structured JSON data
2. `part_calls/documentation.html` — interactive HTML page
3. `part_calls/objects/README.md` — index of all object types
4. `part_calls/sets/README.md` — index of all part sets  
5. Per-folder `README.md` for each discovered folder

---

## Background — The Roboclick HTML Template

Roboclick's `templates/documentation_template.html` is a ~960-line self-contained HTML file with:
- Embedded CSS with pastel rainbow palette and glassmorphism effects
- Client-side JavaScript that reads embedded JSON data
- Category filter sidebar
- Full-text search box
- Card layout with action name, description, and variables table
- Responsive design

The OOBB version will follow the same pattern but with two sections: **Objects** and **Part Sets**.

### Markdown READMEs

In addition to the HTML page, every discovered folder gets a `README.md` so that GitHub/git browsing shows useful information:

```markdown
# oobb_object_circle

**OOBB Object: Circle**

Generates circular OOBB plates with optional doughnut, shaft, and bearing features.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| diameter | Circle diameter in grid units. | number | 3 |
| thickness | Plate thickness in mm. | number | 3 |
| size | Grid system (oobb or oobe). | string | oobb |
| shaft | Optional shaft type. | string | |
| extra | Extra feature (e.g. doughnut_5). | string | |

## Category

OOBB Geometry

## Source

`oobb_get_items_oobb.get_circle()`
```

---

## Deliverables

### 1. `templates/oobb_documentation_template.html`

Self-contained HTML file with:

- **Header**: "OOBB Part Documentation" with generated date and counts
- **Sidebar**: Category filter buttons (one per unique category across objects and sets)
- **Search**: Full-text filter input
- **Tab bar**: "Objects" | "Part Sets" toggle
- **Card grid**: Each card shows:
  - Name (folder name)
  - Long name
  - Description
  - Category badge
  - Aliases
  - Expandable variables table
- **Data injection**: Uses `<!-- DOCUMENTATION_DATA_PLACEHOLDER -->` marker (same as roboclick) where the JSON data is injected as a `<script>` block
- **Styling**: Clean pastel palette, responsive grid, glassmorphism cards

### 2. Add to `part_calls/documentation.py`

#### HTML export function
```python
def export_documentation_html(template_file, output_file, objects_root=None, sets_root=None):
    """Generate HTML documentation page.
    
    1. Collect documentation data (objects + part_sets)
    2. Read template HTML file
    3. Inject JSON data into template at placeholder
    4. Write output HTML file
    """
```

#### Markdown export function
```python
def export_documentation_markdown(objects_root=None, sets_root=None):
    """Generate Markdown README files.
    
    Creates:
    1. part_calls/objects/README.md — index table of all objects
    2. part_calls/sets/README.md — index table of all sets
    3. <folder>/README.md for each discovered object and set
    
    Index format:
    # OOBB Objects
    | Name | Description | Category |
    |------|-------------|----------|
    | [oobb_object_circle](oobb_object_circle/) | Generates circular plates... | OOBB Geometry |
    
    Per-folder format:
    # <name>
    **<name_long>**
    <description>
    ## Variables
    | Name | Description | Type | Default |
    ...
    """
```

#### CLI entry point
```python
def cli():
    """Command-line interface for documentation generation."""
    parser = argparse.ArgumentParser(description="OOBB Documentation Generator")
    parser.add_argument("--json", default="", help="Output path for JSON documentation")
    parser.add_argument("--html-template", default="", help="Path to HTML template file")
    parser.add_argument("--html-output", default="", help="Output path for HTML documentation")
    parser.add_argument("--markdown", action="store_true", help="Generate Markdown README files")
    parser.add_argument("--objects-root", default=None)
    parser.add_argument("--sets-root", default=None)
    args = parser.parse_args()
    
    if args.json:
        export_documentation_json(args.json, ...)
    if args.html_template and args.html_output:
        export_documentation_html(args.html_template, args.html_output, ...)
    if args.markdown:
        export_documentation_markdown(...)

if __name__ == "__main__":
    cli()
```

### 3. `tests/test_documentation_generation.py` — additions

Three new test cases (added to the test file from Step 4):

#### `test_export_html_creates_file`
- Create a temp template HTML file with `<!-- DOCUMENTATION_DATA_PLACEHOLDER -->` marker
- Call `export_documentation_html(template, output)`
- Assert output file was created
- Assert output file contains `DOCUMENTATION_DATA`
- Assert output file contains at least one object name (e.g. `oobb_object_circle`)

#### `test_export_markdown_creates_index`
- Call `export_documentation_markdown()` with temp roots containing valid working.py files
- Assert `<objects_root>/README.md` was created
- Assert `<sets_root>/README.md` was created
- Assert index files contain `|` (table formatting)
- Assert index files contain folder names

#### `test_per_folder_readme_generated`
- Call `export_documentation_markdown()` with temp roots
- For each discovered folder, assert `<folder>/README.md` was created
- Assert each README contains the description from `define()`
- Assert each README contains a variables table

---

## Files Created/Modified

| File | Change |
|------|--------|
| `templates/oobb_documentation_template.html` | **NEW** — HTML template |
| `part_calls/documentation.py` | Add `export_documentation_html()`, `export_documentation_markdown()`, `cli()` |
| `tests/test_documentation_generation.py` | Add 3 test cases |

---

## Test Contract

**All of the following must pass before proceeding to Step 6:**

```powershell
# Documentation tests (all 8: 5 from Step 4 + 3 new)
python -m unittest tests.test_documentation_generation -v

# Step 1-3 tests (must still pass)
python -m unittest tests.test_object_discovery tests.test_object_working_files tests.test_object_dispatch_integration -v

# Pre-existing tests
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery -v
```

**Gate command:**
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Acceptance Criteria

- [ ] `templates/oobb_documentation_template.html` exists (~500+ lines)
- [ ] HTML template has placeholder for data injection
- [ ] `export_documentation_html()` produces a valid HTML file with embedded JSON
- [ ] `export_documentation_markdown()` creates index README.md for objects and sets
- [ ] Per-folder README.md files are generated with name, description, variables table
- [ ] CLI works: `python part_calls/documentation.py --json out.json`
- [ ] CLI works: `python part_calls/documentation.py --html-template templates/oobb_documentation_template.html --html-output out.html`
- [ ] CLI works: `python part_calls/documentation.py --markdown`
- [ ] All 8 documentation tests pass
- [ ] All pre-existing tests still pass

---

## Estimated Scope

- ~500 lines for HTML template
- ~100 lines of new code in `documentation.py`
- ~60 lines of new test code
- No changes to any existing non-test files
