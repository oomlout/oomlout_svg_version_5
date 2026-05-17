# Test Samples

## Implementation Contract

Apply these instructions exactly in `working.py` for this folder. Do not shorten or reinterpret the steps.

1. Open `working.py` in this folder.
2. If `def test():` already exists, replace the whole function. If it does not exist, add a new `test()` at the end of the file after the existing public functions.
3. Add the imports shown in the code skeleton below inside `test()`.
4. Set `folder = os.path.dirname(os.path.abspath(__file__))`.
5. Set `images_dir = os.path.join(folder, "images")`.
6. Call `os.makedirs(images_dir, exist_ok=True)`.
7. Copy the exact `samples = ...` block from this file into `test()`.
8. For each sample, deep-copy the sample data before modifying it.
9. Normalize the return from `action(...)` into a list before rendering:
   - if the result is already a list, keep it unchanged
   - if the result is a single dict, wrap it as `[result]`
10. Do not adjust the camera. The only allowed view control is the `preview_rot` geometry rotation listed in this file.
11. If a sample `kwargs` already contains its own `rot`, keep that value exactly as written and still apply `preview_rot` as the outer wrapper.
12. Write matching `.scad` and `.png` files into the local `images` folder using each sample filename.
13. Return a `generated_files` list containing the PNG paths in render order.

### Exact code skeleton

```python
def test():
    import copy
    import os
    import opsc

    folder = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(folder, "images")
    os.makedirs(images_dir, exist_ok=True)

    samples = [
        # Paste the exact samples block from this TEST_SAMPLES.md here.
    ]

    generated_files = []

    for sample in samples:
        kwargs = copy.deepcopy(sample["kwargs"])
        result = action(**kwargs)
        if isinstance(result, list):
            components = result
        else:
            components = [result]

        preview_rot = sample["preview_rot"]
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

### Exact rotation wrapper

```python
wrapped = [{
    "type": "rotation",
    "typetype": "positive",
    "pos": [0, 0, 0],
    "rot": preview_rot,
    "objects": components,
}]
```

Skip the wrapper only when `preview_rot` is exactly `[0, 0, 0]`.

### Exact render calls

```python
opsc.opsc_make_object(
    scad_path,
    wrapped,
    mode="true",
    save_type="none",
    overwrite=True,
    render=True,
)
opsc.save_to_png(scad_path, fileOut=png_path)
```

## Exact `samples` block to paste into `working.py`

```python
samples = [{'filename': 'test_1',
  'preview_rot': [35, 0, 25],
  'kwargs': {'pos': [0, 0, 0], 'size': [24, 24, 12], 'zz': 'bottom'}},
 {'filename': 'test_2',
  'preview_rot': [35, 0, 25],
  'kwargs': {'pos': [0, 0, 0], 'size': [36, 18, 8], 'zz': 'middle'}}]
```

## Sample-by-sample meaning

### Sample 1: `test_1.png`
- Intent: default cube wrapper preview.
- preview_rot: `[35, 0, 25]`
- kwargs: `{"pos":[0,0,0],"size":[24,24,12],"zz":"bottom"}`
- Implementation rule: keep the sample values exactly as written. If `kwargs` already contains `rot`, do not replace it; use `preview_rot` only as the outer rotation wrapper for the final rendered scene.

### Sample 2: `test_2.png`
- Intent: flatter rectangular block.
- preview_rot: `[35, 0, 25]`
- kwargs: `{"pos":[0,0,0],"size":[36,18,8],"zz":"middle"}`
- Implementation rule: keep the sample values exactly as written. If `kwargs` already contains `rot`, do not replace it; use `preview_rot` only as the outer rotation wrapper for the final rendered scene.

## Folder-specific notes

- Output folder: `images`
- Output files: `test_1.png`, `test_2.png`
- Notes: show that this wrapper behaves like the centered cube version.
- Final instruction: do not invent new sample values, do not invent extra camera settings, and do not swap in a different rotation than the `preview_rot` listed above.
