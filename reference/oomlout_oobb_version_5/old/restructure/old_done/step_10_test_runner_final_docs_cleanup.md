# Step 10 — Per-Folder Test Runner, Final Docs & Cleanup

> **Master plan:** `restructure/object_per_folder_plan.md`  
> **Step index:** `restructure/object_per_folder_steps.md`  
> **Prerequisite:** Steps 7, 8, 9 all complete with all tests passing  
> **Blocks:** None (final step)

---

## Goal

Complete the migration by:

1. **Per-folder test runner**: A script that discovers and runs every `test()` function in every `working.py`
2. **Final documentation**: Generate complete JSON, HTML, and Markdown documentation covering all ~85+ entities
3. **Migration report**: Confirm 100% migration and print final counts
4. **Cleanup checklist**: Document what legacy code can be removed (but don't remove it yet)

---

## Background — The Roboclick Test Runner

Roboclick's `run_tests.py` (442 lines) provides:

```python
@dataclass
class TestCase:
    action_name: str
    status: str  # "PASS" / "FAIL" / "ERROR" / "SKIP"
    message: str
    duration: float

def run_all_tests(actions_root=None) -> list[TestCase]:
    discovered = discover_actions(actions_root)
    results = []
    for name, action in sorted(discovered.items()):
        if action.test_fn is None:
            results.append(TestCase(name, "SKIP", "no test() function", 0.0))
            continue
        start = time.time()
        try:
            passed = action.test_fn()
            status = "PASS" if passed else "FAIL"
            msg = ""
        except Exception as e:
            status = "ERROR"
            msg = str(e)
        results.append(TestCase(name, status, msg, time.time() - start))
    return results
```

The OOBB version will run both object and set tests.

---

## Deliverables

### 1. `part_calls/run_tests.py`

Per-folder test runner that:

```python
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Literal


@dataclass
class TestResult:
    entity_type: Literal["object", "set"]
    name: str
    status: Literal["PASS", "FAIL", "ERROR", "SKIP"]
    message: str
    duration: float


def run_all_object_tests(objects_root=None) -> list[TestResult]:
    """Discover all objects and run their test() functions.
    
    For each discovered object:
    - If test_fn is None → SKIP
    - If test_fn() returns True → PASS
    - If test_fn() returns False → FAIL
    - If test_fn() raises → ERROR with exception message
    """


def run_all_set_tests(sets_root=None) -> list[TestResult]:
    """Discover all sets and run their test() functions.
    
    Same pattern as objects but with discovered sets.
    """


def run_all_tests(objects_root=None, sets_root=None) -> list[TestResult]:
    """Run all object + set tests and return combined results."""
    return run_all_object_tests(objects_root) + run_all_set_tests(sets_root)


def print_test_report(results: list[TestResult]):
    """Print formatted test results.
    
    Output:
    ════════════════════════════════════════════
     OOBB Per-Folder Test Report
    ════════════════════════════════════════════
    
    OBJECTS (60 total)
    ✓ oobb_object_circle         PASS  (0.003s)
    ✓ oobb_object_bolt           PASS  (0.002s)
    ✗ oobb_object_plate          FAIL  (0.015s)
    ⚠ oobb_object_old_1          SKIP  (no test)
    ✗ oobb_object_test_gear      ERROR (0.001s) ValueError: ...
    
    SETS (25 total)
    ✓ circles                    PASS  (0.010s)
    ✓ plates                     PASS  (0.012s)
    ...
    
    ────────────────────────────────────────────
    TOTAL: 85 | PASS: 80 | FAIL: 2 | ERROR: 1 | SKIP: 2
    ────────────────────────────────────────────
    """


def cli():
    """Command-line interface for running tests."""
    import argparse
    parser = argparse.ArgumentParser(description="OOBB Per-Folder Test Runner")
    parser.add_argument("--objects-only", action="store_true")
    parser.add_argument("--sets-only", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", default="", help="Output results as JSON to file")
    args = parser.parse_args()
    
    if args.objects_only:
        results = run_all_object_tests()
    elif args.sets_only:
        results = run_all_set_tests()
    else:
        results = run_all_tests()
    
    print_test_report(results)
    
    if args.json:
        # Export results as JSON
        import json
        with open(args.json, "w") as f:
            json.dump([vars(r) for r in results], f, indent=2)
    
    # Exit with non-zero if any failures
    failures = [r for r in results if r.status in ("FAIL", "ERROR")]
    return len(failures)


if __name__ == "__main__":
    import sys
    sys.exit(cli())
```

### 2. Final Documentation Generation

Run the documentation system from Step 5 to produce the complete output:

```powershell
# Generate all documentation
python part_calls/documentation.py --json part_calls/documentation_data.json --html-template templates/oobb_documentation_template.html --html-output part_calls/documentation.html --markdown
```

This should produce:
- `part_calls/documentation_data.json` — ~8000+ lines covering all ~85 entities
- `part_calls/documentation.html` — searchable HTML page
- `part_calls/objects/README.md` — index of all objects
- `part_calls/sets/README.md` — index of all sets
- Per-folder `README.md` for each entity

### 3. Final Migration Report

```powershell
python -c "from oobb_arch.catalog.migration_status import print_migration_report; print_migration_report()"
```

Expected output:
```
════════════════════════════════════════════
 OOBB Migration Status Report
════════════════════════════════════════════

OBJECTS: 60+ / 60+ migrated (100.0%)
✓ circle, gear, plate, bolt, nut, ...

SETS: 25 / 25 migrated (100.0%)
✓ circles, gears, plates, holders, ...
```

### 4. Cleanup Checklist Document

Create `restructure/cleanup_checklist.md`:

```markdown
# Post-Migration Cleanup Checklist

These items can be addressed AFTER the migration is verified stable.
Do NOT execute these during the migration.

## Safe to Archive (not delete — move to archive/)
- [ ] oobb_get_items_oobb.py → all functions now in per-folder working.py
- [ ] oobb_get_items_oobb_old.py → same
- [ ] oobb_get_items_oobb_wire.py → same
- [ ] oobb_get_items_oobb_holder.py → same
- [ ] oobb_get_items_oobb_other.py → same
- [ ] oobb_get_items_oobb_bearing_plate.py → same
- [ ] oobb_get_items_other.py → same
- [ ] oobb_get_items_test.py → same
- [ ] oobb_get_items_test_old.py → same
- [ ] oobb_get_items_base_old.py → same
- [ ] oobb_make_sets_old.py → same

## Keep as-is (still referenced by legacy flows)
- [ ] oobb_base.py — dispatch hub, still needed
- [ ] oobb_make_sets.py — make_all() still the entry point
- [ ] oobb_get_item_common.py — utility functions used by builders
- [ ] oobb_variables.py — shared constants
- [ ] oobb.py — star import hub (needed until builders are self-contained)

## Can be simplified once migration is stable
- [ ] oobb_base.get_thing_from_dict() — remove legacy getattr chain, keep only discovery
- [ ] oobb_make_sets.make_all() — simplify to only use discover_part_sets()
- [ ] Legacy builder registry — remove once all objects use discovery

## Documentation outputs to commit
- [ ] part_calls/documentation_data.json
- [ ] part_calls/documentation.html
- [ ] part_calls/objects/README.md
- [ ] part_calls/sets/README.md
- [ ] Per-folder README.md files
```

---

## Tests

### `tests/test_per_folder_test_runner.py`

Four test cases:

#### `test_run_all_object_tests_returns_results`
- Call `run_all_object_tests()` with real objects root
- Assert return is a list of `TestResult`
- Assert at least one result exists
- Assert all results have `entity_type == "object"`

#### `test_run_all_set_tests_returns_results`
- Call `run_all_set_tests()` with real sets root
- Assert return is a list of `TestResult`
- Assert at least one result exists
- Assert all results have `entity_type == "set"`

#### `test_run_all_tests_combined`
- Call `run_all_tests()`
- Assert both object and set results are present
- Assert total count ≥ 85

#### `test_skip_result_for_missing_test_fn`
- Create a temp `working.py` with `define()` and `action()` but NO `test()`
- Run tests against this temp directory
- Assert the result for this entity has `status == "SKIP"`

### `tests/test_final_migration_complete.py`

Three final gate tests:

#### `test_100_percent_object_migration`
- Call `get_migration_status()`
- Assert `objects["percentage"] == 100.0`

#### `test_100_percent_set_migration`
- Call `get_migration_status()`
- Assert `sets["percentage"] == 100.0`

#### `test_documentation_json_covers_all_entities`
- Generate `documentation_data.json` to temp file
- Load and parse
- Assert `total_objects` ≥ 60
- Assert `total_part_sets` ≥ 25
- Assert every discovered object name appears in the JSON
- Assert every discovered set name appears in the JSON

---

## Files Created/Modified

| File | Change |
|------|--------|
| `part_calls/run_tests.py` | **NEW** — per-folder test runner |
| `restructure/cleanup_checklist.md` | **NEW** — post-migration cleanup guide |
| `part_calls/documentation_data.json` | **GENERATED** — complete JSON docs |
| `part_calls/documentation.html` | **GENERATED** — searchable HTML docs |
| `part_calls/objects/README.md` | **GENERATED** — object index |
| `part_calls/sets/README.md` | **GENERATED** — set index |
| `part_calls/objects/*/README.md` | **GENERATED** — per-object README |
| `part_calls/sets/*/README.md` | **GENERATED** — per-set README |
| `tests/test_per_folder_test_runner.py` | **NEW** — 4 tests |
| `tests/test_final_migration_complete.py` | **NEW** — 3 final gate tests |

---

## Test Contract

**ALL tests across the entire test suite must pass:**

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Additionally, run the per-folder test runner:

```powershell
python part_calls/run_tests.py
```

---

## Acceptance Criteria

- [ ] `part_calls/run_tests.py` discovers and runs all object + set `test()` functions
- [ ] Test runner produces formatted output with PASS/FAIL/ERROR/SKIP counts
- [ ] Test runner exits with non-zero if any failures
- [ ] `documentation_data.json` covers all ~85+ entities
- [ ] `documentation.html` is a functional searchable page
- [ ] All per-folder `README.md` files are generated
- [ ] Object and set indexes (`README.md`) list all entities with descriptions
- [ ] `get_migration_status()` reports 100% for both objects and sets
- [ ] `cleanup_checklist.md` documents what can be archived vs. kept
- [ ] All 7 new tests pass
- [ ] **All tests across the entire test suite pass (zero regressions)**

---

## Final Verification Gate

After Step 10, run this complete validation:

```powershell
# 1. All unit tests pass
python -m unittest discover -s tests -p "test_*.py" -v

# 2. Per-folder test runner passes
python part_calls/run_tests.py

# 3. Migration is 100% complete
python -c "from oobb_arch.catalog.migration_status import print_migration_report; print_migration_report()"

# 4. Documentation is generated
python part_calls/documentation.py --json part_calls/documentation_data.json --markdown

# 5. Snapshot/capability tests still match (most important)
python -m unittest tests.test_file_generation -v
```

---

## Summary — Full Migration Complete

After all 10 steps, the project will have:

| Metric | Count |
|--------|-------|
| Object folders (`part_calls/objects/oobb_object_*/`) | ~60+ |
| Set folders (`part_calls/sets/*/`) | ~25 |
| Total `working.py` files | ~85+ |
| Unit tests (unittest) | ~50+ |
| Per-folder tests (test() functions) | ~85+ |
| Documentation entries (JSON) | ~85+ |

**Architecture summary:**
```
part_calls/
├── objects/
│   ├── README.md                    (auto-generated index)
│   ├── oobb_object_circle/
│   │   ├── working.py               (define + action + test)
│   │   └── README.md                (auto-generated docs)
│   ├── oobb_object_plate/
│   │   ├── working.py
│   │   └── README.md
│   └── ... (60+ folders)
├── sets/
│   ├── README.md                    (auto-generated index)
│   ├── circles/
│   │   ├── working.py               (define + items + test)
│   │   └── README.md
│   └── ... (25 folders)
├── documentation.py                 (JSON/HTML/Markdown generator)
├── documentation_data.json          (generated)
├── documentation.html               (generated)
└── run_tests.py                     (per-folder test runner)
```

---

## Estimated Scope

- ~120 lines in `run_tests.py`
- ~40 lines in `cleanup_checklist.md`
- ~50 lines in `test_per_folder_test_runner.py`
- ~40 lines in `test_final_migration_complete.py`
- Generated docs: ~8000+ lines JSON, ~500+ lines HTML, ~2000+ lines Markdown
- No changes to any existing production code
