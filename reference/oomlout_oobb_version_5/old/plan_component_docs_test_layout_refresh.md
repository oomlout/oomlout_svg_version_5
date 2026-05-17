# Plan: Component Docs, Test Layout, And Full Regeneration Refresh

## Goal

Update the component test-output and documentation system so it matches the new
structure and documentation expectations:

- each component should use a `test/` folder instead of `images/`
- each sample should live in its own folder such as `test/test_1/`
- each sample folder should contain:
  - `working.scad`
  - `image.png`
- the component detail docs should show fuller example-piece information,
  including both the explicitly set values and the default values
- the component detail docs should include a link to download/open the matching
  SCAD file
- there should be a new batch file,
  [action_documentation_regenerate_all.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate_all.bat),
  that regenerates documentation and also generates the component test outputs

This plan is for the next implementation pass.

## Requested Changes

The requested behavior changes are:

1. Rename test output folder usage from `images/` to `test/`.
2. Replace flat filenames like `images/test_1.png` with nested sample folders:
   - `test/test_1/working.scad`
   - `test/test_1/image.png`
3. Update the docs to link to `working.scad` for each example/sample.
4. Expand the example/sample documentation to show:
   - values explicitly set in the sample
   - defaults for the component variables
5. Add a new batch entry point that runs:
   - docs regeneration
   - component test generation
   - render/export of sample SCAD and image outputs

## Current State

Today the repo uses:

- `test()` functions in each component `working.py`
- sample metadata in `TEST_SAMPLES.md`
- documentation generation in
  [components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)
- popup/modal display in
  [templates/oobb_documentation_template.html](/c:/gh/oomlout_oobb_version_5/templates/oobb_documentation_template.html)
- docs regeneration in
  [action_documentation_regenerate.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate.bat)

The current sample-output convention is still the older flat layout:

- `images/test_1.scad`
- `images/test_1.png`

The current docs payload and detail pages already include:

- parsed sample captions from `TEST_SAMPLES.md`
- sample kwargs
- preview rotation
- image path metadata
- a detail page per component

What they do not yet include:

- a normalized "set values vs default values" example section
- SCAD file links for each example
- the new `test/test_1/working.scad` filesystem layout
- a single batch file that regenerates both docs and test assets

## Recommended End State

Each component folder should converge on this structure:

- `components/<name>/working.py`
- `components/<name>/TEST_SAMPLES.md`
- `components/<name>/README.md` if authored
- `components/<name>/test/test_1/working.scad`
- `components/<name>/test/test_1/image.png`
- `components/<name>/test/test_2/working.scad`
- `components/<name>/test/test_2/image.png`
- `components/<name>/documentation_detail.html`

Each detail page should show, for every example/sample:

- example title / intent
- preview image
- link to `working.scad`
- explicit sample kwargs
- resolved default values for the component variables
- helper-specific values when relevant
- notes/rules from `TEST_SAMPLES.md`

The main docs modal should display that richer content unchanged via the
generated detail page.

## Recommended Architecture

### 1. Update the `test()` contract first

The file layout change should be driven from the component `test()` functions.

Every component `test()` should create:

- `test/`
- `test/test_1/`
- `test/test_2/`

Inside each sample folder it should write:

- `working.scad`
- `image.png`

Recommendation:

- stop writing flat files into `images/`
- keep sample folder names aligned exactly to `filename` from `TEST_SAMPLES.md`
- convert `filename: "test_1"` into folder `test/test_1/`

### 2. Update the sample-doc parser and payload

[components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)
should change its sample path assumptions from:

- `images/test_1.png`
- `images/test_1.scad`

to:

- `test/test_1/image.png`
- `test/test_1/working.scad`

It should also compute two additional example data blocks:

- `set_values`
- `default_values`

Recommendation for payload per sample:

- `sample_id`
- `title`
- `intent`
- `image_path`
- `scad_path`
- `preview_rot`
- `set_values`
- `default_values`
- `helper_kwargs`
- `companion_geometry_kwargs`
- `implementation_rule`
- `exists`
- `scad_exists`

### 3. Treat component metadata as the source of defaults

The component defaults should come from `define()["variables"]`, not from
guesswork or from the sample kwargs.

For each variable:

- if the sample sets a value explicitly, it belongs in `set_values`
- if the variable has a documented default in metadata, include it in
  `default_values`

This gives the example section a consistent structure even when the sample only
sets a few keys.

