# Code Migration Strategy: Legacy Monolith → Folder-Based Architecture

## Current State (Where We Are)

### What exists today

```
Caller (oobb_make_sets.py)
  └─ builds thing_dict:  {"type": "circle", "diameter": 3, ...}
       └─ oobb_base.get_thing_from_dict(thing_dict)
            ├─ 1. Discovery lookup  → folder working.py action()  → calls back to legacy module
            ├─ 2. Legacy registry   → oobb_get_items_oobb.get_circle()
            └─ 3. Legacy getattr    → getattr(oobb_get_items_oobb, "get_circle")
```

The folder-based `working.py` files are **thin wrappers** that delegate back to legacy:

```python
# part_calls/objects/oobb_object_circle/working.py
def action(**kwargs):
    import oobb_get_items_oobb
    return oobb_get_items_oobb.get_circle(**kwargs)   # ← all code still lives in the monolith
```

The actual geometry logic (~5,000+ lines) still lives in:
- `oobb_get_items_oobb.py` (1,490 lines — plates, circles, gears, pulleys, wheels, wires)
- `oobb_get_items_oobb_old.py` (4,912 lines — bearing circles, holders, mounting plates, jigs, etc.)
- `oobb_get_items_oobb_holder.py` (828 lines — motor/electronic holders)
- `oobb_get_items_oobb_holder_electronic.py`
- `oobb_get_items_oobb_bearing_plate.py`
- `oobb_get_items_oobb_wire.py`
- `oobb_get_items_oobb_other.py`
- `oobb_get_items_oobb_wheel.py`
- `oobb_get_items_other.py`
- `oobb_get_items_test.py`

### Call patterns that must be preserved

| Pattern | Example | Frequency |
|---------|---------|-----------|
| **Top-level dispatch** | `oobb_base.get_thing_from_dict({"type":"circle",...})` | ~20 call sites |
| **Internal sub-dispatch** | `get_plate()` calling `get_plate_base()` or `get_plate_l()` via `getattr` | ~10 sites |
| **Cross-module delegation** | `get_holder()` → `oobb_get_items_oobb_holder.get_holder_*()` | ~15 sites |
| **Internal composition** | `get_gear_double_stack()` calling `oobb_base.get_thing_from_dict(p3)` to compose sub-parts | ~12 sites |
| **Helper calls** | `oobb_get_items_oobb_wire` calling `oobb_get_items_oobb.get_plate_dict()` | ~5 sites |
| **Star imports** | `oobb_get_items_oobb.py` does `from oobb_get_items_oobb_old import *` | 3 files |

---

## Target State (Where We Want To Be)

```
Caller
  └─ {"type": "circle", "diameter": 3, ...}
       └─ oobb_base.get_thing_from_dict(thing_dict)
            └─ Discovery lookup only
                 └─ part_calls/objects/oobb_object_circle/working.py
                      └─ action(**kwargs)  ← OWNS the geometry code
                           └─ calls shared helpers OR other object folders
```

Each folder's `working.py` **owns its geometry code** rather than delegating to the legacy monolith.

When one object needs another (e.g., `gear_double_stack` composes `circle`), it calls through dispatch:
```python
# part_calls/objects/oobb_object_gear_double_stack/working.py
def action(**kwargs):
    import oobb_base
    # compose sub-parts through the standard dispatch
    sub_thing = oobb_base.get_thing_from_dict({"type": "circle", ...})
```

---

## Migration Strategy: 4 Phases

### Phase 1 — Shared Helpers Extraction (Low Risk)

**Goal:** Pull out utility functions that are used across multiple object types into a shared helpers module, so individual folders can import them directly without depending on the monolith.

**What to extract into `oobb_arch/helpers/`:**
```
oobb_arch/
  helpers/
    __init__.py
    plate_helpers.py      ← get_plate_dict(), get_plate_hole_dict()
    component_helpers.py  ← common component-building patterns
```

**Why first:** These are pure utility functions with no dispatch logic. Moving them is risk-free and removes the #1 reason folders need to import the monolith.

**Steps:**
1. Identify all "helper" functions (non-`get_*` or used only as utilities)
2. Copy them into `oobb_arch/helpers/`
3. Update the legacy modules to import from the new location (backward compat)
4. Update folder `working.py` files to import from `oobb_arch/helpers/` instead

