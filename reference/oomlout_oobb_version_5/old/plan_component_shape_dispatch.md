# Plan: Component-based shape dispatch in `oobb_easy`

## Goal
Replace the `globals()[f'get_{shape}']` lookup with a component-based dispatch that finds `action()` in `components/<name>/working.py`, indexed by both folder name and aliases from `define()["name_short"]`.

## What already exists
- `oobb_arch/catalog/object_discovery.py` already has `build_object_lookup()` that scans `components/*/working.py`, calls `define()`, extracts `name_short` aliases, and returns a `dict[str, DiscoveredObject]` keyed by folder name + aliases, each with an `action_fn`.
- `_get_object_lookup()` in `oobb.py` already lazily builds this lookup (used by `get_thing_from_dict`).

## What needs to change

### 1. Build a *shape-level* component index at startup (new function + global)

The existing `build_object_lookup()` maps names like `"circle_base"` or `"bolt"` — these are *part-level* type names used in `get_thing_from_dict`. But `oobb_easy` dispatches on *shape names* like `"oobb_circle"`, `"oobb_plate"`, `"oobb_screw_countersunk"`. The shape is typically `"oobb_<folder_name>"`.

We need a new index that maps shape names → `action()` from `components/*/working.py`. Each `working.py` can declare shape aliases via `define()["name_short"]` (e.g. `["oobb_circle", "oobb_ci"]`).

Approach:
- Add a new field to `define()` in each component's `working.py`: **`"shape_aliases"`** — a list of shape strings this component handles (e.g., `["oobb_circle"]`). This is separate from `name_short` which is for part-type dispatch.
- New function `_build_shape_lookup()` in `oobb.py`: scans `components/*/working.py`, loads each module, checks for `define()["shape_aliases"]`, and builds a `dict[str, Callable]` mapping shape name → `action()`.
- If `shape_aliases` is not present, fall back to checking `name_short` for backward compatibility.
- Lazy-init global `_SHAPE_LOOKUP`.

### 2. Modify `oobb_easy()` dispatch (line ~902)

Currently:
```python
func = globals()[f'get_{shape}']
```

Becomes:
```python
shape_lookup = _get_shape_lookup()
if shape in shape_lookup:
    return_value_2.append(shape_lookup[shape](**kwargs))
else:
    # legacy fallback: try globals from _ensure_geometry
    func = globals()[f'get_{shape}']
    return_value_2.append(func(**kwargs))
```

This keeps full backward compatibility — any component with a `working.py` that declares shape aliases gets called first; anything else falls through to the existing `oobb_get_items_base` globals.

### 3. Incremental migration path

Each `components/*/working.py` that wants to handle a shape adds `"shape_aliases": ["oobb_circle"]` to its `define()` return value. Once that's there, `oobb_easy` will route to it. The old `get_oobb_circle` in `oobb_get_items_base.py` continues to work as fallback until removed.

## What stays the same
- The `oobb_pl` and `oobe_pl` special cases at lines 888-898 stay as-is (they do multi-step plate+holes logic).
- The `opsc.opsc_easy()` fallback for non-oobb shapes stays as-is.
- `_ensure_geometry()` stays as fallback for shapes not yet migrated to components.
- `get_thing_from_dict` dispatch (for part-level building) is untouched.

## Open questions

1. **Shape alias field name**: Proposal is `"shape_aliases"` in `define()` to keep it distinct from `"name_short"` (which is for part-type dispatch). Or reuse `"name_short"` for both purposes?

2. **The `oobb_pl` / `oobe_pl` special cases** (plate + holes composite): Should those eventually become a component too, or leave them hardcoded for now?

3. **When a shape hits the component `action()`**: Should it receive the same `**kwargs` that `oobb_easy` currently passes (with `shape`, `pos`, `type`, etc.), or should there be any kwargs normalization before calling the component?