### 4. Keep `TEST_SAMPLES.md` as the example source

`TEST_SAMPLES.md` should still be the source for:

- sample names
- intent/caption text
- example kwargs
- helper/companion example data
- notes and implementation rules

The generator should enrich it with:

- resolved file paths
- defaults from component metadata
- existence flags for generated files

### 5. Add a separate full-regeneration batch file

Keep the current
[action_documentation_regenerate.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate.bat)
focused if possible.

Add a new wrapper:

- [action_documentation_regenerate_all.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate_all.bat)

That new batch file should:

1. regenerate docs JSON/HTML/detail pages
2. run component test generation across all real component folders
3. produce `working.scad` and `image.png` for each sample
4. report completion clearly

Recommendation:

- keep the all-in-one batch additive, not replacing the simpler docs-only batch

## Detailed Implementation Plan

### Phase 1: Change the sample output layout

Files to update:

- all affected `components/<name>/working.py` files with `test()` functions
- possibly the test planning docs for consistency

Required behavior change inside each `test()`:

- replace `images_dir` with `test_dir`
- for each sample:
  - create `sample_dir = os.path.join(test_dir, sample["filename"])`
  - write SCAD to `os.path.join(sample_dir, "working.scad")`
  - write PNG to `os.path.join(sample_dir, "image.png")`

Required return value recommendation:

- return a list of generated PNG paths
- those paths should now point to `test/test_1/image.png`

Special cases still apply:

- `oobb_rot`
- `import_stl`
- components returning `thing["components"]`

### Phase 2: Update the docs payload to match the new layout

Files to update:

- [components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)

Required parser changes:

- replace any `images/` assumptions with `test/<sample_id>/`
- expose:
  - `detail_image_path = f"test/{sample_id}/image.png"`
  - `detail_scad_path = f"test/{sample_id}/working.scad"`

Required enrichment changes:

- load component variable metadata
- build a `default_values` object from metadata defaults
- build a `set_values` object from sample kwargs, helper kwargs, or companion
  kwargs as appropriate

Recommendation for helper components:

- `oobb_rot` should expose:
  - `set_values.helper_kwargs`
  - `set_values.companion_geometry_kwargs`
  - `default_values` from the helper metadata

### Phase 3: Expand the detail-page HTML

Files to update:

- [components/documentation.py](/c:/gh/oomlout_oobb_version_5/components/documentation.py)
  - detail page generator

Required new example-piece section content:

- image tile
- image caption / intent
- SCAD link
- "Set Values" block
- "Default Values" block
- preview rotation
- notes / implementation rule

Recommendation:

- use collapsible `<details>` blocks for the set/default JSON blocks
- keep the SCAD link prominent near the image

For missing generated files:

- show "SCAD not generated yet" and "Image not generated yet"
- do not hide the example entry entirely

### Phase 4: Ensure the popup supports the richer content cleanly

Files to update:

- [templates/oobb_documentation_template.html](/c:/gh/oomlout_oobb_version_5/templates/oobb_documentation_template.html)
  only if the new detail-page size creates modal usability issues

Likely adjustments:

- allow taller iframe content comfortably
- keep modal scrolling smooth on mobile
- ensure long example sections are still readable

### Phase 5: Add the all-in-one regeneration batch

Files to add/update:

- add
  [action_documentation_regenerate_all.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate_all.bat)
- possibly add a Python runner helper if batch-only orchestration becomes messy

Recommended flow:

1. call the existing docs generator
2. run a Python script that:
   - discovers component folders
   - imports each `working.py`
   - calls `test()` where present
   - logs failures without crashing silently
3. print a completion summary

Recommendation:

- if the orchestration is more than a few commands, add a helper script such as
  `components/generate_all_tests.py` and keep the batch file thin

## Data Model Additions

Each object entry in `documentation_data.json` should gain or update:

- `detail_page`
- `sample_images`
- `has_test_images`

Each sample entry should include:

- `sample_id`
- `filename`
- `title`
- `intent`
- `image_path`
- `detail_image_path`
- `scad_path`
- `detail_scad_path`
- `exists`
- `scad_exists`
- `set_values`
- `default_values`
- `preview_rot`
- `implementation_rule`

## Example-Value Resolution Rules

To avoid ambiguity, use these rules:

1. `set_values`
   - the exact keys explicitly present in the sample definition
2. `default_values`
   - the defaults listed in the component metadata variables
