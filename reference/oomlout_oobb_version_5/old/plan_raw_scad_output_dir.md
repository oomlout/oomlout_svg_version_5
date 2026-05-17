# Plan: Save raw_scad files to output directory

**Goal:** When `raw_scad` writes its helper `.scad` file, put it in the same directory as the generated output file rather than `_raw_scad_cache/`. Falls back to `_raw_scad_cache/` if called outside `opsc_make_object`.

---

## Changes (all in `opsc.py`)

- [x] **Change 1 — `opsc_make_object`**: Compute `output_dir` and pass it to `opsc_get_object`.
  ```python
  output_dir = os.path.dirname(os.path.abspath(filename))
  final_object = opsc_get_object(objects, mode=mode, output_dir=output_dir)
  ```

- [x] **Change 2a — `opsc_get_object` signature**: Add `output_dir=None` parameter.
  ```python
  def opsc_get_object(objects, mode="laser", output_dir=None):
  ```

- [x] **Change 2b — `opsc_get_object` → `get_opsc_item` call**: Forward `output_dir`.
  ```python
  opsc_item = get_opsc_item(obj, output_dir=output_dir)
  ```

- [x] **Change 2c — `opsc_get_object` recursive call**: Forward `output_dir` in rotation branch.
  ```python
  opsc_objects = opsc_get_object(objects_2, mode=mode, output_dir=output_dir)
  ```

- [x] **Change 3 — `get_opsc_item`**: Add `output_dir=None` param; inject `cache_dir` into params before calling `raw_scad`.
  ```python
  def get_opsc_item(params, output_dir=None):
      ...
      if output_dir is not None and p2.get("shape") == "raw_scad":
          p2["cache_dir"] = output_dir
  ```

- [x] **Change 4 — `_write_raw_scad_source`**: Add `cache_dir=None` param; use it instead of `_RAW_SCAD_CACHE_DIR` when provided.
  ```python
  def _write_raw_scad_source(source, module_name, cache_dir=None):
      if cache_dir is None:
          cache_dir = _RAW_SCAD_CACHE_DIR
      os.makedirs(cache_dir, exist_ok=True)
      filename = os.path.join(cache_dir, f"{module_name}_{digest}.scad")
  ```

- [x] **Change 5 — `raw_scad`**: Read `cache_dir` from params and pass to `_write_raw_scad_source`.
  ```python
  cache_dir = params.get("cache_dir", None)
  if source:
      filename = _write_raw_scad_source(source, module_name, cache_dir=cache_dir)
  ```

---

## No changes needed
- `working.py` — unchanged
- `opsc_make_object` call sites — unchanged (new param is optional with default)
