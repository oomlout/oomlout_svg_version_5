# Plan: Add Representative Image Tests to Every Component

## Goal

Add a `test` section to every real component so a follow-on implementation pass
can generate representative preview images into:

- `images/test_1.png`
- `images/test_2.png`
- `images/test_3.png` when a third sample is justified

Each component folder also gets a local [TEST_SAMPLES.md](./components) file so
work can be done one folder at a time by a less capable model without needing
repo-wide context.

## Required Test Contract

For each `components/<name>/working.py` implementation:

1. Add a `test()` function in the same file.
2. Create an `images` folder inside that component directory if it does not
   exist.
3. Generate one PNG per sample using the filenames from the folder-local
   `TEST_SAMPLES.md`.
4. Use the exact sample kwargs listed in that file unless a note says otherwise.
5. Make the output representative of the shape, not just technically valid.

## Exact `test()` Function Recipe

The follow-on model should not invent its own structure. It should add a
`test()` function using this exact recipe and only substitute the sample values
from the folder-local `TEST_SAMPLES.md`.

### Required imports inside `test()`

```python
def test():
    import copy
    import os
    import opsc
```

### Required filesystem behavior

Inside `test()`:

1. Set `folder = os.path.dirname(os.path.abspath(__file__))`
2. Set `images_dir = os.path.join(folder, "images")`
3. Call `os.makedirs(images_dir, exist_ok=True)`

### Required sample loop structure

The test should build a `samples` list matching the local `TEST_SAMPLES.md`.

For each sample:

1. Deep-copy the sample kwargs.
2. Call the component `action(**kwargs)`.
3. Normalize the result into a list:
   - if `action()` returns a list, keep it unchanged
   - if `action()` returns a single dict, wrap it as `[result]`
4. Apply the preview rotation using a rotation wrapper object.
5. Write a temporary SCAD file into `images/`.
6. Export PNG from that SCAD file.

### Required rotation wrapper

The model must not “adjust the camera.” It must rotate the geometry using this
wrapper:

```python
wrapped = [{
    "type": "rotation",
    "typetype": "positive",
    "pos": [0, 0, 0],
    "rot": preview_rot,
    "objects": components,
}]
```

If `preview_rot` is `[0, 0, 0]`, it may skip the wrapper.

### Required SCAD and PNG generation sequence

Use this exact sequence:

```python
scad_path = os.path.join(images_dir, f"test_{index}.scad")
png_path = os.path.join(images_dir, f"test_{index}.png")

opsc.opsc_make_object(
    scad_path,
    wrapped_or_components,
    mode="true",
    save_type="none",
    overwrite=True,
    render=True,
)
opsc.save_to_png(scad_path, fileOut=png_path)
```

### Required return value

At the end of `test()`, return a list of generated PNG paths:

```python
return generated_files
```

## Exact Code Skeleton

The follow-on model should start from this and substitute only the sample list
and any folder-specific special handling described in the folder-local
`TEST_SAMPLES.md`.

```python
def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(folder, "images")
    os.makedirs(images_dir, exist_ok=True)

    samples = [
        {
            "filename": "test_1",
            "preview_rot": [35, 0, 25],
            "kwargs": {},
        },
    ]

    generated_files = []

    for index, sample in enumerate(samples, start=1):
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, list):
            components = result
        else:
            components = [result]
        preview_rot = sample.get("preview_rot", [0, 0, 0])

        wrapped = components
        if preview_rot != [0, 0, 0]:
            wrapped = [{
                "type": "rotation",
                "typetype": "positive",
                "pos": [0, 0, 0],
                "rot": preview_rot,
                "objects": components,
            }]

        scad_path = os.path.join(images_dir, f"{sample['filename']}.scad")
        png_path = os.path.join(images_dir, f"{sample['filename']}.png")

        opsc.opsc_make_object(
            scad_path,
            wrapped,
            mode="true",
            save_type="none",
            overwrite=True,
            render=True,
        )
        opsc.save_to_png(scad_path, fileOut=png_path)
        generated_files.append(png_path)

    return generated_files
```

## Exact Placement Rules

The follow-on model should not improvise where the test goes.

