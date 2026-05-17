# gridfinity_tray_raw implementation plan

## Progress

- [x] Research the existing component pattern in this repo.
- [x] Inspect the vendored `ostat/gridfinity_extended_openscad` source.
- [x] Confirm initial product decisions.
- [ ] Create the callable Gridfinity wrapper SCAD module.
- [ ] Create the Python component entrypoint and metadata.
- [ ] Add focused render samples and object tests.
- [ ] Regenerate documentation artifacts and verify output.

## Locked decisions

- Public component command: `gridfinity_tray_raw`
- Backing geometry: upstream `gridfinity_basic_cup`
- Default size inputs: `gridfinity_width=2`, `gridfinity_depth=1`, `gridfinity_height=3`
- Default behavior: match upstream basic-cup defaults unless the repo transport requires otherwise
- Parameter goal: keep names recognizable to upstream so later expansion stays cheap

## Scope

### In scope for the first implementation

- Add a local callable SCAD wrapper module named `gridfinity_tray_raw(...)`
- Bridge the three public size inputs into upstream tuple inputs
- Expose the main upstream settings with stable names through the wrapper
- Add `working.py` using the existing raw-SCAD component pattern
- Add two render samples and wire them into `test()`
- Regenerate component docs after the object works

### Explicitly out of scope for the first implementation

- Editing the vendored upstream repository unless a real integration bug is proven
- Supporting upstream generators other than the basic cup
- Refactoring the repo-wide raw-SCAD transport
- Broad cleanup of Gridfinity naming outside this component

## Working assumptions

1. The right local pattern is `components/gridfinity_base_tile/working.py`: metadata + `action()` + `test()` returning a `shape: "raw_scad"` payload.
2. The right geometry entrypoint is not the upstream top-level `gridfinity_basic_cup.scad` file, because it is a customizer script rather than a callable module.
3. The correct integration is a new local wrapper SCAD file that calls `set_environment(...)` and `gridfinity_cup(...)` from the vendored upstream modules.

## Files to add

- `components/gridfinity_tray_raw/gridfinity_tray_raw_wrapper.scad`
- `components/gridfinity_tray_raw/working.py`
- `components/gridfinity_tray_raw/README.md`
- `components/gridfinity_tray_raw/TEST_SAMPLES.md`

## Implementation sequence

### Phase 1. Wrapper SCAD

- [ ] Create `gridfinity_tray_raw_wrapper.scad`.
- [ ] Import the vendored modules needed for `set_environment(...)` and `gridfinity_cup(...)`.
- [ ] Define `module gridfinity_tray_raw(...)`.
- [ ] Convert `gridfinity_width`, `gridfinity_depth`, and `gridfinity_height` into `width = [gridfinity_width, 0]`, `depth = [gridfinity_depth, 0]`, and `height = [gridfinity_height, 0]`.
- [ ] Thread the rest of the named options through to `set_environment(...)` and `gridfinity_cup(...)`.

### Phase 2. Python component

- [ ] Create `working.py` with `describe()`, `define()`, `action()`, and `test()`.
- [ ] Set category to `Gridfinity`.
- [ ] Return a raw-SCAD payload that points to the local wrapper file and module name.
- [ ] Keep transport defaults aligned with the rest of the repo: `pos`, `rot`, `type`, `inclusion`, `m`.

### Phase 3. Validation samples

- [ ] Add sample 1: default `2x1x3` cup.
- [ ] Add sample 2: one variant that proves non-size plumbing, preferably `vertical_chambers` or magnet settings.
- [ ] Render through the normal component `test()` path.

### Phase 4. Documentation

- [ ] Generate the local README and test samples markdown.
- [ ] Regenerate aggregate component docs.
- [ ] Confirm `gridfinity_tray_raw` appears under the Gridfinity category with the expected defaults.

## Parameter plan

### Public size interface

- `gridfinity_width`
- `gridfinity_depth`
- `gridfinity_height`

### First-pass exposed settings

- General cup: `filled_in`, `wall_thickness`, `headroom`
- Lip: `lip_style`, `lip_side_relief_trigger`, `lip_top_relief_height`, `lip_top_relief_width`, `lip_top_notches`, `lip_clip_position`, `lip_non_blocking`, `height_includes_lip`
- Subdivisions: `chamber_wall_thickness`, `chamber_wall_headroom`, `chamber_wall_top_radius`, `vertical_chambers`, `horizontal_chambers`, bend options, irregular subdivision options
- Base: `enable_magnets`, `enable_screws`, `magnet_size`, `screw_size`, `center_magnet_size`, `hole_overhang_remedy`, `box_corner_attachments_only`, `floor_thickness`, `efficient_floor`, `sub_pitch`, `flat_base`, `spacer`, alignment values
- Secondary groups to carry through if wiring is straightforward: label, sliding lid, fingerslide, tapered corner, wall pattern, floor pattern, wall cutout, extension tabs, bottom text, render/detail controls

### Tightening rule

If the full metadata list becomes the slowest part of the first pass, do not shrink the wrapper itself. Keep the wrapper broad, then trim only the initial Python metadata surface to the settings already verified by render tests.

## Acceptance criteria

- A call to `gridfinity_tray_raw` produces a renderable raw-SCAD component.
- Default invocation renders the upstream-equivalent `2x1x3` basic cup shape.
- At least one non-default setting changes the output through the repo test path.
- The generated SCAD resolves vendored upstream includes without editing upstream files.
- The component appears in generated docs.

## Risks

### Main risk

The upstream option surface is large enough that a one-pass mirror can be wired incorrectly.

### Control

- Keep the wrapper close to upstream naming.
- Isolate the size conversion logic.
- Validate the default render before widening sample coverage.
- Do not modify vendored upstream files unless a specific failure forces it.