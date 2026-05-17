# Code Migration: 10-Step Execution Plan

## Overview

Migrate all geometry code from legacy monolith modules (`oobb_get_items_*.py`) into
folder-based `part_calls/objects/*/working.py` files with verified output equivalence.

**Rule:** Each step's tests must pass before proceeding to the next step. Do NOT review diffs or monitor file changes between steps — just run the tests and move on.

---

## Step Index

| Step | Title | New Tests | Key Deliverable |
|------|-------|-----------|-----------------|
| [01](step_01_output_comparison_harness.md) | Output Comparison Harness | 6 | `oobb_arch/testing/` — reusable comparison + forwarder-check utilities |
| [02](step_02_shared_helpers_extraction.md) | Shared Helpers Extraction | 5 | `oobb_arch/helpers/` — `plate_helpers`, `shaft_helpers` |
| [03](step_03_migrate_other_leaf_objects.md) | Migrate `oobb_get_items_other` | 10 | 8 hardware objects (bolt, nut, screw, bearing) own their code |
| [04](step_04_migrate_test_leaf_objects.md) | Migrate `oobb_get_items_test` | 6 | 15 test objects own their code |
| [05](step_05_migrate_core_leaf_geometry.md) | Migrate Core Leaf Geometry | 7 | `circle_base`, `plate_base`, `plate_ninety_degree`, `plate_label` own code |
| [06](step_06_migrate_composite_plates.md) | Migrate Composite Plates | 6 | `plate_l`, `plate_t`, `plate_u`, `plate_u_double` own code |
| [07](step_07_migrate_gear_pulley.md) | Migrate Gear & Pulley | 8 | `gear`, `gear_double_stack`, `pulley_gt2`, `pulley_gt2_shield_double` own code |
| [08](step_08_migrate_router_functions.md) | Migrate Router Functions | 10 | `circle`, `plate`, `holder`, `other`, `test`, `wheel`, `wire` use clean dispatch |
| [09](step_09_migrate_oobb_old_bulk.md) | Migrate `oobb_old` + Satellites | 10 | ~137 functions from 7 modules moved into folders |
| [10](step_10_cleanup_and_archive.md) | Cleanup & Archive | 6+ | Discovery-only dispatch, legacy archived, all aliases active |

**Total new tests across all steps: ~74**

---

## Dependency Graph

```
Step 01 (harness)
  └─ Step 02 (helpers)
       └─ Step 03 (other.py leaves)      ← can run in parallel with 04
       └─ Step 04 (test.py leaves)       ← can run in parallel with 03
            └─ Step 05 (core leaves: circle_base, plate_base, ...)
                 └─ Step 06 (composite plates: plate_l, plate_t, ...)
                 └─ Step 07 (gear + pulley)
                      └─ Step 08 (routers: circle, plate, holder, ...)
                           └─ Step 09 (bulk: oobb_old + satellites)
                                └─ Step 10 (cleanup + archive)
```

---

## Test Gate

After each step, run:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

**The step is COMPLETE only when:**
1. All pre-existing tests still pass (zero regressions)
2. All new tests from the step pass
3. The legacy module functions still work (via forwarders)
4. `oobb_base.get_thing_from_dict()` dispatch produces identical output

**Do NOT** review diffs, scan for changed files, or enumerate modifications between steps. Just run the tests and proceed.

---

## Cumulative Progress (Reference)

Expected migration status after each step:

| After Step | Functions in Folders | Functions as Forwarders | Legacy Getattr Used? |
|------------|---------------------|------------------------|---------------------|
| 01 | 0 (wrappers only) | 0 | Yes |
| 02 | 0 (helpers extracted) | 0 | Yes |
| 03 | 8 | 8 in `oobb_get_items_other.py` | Yes |
| 04 | 23 | + 15 in `oobb_get_items_test.py` | Yes |
| 05 | 27 | + 4 in `oobb_get_items_oobb.py` | Yes |
| 06 | 31 | + 4 in `oobb_get_items_oobb.py` | Yes |
| 07 | 35 | + 4 in `oobb_get_items_oobb.py` | Yes |
| 08 | 41 | + 6 in `oobb_get_items_oobb.py` | Yes (for unmigrated) |
| 09 | ~178 | + ~137 across 7 modules | No (all migrated) |
| 10 | ~178 | archived | **No — discovery only** |

---

## Key Principles (enforced at every step)

1. **Always leave a forwarder** — never delete a legacy function, replace its body
2. **Output comparison** — folder output must match legacy output exactly
3. **Cross-object calls go through dispatch** — `oobb_base.get_thing_from_dict()`, never direct imports
4. **One function per commit** within each step for easy bisect
5. **No star-import breakage** — forwarders keep re-exported names available
6. **Aliases activate when descriptions are enriched** — remove "Auto-generated scaffold"