1. Open `components/<name>/working.py`.
2. Leave `describe()`, `define()`, `action()`, and `render()` unchanged unless a
   folder-local note explicitly says otherwise.
3. Add `test()` near the end of the file after the existing public functions.
4. If `test()` already exists, replace the full function instead of creating a
   second `test()`.
5. Do not refactor unrelated code while adding the test.

## Standard Implementation Rules

- Prefer `type="positive"` for standalone previews, even for cutout-oriented
  components, unless the sample note says to show a negative-use case.
- Prefer centered or middle-anchored geometry when it makes the preview easier
  to read.
- Use 2 samples by default:
  - `test_1.png`: hero/basic form
  - `test_2.png`: variant, edge case, or distinctive feature
- Use 1 sample only when a second sample would be redundant.
- Use 3 samples only for components with clearly different visual families.

## Render/Camera Guidance

- Use the existing project render path rather than inventing a separate renderer.
- Prefer a simple isometric-style view when possible.
- Leave enough margin around the part so it is recognizable in the PNG.
- For flat/2D-ish shapes, tilt slightly so thickness is visible unless the shape
  is specifically meant to be read top-down.
- Do not use camera controls. Only use the `rotation` wrapper or explicit
  geometry `rot` values.

## Helper / Non-Geometry Components

Some components are helpers rather than standalone solids.

- `oobb_rot`: render a small companion cube using the helper’s returned
  rotation.
- `gridfinity_base_tile`: render the generated SCAD result as the preview.
- `import_stl`: use a local test fixture STL in the component folder.
- `raw_scad`: generate geometry from inline SCAD source.

## Folder-Local File Rules

Every `TEST_SAMPLES.md` must be treated as the source of truth for that folder.

The implementation model must read and follow these fields exactly:

- `filename`
- `preview_rot`
- `kwargs`
- `Intent`
- `Notes`

It must not invent substitute values if the file already specifies them.

## Deliverables

- One `TEST_SAMPLES.md` in every real component folder.
- The file must contain:
  - exact image filenames
  - exact kwargs
  - what the sample is trying to show
  - any special prerequisites or implementation notes

## Folder Scope

Planning files were added for these component folders:

- `bearing`
- `bolt`
- `countersunk`
- `cube`
- `cycloid`
- `cylinder`
- `d_shaft`
- `gear`
- `gridfinity_base_tile`
- `hole`
- `import_stl`
- `oobb_circle`
- `oobb_coupler_flanged`
- `oobb_cube`
- `oobb_cube_center`
- `oobb_cube_hexagon_cutout`
- `oobb_cube_new`
- `oobb_cylinder`
- `oobb_cylinder_hollow`
- `oobb_hole`
- `oobb_holes`
- `oobb_hole_new`
- `oobb_nut`
- `oobb_plate`
- `oobb_rot`
- `oobb_rounded_rectangle_hollow`
- `oobb_rounded_rectangle_rounded`
- `oobb_screw`
- `oobb_screw_countersunk`
- `oobb_screw_self_tapping`
- `oobb_screw_socket_cap`
- `oobb_slice`
- `oobb_slot`
- `oobb_sphere`
- `oobb_tube`
- `oobb_tube_new`
- `oring`
- `polyg`
- `polygon`
- `polyg_tube`
- `polyg_tube_half`
- `pulley_gt2`
- `raw_scad`
- `rounded_octagon`
- `rounded_rectangle`
- `rounded_rectangle_extra`
- `slot`
- `slot_small`
- `sphere`
- `sphere_rectangle`
- `text`
- `text_hollow`
- `tray`
- `tube`
- `tube_new`
- `vpulley`

## Execution Order Recommendation

1. Basic primitives and raw shapes
2. Composite OPSC shapes
3. OOBB geometry wrappers
4. Fasteners and mechanical parts
5. Helper/special-case components

## Progress

- [x] Repo-level rollout plan written
- [x] Folder-local sample specs written
- [x] Repo-level `test()` recipe expanded with exact placement and normalization rules
- [x] Folder-local sample specs rewritten to be fully prescriptive for weaker models
- [x] `test()` functions implemented in each `working.py`
- [ ] Images generated in each component `images` folder
- [ ] Spot-review representative previews for readability