**Test gate:** Full test suite still passes; legacy modules still work. Do not review diffs between phases.

---

### Phase 2 — Leaf Objects First (Bottom-Up, No Internal Dependencies)

**Goal:** Move actual geometry code into folder `working.py` for objects that don't call other `get_*` functions internally.

**These are "leaf" objects — they only use `oobb_base` utilities, not other object builders:**

Priority candidates (in `oobb_get_items_oobb.py`):
- `get_circle_base()` — standalone geometry builder
- `get_plate_base()` — standalone geometry builder
- `get_plate_label()` — standalone
- `get_plate_ninety_degree()` — standalone
- `get_plate_l()`, `get_plate_t()`, `get_plate_u()`, `get_plate_u_double()` — each builds from `oobb_base` helpers, sometimes composes via `get_thing_from_dict`
- `get_pulley_gt2()`, `get_pulley_gt2_shield_double()` — standalone
- `get_wheel()`, `get_wire()`, `get_test()` — standalone

In `oobb_get_items_other.py`:
- `get_bolt()`, `get_nut()`, `get_screw_*()`, `get_bearing()` — standalone

In `oobb_get_items_test.py`:
- `get_test_gear()` etc. — standalone

**Migration pattern per function:**

```python
# BEFORE: part_calls/objects/oobb_object_circle_base/working.py
def action(**kwargs):
    import oobb_get_items_oobb
    return oobb_get_items_oobb.get_circle_base(**kwargs)

# AFTER: part_calls/objects/oobb_object_circle_base/working.py
def action(**kwargs):
    import copy
    import oobb_base
    # ... actual geometry code moved here from oobb_get_items_oobb.get_circle_base() ...
```

**And in the legacy module, replace the original with a forwarder:**
```python
# oobb_get_items_oobb.py — AFTER migration
def get_circle_base(**kwargs):
    # MIGRATED: code now lives in part_calls/objects/oobb_object_circle_base/
    from part_calls.objects.oobb_object_circle_base.working import action
    return action(**kwargs)
```

**Why forwarders?** Other legacy code that calls `get_circle_base()` directly (via star imports or explicit calls) keeps working. Zero breakage.

**Test gate:** Per-object smoke test passes; full suite passes; outputs are identical. Do not review diffs between phases.

---

### Phase 3 — Router Objects (Top-Down Dispatch Wrappers)

**Goal:** Migrate the "router" functions — `get_circle()`, `get_plate()`, `get_holder()`, `get_other()` — that dispatch to sub-functions based on `extra`.

These are the trickiest because they use `getattr` patterns:
```python
def get_circle(**kwargs):
    extra = kwargs.get("extra", "")
    if extra != "":
        function_to_call = getattr(sys.modules[__name__], "get_plate_" + extra)
        return function_to_call(**kwargs)
    else:
        return get_circle_base(**kwargs)
```

**Migration approach — replace `getattr` with dispatch-through-discovery:**
```python
# part_calls/objects/oobb_object_circle/working.py — AFTER
def action(**kwargs):
    import copy
    import oobb_base
    
    p3 = copy.deepcopy(kwargs)
    extra = p3.get("extra", "")
    
    if extra != "" and "doughnut" not in extra:
        # Sub-dispatch through the standard system
        p3["type"] = f"plate_{extra}"
        return oobb_base.get_thing_from_dict(p3)
    else:
        # Delegate to circle_base
        return oobb_base.get_thing_from_dict({**p3, "type": "circle_base"})
```

This is cleaner because:
- No `getattr` / `importlib.reload` hacks
- Sub-types route through the standard dispatch (which will find them in their own folders)
- Adding new sub-types just means adding a new folder

**Test gate:** All circle/plate/holder/other variants produce identical output. Do not review diffs between phases.

---

### Phase 4 — Cleanup and Legacy Removal

**Goal:** Once all code lives in folders, slim down the legacy monolith modules.

