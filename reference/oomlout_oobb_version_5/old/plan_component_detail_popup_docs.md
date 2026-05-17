# Plan: Component Detail Pages And Popup Documentation

## Goal

Extend the documentation system so each component has a richer documentation
page with:

- the core component description
- full variable information
- representative test images
- human-readable captions for those images
- room for extra explanatory detail beyond the short card summary

The main [components/documentation.html](/c:/gh/oomlout_oobb_version_5/components/documentation.html)
should then open that richer component documentation inside a popup/modal when a
component card is clicked.

## Current State

The current documentation pipeline is centered in
[components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py).

Today it:

- discovers component metadata via `discover_objects()`
- normalizes metadata into a JSON payload
- injects that payload into the main HTML template
- writes simple per-folder `README.md` files

The current main page:

- renders one card per component
- shows title, category, short description, and variable chips
- only supports small inline variable popups inside each card
- does not expose test images, captions, or long-form documentation

The current sample-image planning work already gives us useful source material:

- folder-local `TEST_SAMPLES.md`
- `test()` functions in each `working.py`
- expected image outputs such as `images/test_1.png`

## Target End State

Each real component folder should own richer documentation content that can be
generated and then surfaced in the main documentation UI.

The user flow should be:

1. Open the main documentation page.
2. Click a component card.
3. See a popup/modal with the component detail page content.
4. Review description, variables, sample images, and image captions without
   leaving the page.

The generated docs system should remain static-file friendly:

- no server required
- no runtime build step in the browser
- output should work from local files as much as possible

## Recommended Architecture

### 1. Keep one canonical data generator

Continue using
[components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)
as the single source of generated documentation data.

Do not create a second unrelated generator.

Instead, expand the documentation payload so each component entry contains:

- existing metadata fields
- image entries derived from `TEST_SAMPLES.md`
- optional long-form detail content
- relative links to generated component detail pages
- popup-safe HTML fragments or structured data that can be rendered in the
  modal

### 2. Generate one detail page per component

For each component folder, generate a dedicated documentation page, likely one
of:

- `components/<name>/DETAILS.md`
- `components/<name>/DETAILS.html`
- `components/<name>/README.md` expanded to carry the richer content

Recommendation:

- keep `README.md` as the human-editable canonical component detail source
- generate `component_detail.html` or similarly named HTML alongside it for
  popup rendering

That keeps authoring pleasant while keeping the popup fast and predictable.

### 3. Parse test sample documentation into structured image docs

Use each folder's `TEST_SAMPLES.md` as the initial source for image captions and
sample meaning.

For each sample image, the generated documentation should include:

- filename, such as `test_1.png`
- image path, such as `components/<name>/images/test_1.png`
- intent text from the sample definition
- the sample kwargs block
- optional preview rotation
- folder-level notes

This means we do not have to invent captions separately if they already exist in
the sample doc.

### 4. Open modal content from structured data, not ad-hoc DOM scraping

The main documentation page should open a modal based on documentation data
already loaded into `window.DOCUMENTATION_DATA`.

Do not scrape card HTML to build popup content.

Recommended modal data model per component:

- `command`
- `name_long`
- `description`
- `summary`
- `category`
- `returns`
- `variables`
- `detail_markdown` or `detail_html`
- `sample_images`

### 5. Keep popup rendering in the main template

Update
[templates/oobb_documentation_template.html](/c:/gh/oomlout_oobb_version_5/templates/oobb_documentation_template.html)
to own:

- modal container markup
- modal styles
- click handlers for cards
- keyboard close behavior
- image gallery rendering
- variable table rendering
- long-form detail rendering

This keeps the UX logic in one place and makes regeneration simple.

## Content Model Recommendation

Each component should expose two layers of documentation:

### Card layer

This remains lightweight:

- short title
- category
- one-paragraph summary
- quick variable chips

### Detail layer

This should appear in the popup and include:

- component title
- long description
- aliases, if any
- category and returns type
- full variable table
- image gallery
- image captions and sample intent
- optional extra notes or usage guidance

## Proposed File Layout

Recommended generated and source files:

- `components/<name>/README.md`
  - human-readable main detail source
- `components/<name>/TEST_SAMPLES.md`
  - sample-image source and captions
- `components/<name>/images/test_1.png`
  - generated sample image outputs
- `components/<name>/component_detail.html`
  - generated popup-ready detail HTML fragment or page

Optional alternative if simpler:

- skip standalone `component_detail.html`
- embed all detail HTML directly inside `documentation_data.json`

Recommendation:

- start by embedding structured detail data in the JSON payload
- only generate separate per-component HTML files if payload size becomes
  awkward or if standalone component pages become useful

This lowers complexity for the first implementation.

## Recommended Implementation Phases

### Phase 1: Extend the documentation payload

Update
[components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)
so each component entry also includes:

- `detail_source_path`
- `readme_markdown`
- `sample_images`
- `sample_notes`
- `has_test_images`

Work items:

1. Add a helper to read `README.md` from each component folder if present.
2. Add a helper to parse `TEST_SAMPLES.md`.
3. Add a helper to scan `images/test_*.png`.
4. Merge those into the normalized component entry.

### Phase 2: Improve markdown generation rules

Decide how `README.md` should be used going forward.

Recommended rule:

- `README.md` becomes the editable long-form component description file
- if missing, the generator can synthesize a fallback from metadata