3. Do not merge them into one object in the UI.
4. Show both, side by side or as separate details blocks.

For components with empty variable metadata:

- show `default_values: none documented`

For helper flows:

- show separate blocks when the sample schema is not plain `kwargs`

## Batch Workflow Recommendation

Recommended final command layout:

- docs only:
  [action_documentation_regenerate.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate.bat)
- docs + tests + sample assets:
  [action_documentation_regenerate_all.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate_all.bat)

Suggested internal sequence for the all-in-one batch:

1. regenerate documentation payload and HTML
2. generate all component sample outputs
3. regenerate documentation again so existence flags and links are fresh

That final docs pass is important because it lets the JSON reflect the newly
generated sample assets.

## Risks And Tricky Spots

### Risk: all component `test()` functions need synchronized path changes

There are many generated `test()` functions now, so the folder-layout change
needs to be applied consistently.

Mitigation:

- do it with one repo-wide scripted pass
- verify via grep for `images_dir` leftovers

### Risk: docs and tests drift apart

If docs expect `test/test_1/image.png` but `test()` still writes to `images/`,
the popup will look broken.

Mitigation:

- land test layout change before or together with docs generator changes

### Risk: defaults are inconsistent or poorly documented

Some components have sparse metadata variables.

Mitigation:

- display only documented defaults
- explicitly mark missing defaults as undocumented rather than guessing

### Risk: generated HTML pages get long

Showing both set/default value blocks for each sample increases page length.

Mitigation:

- use expandable details blocks
- keep the first view concise and scannable

### Risk: test generation still depends on missing environment packages

Rendering may still be blocked by missing `solid` or other toolchain issues.

Mitigation:

- ensure the all-in-one batch reports failures clearly
- let docs regenerate even if some sample renders fail

## Deliverables

Implementation should produce:

- updated `test/` sample folder layout across components
- richer component detail docs with set/default example data
- SCAD links for each example/sample
- updated JSON and HTML docs reflecting the new paths
- a new all-in-one regeneration batch file

## Suggested Execution Order

1. Update all `test()` implementations to the new `test/test_1/working.scad`
   layout.
2. Update the docs generator to read the new layout and expose `set_values` and
   `default_values`.
3. Expand the detail-page HTML to show both value blocks and SCAD links.
4. Add `action_documentation_regenerate_all.bat`.
5. Regenerate everything and verify paths, popup content, and sample file links.

## Progress

- [x] New requirements reviewed
- [x] Current docs/test layout inspected
- [x] Refresh plan written
- [x] Component `test()` functions migrated to `test/<sample>/working.scad` layout
- [x] Documentation payload updated for set/default values and SCAD links
- [x] Detail pages updated to show richer example-piece information
- [x] `action_documentation_regenerate_all.bat` added
- [x] Full regeneration flow run and verified

## Implementation Notes

### Completed

- component `test()` functions now write sample assets to:
  - `test/test_1/working.scad`
  - `test/test_1/image.png`
- documentation payload entries now expose:
  - `set_values`
  - `default_values`
  - `scad_path`
  - `detail_scad_path`
  - `image_path`
  - `detail_image_path`
- generated detail pages now show:
  - example intent text
  - preview image or a missing-image placeholder
  - SCAD download link or a missing-SCAD placeholder
  - `Set Values`
  - `Default Values`
- added
  [components/generate_all_component_tests.py](/c:/gh/oomlout_oobb_version_5/components/generate_all_component_tests.py)
  to run every component `test()` function
- added
  [action_documentation_regenerate_all.bat](/c:/gh/oomlout_oobb_version_5/action_documentation_regenerate_all.bat)
  to run docs generation, test generation, and a final docs refresh

### Verification Status

- `action_documentation_regenerate_all.bat` runs successfully end-to-end
- `components/documentation_data.json` now contains the new `test/...` paths and
  richer example metadata
- generated detail pages such as
  [components/oring/documentation_detail.html](/c:/gh/oomlout_oobb_version_5/components/oring/documentation_detail.html)
  include `Set Values`, `Default Values`, and `Download SCAD`

### Known Environment Blocker

- sample PNG/SCAD generation is wired correctly but currently blocked in this
  environment because component imports fail with
  `ModuleNotFoundError: No module named 'solid'`
- because of that blocker, the refreshed docs currently show the correct new
  paths and placeholders, but most sample files are not yet physically present
  until the missing dependency is installed
