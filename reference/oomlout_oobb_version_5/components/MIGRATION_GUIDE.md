# Component Migration Guide

How to move a legacy shape function from `old/oobb_get_items_base_old.py` (or
similar) into the `components/` system so it is auto-discovered by `oobb.py`'s
`_get_shape_lookup()` and appears in the generated documentation.

---

## Quick Start

1. Copy `components/_example_shell/working.py` into a new folder:
   ```
   components/<shape_name>/working.py
   ```
2. Fill in `describe()`, then translate the legacy function body into `action()`.
3. Run the smoke-test command below to confirm it loads.

That's it — no registration step needed. The shape is live immediately.

---

## Folder & File Conventions

| Rule | Detail |
|------|--------|
| Folder name = shape name | `components/oobb_hole/` → shape `"oobb_hole"` |
| One file per component | `working.py` only |
| Underscore prefix = not auto-registered | `_example_shell` is skipped by discovery |
| Extra aliases via `shape_aliases` | list extra strings callers can use as `shape=` |

---

## Anatomy of `working.py`

```python
import copy, os, sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import oobb   # geometry helpers, gv() variable lookup
import opsc   # low-level OpenSCAD primitive builder

d = {}

def describe():
    """Fill d with metadata. Called once; cached in the module global d."""
    global d
    d = {}
    d["name"]          = 'shape_name'
    d["name_long"]     = 'Category: Human Name'
    d["description"]   = 'One sentence.'
    d["category"]      = 'OOBB Geometry Primitives'  # see categories below
    d["shape_aliases"] = ['alias1', 'alias2']         # extra shape= names
    d["returns"]       = 'List of geometry component dicts.'
    v = []
    v.append({"name": "pos",   "description": "...", "type": "list",   "default": "[0,0,0]"})
    v.append({"name": "depth", "description": "...", "type": "number", "default": 10})
    d["variables"] = v
    return d

def define():
    global d
    if not isinstance(d, dict) or not d:
        describe()
    out = {}
    out.update(d)
    return out

def action(**kwargs):
    """The geometry builder. Must return a list of dicts."""
    ...
    return return_value   # always a list
```

### Categories in use

| Category string | Use for |
|-----------------|---------|
| `OOBB Geometry Primitives` | basic shapes — cylinders, cubes, holes |
| `OOBB Geometry Helpers` | combinators — hole arrays, rotation wrappers |
| `Fasteners` | screws, nuts, bolts |
| `Gridfinity` | gridfinity-system tiles |
| `OOBB Mechanical` | couplers, flanges, bearings |

---

## Translating a Legacy Function

### Typical pattern

```python
# OLD (oobb_get_items_base_old.py)
def get_oobb_foo(**kwargs):
    objects = []
    for mode in ["laser", "3dpr", "true"]:
        kwargs["inclusion"] = mode
        kwargs["r"] = ob.gv("hole_radius_m3", mode)
        kwargs["shape"] = "cylinder"
        objects.append(opsc.opsc_easy(**kwargs))
    return objects

# NEW (components/oobb_foo/working.py  →  action())
def action(**kwargs):
    return_value = []
    for mode in ["laser", "3dpr", "true"]:
        p = copy.deepcopy(kwargs)   # always deepcopy before mutating
        p["inclusion"] = mode
        p["r"]         = oobb.gv("hole_radius_m3", mode)
        p["shape"]     = "cylinder"
        return_value.append(opsc.opsc_easy(**p))
    return return_value
```

### Key differences from legacy code

| Legacy | Component |
|--------|-----------|
| `ob.gv(...)` | `oobb.gv(...)` |
| `ob.oobb_easy(...)` | `oobb.oobb_easy(...)` |
| `ob.oobb_easy_array(...)` | `oobb.oobb_easy_array(...)` |
| Mutates `kwargs` in-place | Always `copy.deepcopy(kwargs)` before mutating |
| Returns list or single dict | Must always return a **list** |
| `import oobb_base as ob` | `import oobb` at top level |

### Cross-component dependencies

If your component needs to call another component's `action()`:

```python
import importlib.util

def _load_component(folder_name):
    path = os.path.join(_PROJECT_ROOT, "components", folder_name, "working.py")
    spec = importlib.util.spec_from_file_location(f"comp_{folder_name}", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_rot_mod = _load_component("oobb_rot")
get_rot  = _rot_mod.action
```

### `both_holes` / oobe variants

When you need half-grid (oobe) holes inline, implement a private `_get_oobe_*`
helper inside the same `working.py` rather than importing from the legacy file.
See `components/oobb_holes/working.py` for a complete example.

---

## Smoke Test

After creating the file, verify discovery and a basic call:

```powershell
.venv\Scripts\python.exe -c "
import sys; sys.path.insert(0, '.')
import oobb
lu = oobb._get_shape_lookup()
print('shape_name in lookup:', 'shape_name' in lu)
result = lu['shape_name'](pos=[0,0,0])
print('items returned:', len(result))
"
```

---

## Common Pitfalls

- **Import at module level** — `import oobb` runs at load time. Keep heavy logic
  inside `action()` or helper functions, never at module scope.
- **Mutable default arguments** — never use `def action(holes=["all"], ...)`.
  Use `kwargs.get("holes", ["all"])` instead.
- **Forgetting deepcopy** — mutating `kwargs` directly causes subtle bugs when
  the caller reuses it. Always `p = copy.deepcopy(kwargs)` before setting keys.
- **Returning a dict instead of a list** — `_call_shape_action` in `oobb.py`
  handles a single dict, but returning a list is the expected contract.
- **shape_aliases collision** — check existing components first with:
  ```powershell
  .venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'.'); import oobb; print(sorted(oobb._get_shape_lookup().keys()))"
  ```