That means the markdown export step should stop overwriting thoughtful hand-made
content blindly.

Important design choice:

- either preserve existing `README.md` if present
- or generate to a different file such as `AUTO_README.md`

Recommendation:

- preserve human-authored `README.md`
- generate richer auto docs to `component_detail.html` and JSON

### Phase 3: Add modal UI to the main documentation page

Update
[templates/oobb_documentation_template.html](/c:/gh/oomlout_oobb_version_5/templates/oobb_documentation_template.html)
to support:

- card click opening a modal
- modal close button
- backdrop click to close
- `Escape` key to close
- scrolling inside the modal
- responsive image gallery layout

The card should remain lightweight; the modal becomes the detail surface.

### Phase 4: Render full component details in the modal

The popup content should include:

- hero title and category badge
- description block
- images section
- sample caption list
- variables table
- returns and aliases section

If `README.md` contains richer markdown sections, render them in a dedicated
"Details" section below the generated metadata summary.

### Phase 5: Regenerate and validate

Update the regen workflow so
[action_documentation_regenerate.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate.bat)
still rebuilds everything in one run.

Validation pass should check:

- every component card still renders
- clicking a card opens a modal
- images load when present
- missing images degrade gracefully
- missing `README.md` degrades gracefully
- long text scrolls correctly on mobile and desktop

## Detailed Move List

### Generator changes

Files to update:

- [components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)
- possibly [action_documentation_regenerate.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate.bat)

New helper responsibilities:

- resolve component folder from discovered object
- read `README.md` safely
- parse `TEST_SAMPLES.md` into structured sample docs
- collect image files from `images/`
- attach all of the above to each component entry

### Template/UI changes

Files to update:

- [templates/oobb_documentation_template.html](/c:/gh/oomlout_oobb_version_5/templates/oobb_documentation_template.html)

New UI responsibilities:

- modal markup
- modal open/close functions
- popup detail renderer
- image gallery renderer
- richer variable rendering
- card click behavior

### Optional generated artifact changes

Files to generate:

- `components/<name>/component_detail.html` if separate detail files are chosen
- updated [components/documentation_data.json](/c:/gh/oomlout_oobb_version_5/components/documentation_data.json)
- updated [components/documentation.html](/c:/gh/oomlout_oobb_version_5/components/documentation.html)

## Parsing Strategy For Sample Images

`TEST_SAMPLES.md` already contains structured information in a predictable
format. The parser should extract:

- sample filename
- intent
- preview rotation
- kwargs
- folder notes

Then enrich that with filesystem checks:

- whether the PNG exists
- relative path to the PNG
- relative path to the matching SCAD, if present

If a sample image is missing, do not fail generation. Instead:

- keep the sample entry
- mark it as missing
- render a "not generated yet" state in the popup

## Recommended Popup UX

When a card is clicked:

1. The modal opens centered over the page.
2. The header shows component name, long name, and category.
3. The first content block shows the description.
4. The second content block shows image tiles with captions.
5. The third block shows the variable table.
6. Optional long-form markdown content appears after the generated summary.

Important UX behaviors:

- preserve search/filter state behind the modal
- avoid page navigation
- keep images clickable for larger view if practical
- support mobile scrolling without clipping

## Risks And Design Traps

### Risk: `README.md` regeneration destroys authored content

Current markdown generation writes README files directly.

Mitigation:

- treat `README.md` as authored content
- either stop overwriting it or only generate if missing

### Risk: JSON payload gets too large

Embedding full markdown and full sample data for every component may bloat the
main page.

Mitigation:

- first measure payload size after adding detail content
- if too large, move long-form detail HTML to per-component files and lazy-load
  them

### Risk: local-file image paths fail

Popup image references must work when opening `documentation.html` locally.

Mitigation:

- keep all paths relative to `components/documentation.html`
- verify with local file browsing, not just server-based assumptions

### Risk: template complexity rises too quickly

The current template is simple and static.

Mitigation:

- keep rendering logic data-driven
- separate small helper functions in the inline script
- avoid mixing card rendering and modal rendering logic

## Recommended Decisions Before Implementation

These are the best default choices unless review changes them:

1. `README.md` becomes the human-authored long-form detail source.
2. `TEST_SAMPLES.md` becomes the image-caption source.
3. `components/documentation.py` stays the only documentation generator.
4. The first implementation embeds detail data in `documentation_data.json`.
5. The main docs page opens a modal instead of navigating away.

## Suggested Execution Order

1. Update the generator payload shape in `components/documentation.py`.
2. Decide and lock the `README.md` preservation policy.
3. Add modal markup and rendering to the HTML template.
4. Render sample images and captions inside the modal.
5. Regenerate docs and verify local-file behavior.
6. Only if payload size or performance becomes a problem, split out
   per-component HTML files.

## Deliverables

Implementation should eventually produce:

- richer documentation entries in `documentation_data.json`
- updated main documentation UI with modal popups
- per-component detail content surfaced in the popup
- sample images and captions shown in the popup
- a regeneration workflow that rebuilds everything consistently

## Progress

- [x] Current documentation pipeline reviewed
- [x] Main HTML popup requirements analyzed
- [x] Plan for per-component detail docs written
- [x] Generator payload extended with detail-page data
- [x] Modal UI added to main documentation template
- [x] Sample images and captions rendered in popup
- [x] Documentation regeneration flow updated and verified