**Steps:**
1. Legacy modules become pure forwarder files (each `get_*` just calls the folder's `action()`)
2. Remove the legacy `getattr` fallback from `oobb_base.get_thing_from_dict()`
3. Remove the legacy registry layer
4. Optionally archive the old files to `legacy/` for reference

**Final dispatch chain:**
```
oobb_base.get_thing_from_dict()
  └─ Discovery lookup only → folder working.py action()
```

---

## Migration Order Within Phase 2 (Recommended)

Start with the simplest, most isolated functions. Each one is a self-contained PR/commit:

| Wave | Functions | Source Module | Complexity |
|------|-----------|---------------|------------|
| 1 | `get_test()` | `oobb_get_items_oobb` | Trivial |
| 2 | `get_bolt()`, `get_nut()`, `get_screw_*()`, `get_bearing()` | `oobb_get_items_other` | Simple |
| 3 | `get_circle_base()`, `get_plate_base()` | `oobb_get_items_oobb` | Medium (core geometry) |
| 4 | `get_plate_label()`, `get_plate_ninety_degree()` | `oobb_get_items_oobb` | Medium |
| 5 | `get_plate_l()`, `get_plate_t()`, `get_plate_u()`, `get_plate_u_double()` | `oobb_get_items_oobb` | Medium (compose via dispatch) |
| 6 | `get_pulley_gt2()`, `get_pulley_gt2_shield_double()` | `oobb_get_items_oobb` | Medium-High |
| 7 | `get_wheel()`, `get_wire()` | `oobb_get_items_oobb` | Medium |
| 8 | `oobb_get_items_oobb_old.py` functions (bearing_circle, holders, jigs, etc.) | `oobb_get_items_oobb_old` | High (~4,900 lines) |

---

## Key Principles

### 1. Always Leave a Forwarder
When moving code out of a legacy module, replace the original function body with a one-line forwarder. This ensures all existing callers (including star imports, internal calls, and external scripts) keep working.

### 2. One Function Per Commit
Each function migration is a single atomic commit. If something breaks, you can bisect easily.

### 3. Output Comparison Testing
Before migrating a function:
1. Run it via the legacy path, capture the output dict
2. Move the code to the folder
3. Run it via the folder path, compare outputs
4. They must be **identical** (use `json.dumps(result, sort_keys=True)` for deep comparison)

### 4. Cross-Object Calls Go Through Dispatch
When one object needs another, it should call `oobb_base.get_thing_from_dict({"type": "other_type", ...})`, **not** directly import the other folder's `working.py`. This keeps the dispatch system as the single routing point.

### 5. Don't Break Star Imports (Yet)
`oobb_get_items_oobb.py` does `from oobb_get_items_oobb_old import *`. The forwarder pattern keeps this working. Only remove star imports in Phase 4.

### 6. Aliases Activate When Descriptions Are Enriched
Auto-generated scaffolds currently have aliases suppressed (description starts with "Auto-generated scaffold"). When you move real code into a folder and update the description, aliases automatically activate for discovery dispatch.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking production builds | Forwarder pattern ensures zero-downtime migration |
| Circular imports | Lazy imports inside `action()` (already the pattern) |
| `importlib.reload` hacks | Phase 3 replaces these with clean dispatch |
| Star import chains | Forwarders keep them working until Phase 4 |
| 4,900-line `oobb_old` | Migrate function-by-function, not all at once |
| Cross-object composition | Route through `get_thing_from_dict()`, not direct imports |

---

## Quick Reference: What Changes Where

```
Phase 1:  oobb_arch/helpers/          NEW shared utility functions
Phase 2:  part_calls/objects/*/working.py   gets real code (leaf objects)
          oobb_get_items_*.py               get_X() → forwarder to folder
Phase 3:  part_calls/objects/*/working.py   gets router logic (circle, plate, holder)
          oobb_get_items_*.py               router functions → forwarders
Phase 4:  oobb_base.py                     remove legacy fallback chains
          oobb_get_items_*.py               archive to legacy/
```

## Success Criteria

- [ ] All 170 object folders contain their own geometry code (not delegating to legacy)
- [ ] All 25 set folders work through discovery dispatch only
- [ ] `oobb_base.get_thing_from_dict()` has only the discovery lookup (no getattr fallback)
- [ ] Legacy modules are either archived or contain only forwarders
- [ ] Full test suite passes
- [ ] Build output (SCAD files) is byte-for-byte identical to pre-migration
