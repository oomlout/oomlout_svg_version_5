# OOBB Object-Per-Folder Migration — 10 Step Execution Plan

> **Master plan:** `restructure/object_per_folder_plan.md`
> **Contract:** No step may be marked complete until ALL listed tests pass.
> Test gate command: `python -m unittest discover -s tests -p "test_*.py"`

---

## Step 1 — Object Discovery Runtime

**Goal:** Build the `discover_objects()` and `build_object_lookup()` functions in `oobb_arch/catalog/object_discovery.py`, mirroring the existing `discover_part_sets()` but for the `part_calls/objects/*/working.py` contract (`define()` + `action()` + `test()`).

**Deliverables:**
1. `oobb_arch/catalog/object_discovery.py` with:
   - `DiscoveredObject` dataclass (name, path, metadata, action_fn, test_fn, aliases)
   - `resolve_objects_root()` → defaults to `part_calls/objects`
   - `discover_objects(objects_root)` → scans `*/working.py`, validates `define()`, `action()`, `test()` callables
   - `build_object_lookup(objects_root)` → discover + add alias entries from `name_short`
2. Update `oobb_arch/catalog/__init__.py` to export new functions
3. `tests/test_object_discovery.py` with tests:
   - `test_discover_objects_contract` — temp folder with valid working.py is discovered
   - `test_discover_objects_skips_invalid` — folder missing action() is skipped
   - `test_build_object_lookup_aliases` — name_short aliases resolve correctly
   - `test_discover_objects_empty_dir` — empty root returns empty dict

**Test contract:**
```
python -m unittest tests.test_object_discovery -v
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery -v
```
ALL must pass before proceeding to Step 2.

**Acceptance criteria:**
- [ ] `discover_objects()` loads a valid `working.py` with `define()/action()/test()`
- [ ] Invalid folders (missing callables) are skipped with a warning, not an error
- [ ] Aliases from `name_short` are added to lookup
- [ ] All pre-existing tests still pass

---

## Step 2 — First Object Working.py Files (3 objects)

**Goal:** Create the first three `part_calls/objects/*/working.py` files — one from each source module to prove all three legacy pathways work.

**Deliverables:**
1. `part_calls/objects/oobb_object_circle/working.py` — wraps `oobb_get_items_oobb.get_circle()`
2. `part_calls/objects/oobb_object_bolt/working.py` — wraps `oobb_get_items_other.get_bolt()`
3. `part_calls/objects/oobb_object_test_gear/working.py` — wraps `oobb_get_items_test.get_test_gear()`
4. Each file follows the full contract: `define()` with rich metadata (name, name_short, name_long, description, category, variables list with name/description/type/default), `action(**kwargs)` delegating to legacy, `test(**kwargs)` with smoke check
5. `tests/test_object_working_files.py` with:
   - `test_circle_define_metadata` — verify define() returns dict with required keys
   - `test_bolt_define_metadata`
   - `test_test_gear_define_metadata`
   - `test_circle_discovered` — verify discovered by `discover_objects()`
   - `test_bolt_discovered` — verify discovered
   - `test_test_gear_discovered` — verify discovered
   - `test_circle_alias_dispatch` — "circle" alias resolves to `oobb_object_circle`

**Test contract:**
```
python -m unittest tests.test_object_discovery tests.test_object_working_files -v
python -m unittest tests.test_architecture_scaffold tests.test_part_set_discovery -v
```
ALL must pass before proceeding to Step 3.

**Acceptance criteria:**
- [ ] Three working.py files exist with complete define() metadata
- [ ] Each file's action() calls the correct legacy function
- [ ] Each file's test() returns True
- [ ] discovery finds all three
- [ ] Alias dispatch works ("circle" → oobb_object_circle)

---

## Step 3 — Wire Object Discovery into oobb_base Dispatch

**Goal:** Update `oobb_base.get_thing_from_dict()` to check discovered objects before falling back to legacy module `getattr` chains.

**Deliverables:**
1. Modify `oobb_base.py`:
   - Import `build_object_lookup` from `oobb_arch.catalog.object_discovery` (with try/except safety)
   - Add `_OBJECT_LOOKUP` cache + `_get_object_lookup()` lazy initializer
   - In `get_thing_from_dict()`: try `_get_object_lookup().get(thing_dict["type"])` first, then existing legacy chain
2. `tests/test_object_dispatch_integration.py` with:
   - `test_dispatch_prefers_discovered` — discovered object takes precedence
   - `test_dispatch_falls_back_to_legacy` — unknown type still resolves via legacy
   - `test_dispatch_circle_via_discovery` — real circle type resolves through discovered working.py
3. Verify existing `tests/test_file_generation.py` snapshot tests still pass (no behavior change for any existing type)

**Test contract:**
```
python -m unittest tests.test_object_dispatch_integration -v
python -m unittest tests.test_object_discovery tests.test_object_working_files -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests.test_dump_json_and_load_json_round_trip -v
```
ALL must pass before proceeding to Step 4.

**Acceptance criteria:**
- [ ] `get_thing_from_dict({"type": "circle", ...})` routes through discovery
- [ ] `get_thing_from_dict({"type": "plate", ...})` still works via legacy (not yet migrated)
- [ ] Snapshot/capability tests unchanged
- [ ] try/except guard means missing `oobb_arch` doesn't break anything

---

## Step 4 — Documentation Data Model & JSON Export

**Goal:** Build the documentation generation system that collects `define()` metadata from all discovered objects and part sets, and exports structured JSON.

**Deliverables:**
1. `part_calls/documentation.py` with:
   - `get_all_objects_documentation(objects_root=None) -> list[dict]` — mirrors roboclick's `get_all_actions_documentation()`
   - `get_all_part_sets_documentation(sets_root=None) -> list[dict]`
   - `export_documentation_json(output_file, objects_root=None, sets_root=None)` — writes `documentation_data.json`
   - Helper functions: `_build_summary()`, `_extract_variable_names()`, `_coerce_text()`
2. `tests/test_documentation_generation.py` with:
   - `test_get_all_objects_documentation_returns_list` — non-empty list of dicts
   - `test_object_doc_entry_has_required_keys` — each entry has command, name_long, description, variables, category
   - `test_get_all_part_sets_documentation_returns_list`
   - `test_export_json_creates_file` — writes valid JSON with expected top-level keys
   - `test_documentation_variable_structure` — each variable has name, description, type, default

**Test contract:**
```
python -m unittest tests.test_documentation_generation -v
python -m unittest tests.test_object_discovery tests.test_object_working_files tests.test_object_dispatch_integration -v
```
ALL must pass before proceeding to Step 5.

**Acceptance criteria:**
- [ ] JSON output contains both "objects" and "part_sets" arrays
- [ ] Every discovered object/set appears in documentation
- [ ] Variable metadata is structured (name, description, type, default)
- [ ] Summary is auto-generated from description or variable names

---

## Step 5 — Documentation HTML & Markdown Export

**Goal:** Create the HTML documentation template and markdown README auto-generation.

**Deliverables:**
1. `templates/oobb_documentation_template.html` — searchable/filterable page (modeled on roboclick's `documentation_template.html`)
   - Category filter sidebar
   - Search box
   - Card layout showing name, description, variables table
   - Separate sections for Objects and Part Sets
2. Add to `part_calls/documentation.py`:
   - `export_documentation_html(template_file, output_file, objects_root=None, sets_root=None)`
   - `export_documentation_markdown(objects_root=None, sets_root=None)` — generates:
     - `part_calls/objects/README.md` (index of all objects)
     - `part_calls/sets/README.md` (index of all sets)
     - Per-folder `README.md` for each discovered folder
3. CLI entry: `python -m part_calls.documentation --json/--html/--markdown`
4. `tests/test_documentation_generation.py` additions:
   - `test_export_html_creates_file` — writes valid HTML
   - `test_export_markdown_creates_index` — creates README.md files
   - `test_per_folder_readme_generated` — each folder gets a README.md

**Test contract:**
```
python -m unittest tests.test_documentation_generation -v
python -m unittest tests.test_object_discovery tests.test_object_working_files -v
```
ALL must pass before proceeding to Step 6.

**Acceptance criteria:**
- [ ] HTML file is generated and contains embedded JSON data
- [ ] Markdown index files are generated with links to all folders
- [ ] Per-folder README.md contains metadata from define()
- [ ] CLI works: `python -m part_calls.documentation --json ...`

---

## Step 6 — Enhanced Scaffold Generator & Migration Reporter

**Goal:** Upgrade the scaffold generator to support both object and set tiers, and enhance the migration status reporter.

**Deliverables:**
1. Replace `part_calls/generate_set_scaffold.py` with `part_calls/generate_scaffold.py`:
   - `--tier object|set` flag
   - `--name <name>` — folder name
   - `--source-module <module>` — optional, pre-fills `action()` delegation
   - `--source-function <func>` — optional, pre-fills `action()` delegation
   - Generates folder + `working.py` + `README.md` placeholder
   - For objects: analyzes existing `get_<type>` signature to pre-fill variables in define()
2. Enhance `part_calls/report_migration_status.py`:
   - Report on BOTH tiers (objects + sets)
   - Show ✓/✗ for each expected entity
   - Show percentage complete
   - List unexpected/extra discovered entities
3. `tests/test_scaffold_and_status.py` with:
   - `test_scaffold_object_creates_folder` — creates `part_calls/objects/<name>/working.py`
   - `test_scaffold_set_creates_folder` — creates `part_calls/sets/<name>/working.py`
   - `test_scaffold_with_source_module` — generated file contains import
   - `test_status_report_both_tiers` — reports objects and sets counts

**Test contract:**
```
python -m unittest tests.test_scaffold_and_status -v
python -m unittest tests.test_documentation_generation tests.test_object_discovery -v
```
ALL must pass before proceeding to Step 7.

**Acceptance criteria:**
- [ ] `generate_scaffold.py --tier object --name circle` creates correct folder and working.py
- [ ] Generated working.py passes discovery validation
- [ ] Status report shows both object and set migration progress
- [ ] Existing scaffold tests (`test_part_set_scaffold_generator.py`) still pass or are merged

---

## Step 7 — Bulk Object Migration (OOBB core: 10+ objects)

**Goal:** Migrate the core OOBB geometry builders from `oobb_get_items_oobb.py` into `part_calls/objects/*/working.py` using the scaffold generator where possible.

**Objects to migrate:**
1. `oobb_object_circle` (done in Step 2)
2. `oobb_object_gear`
3. `oobb_object_plate`
4. `oobb_object_plate_l`
5. `oobb_object_plate_label`
6. `oobb_object_plate_ninety_degree`
7. `oobb_object_plate_t`
8. `oobb_object_plate_u`
9. `oobb_object_plate_u_double`
10. `oobb_object_pulley_gt2`
11. `oobb_object_wheel`
12. `oobb_object_holder`
13. `oobb_object_other`
14. `oobb_object_tray` (from oobb_get_items_oobb_old via star import)

**Deliverables:**
1. One `working.py` per object with complete `define()` metadata
2. All dispatched through discovery in `get_thing_from_dict()`
3. `tests/test_bulk_object_migration.py`:
   - `test_all_migrated_objects_discovered` — all folders found
   - `test_each_object_test_passes` — run test() for each
   - `test_each_object_has_rich_metadata` — variables list non-empty
   - `test_dispatch_routes_through_discovery` — spot-check 3 types

**Test contract:**
```
python -m unittest tests.test_bulk_object_migration -v
python -m unittest tests.test_object_dispatch_integration tests.test_documentation_generation -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests -v
```
ALL must pass before proceeding to Step 8.

**Acceptance criteria:**
- [ ] 10+ object types live in `part_calls/objects/*/working.py`
- [ ] Each has complete define() metadata with variables
- [ ] `get_thing_from_dict()` routes through discovery for all migrated types
- [ ] Documentation JSON includes all migrated objects
- [ ] Existing snapshot tests still pass

---

## Step 8 — Bulk Object Migration (Other + Test: remaining objects)

**Goal:** Migrate the remaining object types from `oobb_get_items_other.py` and `oobb_get_items_test.py`.

**Objects to migrate from `oobb_get_items_other.py`:**
1. `oobb_object_bolt` (done in Step 2)
2. `oobb_object_nut`
3. `oobb_object_screw_countersunk`
4. `oobb_object_screw_self_tapping`
5. `oobb_object_screw_socket_cap`
6. `oobb_object_standoff`
7. `oobb_object_threaded_insert`
8. `oobb_object_bearing`

**Objects to migrate from `oobb_get_items_test.py`:**
9. `oobb_object_test_gear` (done in Step 2)
10. `oobb_object_test_hole`
11. `oobb_object_test_rotation`
12. `oobb_object_test_motor_tt_01`
13. `oobb_object_test_motor_tt_01_shaft`
14. `oobb_object_test_motor_n20_shaft`
15. `oobb_object_test_oobb_motor_servo_standard_01`
16. `oobb_object_test_oobb_nut`
17. `oobb_object_test_oobb_screw_socket_cap`
18. `oobb_object_test_oobb_screw_countersunk`
19. `oobb_object_test_oobb_screw_self_tapping`
20. `oobb_object_test_oobb_screw`
21. `oobb_object_test_oobb_shape_slot`
22. `oobb_object_test_oobb_wire`

**Plus sub-module objects from:**
- `oobb_get_items_oobb_old.py` (bearing_circle, bearing_plate_shim, bunting_alphabet, etc.)
- `oobb_get_items_oobb_wire.py` (wire_basic, wire_motor, wire_spacer, etc.)
- `oobb_get_items_oobb_holder.py` (holder variants)
- `oobb_get_items_oobb_other.py` (other_bolt_stacker, other_corner_cube, etc.)

**Deliverables:**
1. One `working.py` per object with complete metadata
2. `tests/test_bulk_object_migration.py` updated:
   - `test_all_other_objects_discovered`
   - `test_all_test_objects_discovered`
   - `test_total_migrated_objects_count` — verify expected count

**Test contract:**
```
python -m unittest tests.test_bulk_object_migration -v
python -m unittest tests.test_object_dispatch_integration tests.test_documentation_generation -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests -v
```
ALL must pass before proceeding to Step 9.

**Acceptance criteria:**
- [ ] All object types from all three source modules have working.py files
- [ ] `report_migration_status.py` shows ~100% object coverage
- [ ] Documentation JSON includes all objects with rich metadata
- [ ] No behavior change: all existing tests pass

---

## Step 9 — Bulk Part Set Migration (all remaining sets)

**Goal:** Migrate ALL remaining part-set definitions from `oobb_make_sets.py` into `part_calls/sets/*/working.py`.

**Sets to migrate (22 remaining from the 25 total, 3 already done):**
1. `bearing_plates`
2. `buntings`
3. `circles`
4. `gears`
5. `holders`
6. `jacks`
7. `mounting_plates`
8. `plates`
9. `pulleys`
10. `shaft_couplers`
11. `shafts`
12. `soldering_jigs`
13. `smd_magazines`
14. `tool_holders`
15. `trays`
16. `ziptie_holders`
17. `nuts`
18. `wires`
19. `wheels`
20. `screws`
21. `bearings`
22. `tests`

**Deliverables:**
1. One `part_calls/sets/<name>/working.py` per set with complete metadata
2. Each items() function is a direct lift from the corresponding `get_<name>()` in `oobb_make_sets.py`
3. `oobb_make_sets.py` legacy getters updated to use discovery bridge (like `get_bearing_circles` was)
4. `tests/test_bulk_set_migration.py`:
   - `test_all_sets_discovered` — all 25 sets found
   - `test_each_set_items_returns_list` — each items() returns non-empty list
   - `test_each_set_has_rich_metadata` — variables, description, category
   - `test_make_all_uses_discovery` — make_all() routes through discovery for all sets
5. Documentation JSON updated with all sets

**Test contract:**
```
python -m unittest tests.test_bulk_set_migration -v
python -m unittest tests.test_make_sets_discovery_integration tests.test_documentation_generation -v
python -m unittest tests.test_file_generation.OobbBaseFileGenerationTests -v
```
ALL must pass before proceeding to Step 10.

**Acceptance criteria:**
- [ ] All 25 part sets have working.py files
- [ ] `make_all()` uses discovery for all sets (no legacy fallback needed)
- [ ] Each set's items() returns the same part dicts as the legacy function
- [ ] `report_migration_status.py` shows 100% set coverage
- [ ] All existing tests pass

---

## Step 10 — Per-Folder Test Runner, Final Documentation, & Cleanup

**Goal:** Build the per-folder test runner (like roboclick's `run_tests.py`), generate final documentation, clean up legacy bridges, and verify the complete system.

**Deliverables:**
1. `part_calls/run_tests.py`:
   - Discovers all `working.py` in both `objects/` and `sets/`
   - Runs each `test()` callable, captures output
   - Writes `test_report.md` and `test_results.json`
   - Returns exit code based on pass/fail
2. Run `python -m part_calls.documentation --json --html --markdown` to generate all documentation outputs:
   - `part_calls/documentation_data.json`
   - `part_calls/documentation.html`
   - All README.md files
3. Final cleanup:
   - Verify `oobb_make_sets.py` legacy getters all route through discovery bridge
   - Verify `oobb_base.get_thing_from_dict()` routes through discovery
   - Update `restructure/object_per_folder_plan.md` with completion status
   - Update `.github/copilot-instructions.md` with new directory layout
4. `tests/test_complete_migration.py`:
   - `test_all_objects_discovered` — comprehensive count check
   - `test_all_sets_discovered` — comprehensive count check
   - `test_per_folder_test_runner` — run_tests.py produces report
   - `test_documentation_json_complete` — all entities in JSON
   - `test_documentation_html_exists` — HTML file generated
   - `test_no_legacy_fallback_needed` — make_all runs fully through discovery
   - `test_all_readme_files_generated` — every folder has README.md

**Test contract (FINAL GATE):**
```
python -m unittest discover -s tests -p "test_*.py"
python part_calls/run_tests.py
```
BOTH must pass. This is the final verification that the entire migration is complete.

**Acceptance criteria:**
- [ ] Per-folder test runner works and produces report
- [ ] All documentation outputs generated (JSON, HTML, Markdown)
- [ ] Every object folder has working.py + README.md
- [ ] Every set folder has working.py + README.md
- [ ] Full test suite passes (unittest discover + per-folder runner)
- [ ] Migration status report shows 100% on both tiers
- [ ] copilot-instructions.md updated with new layout
- [ ] Legacy modules still exist but all dispatch goes through discovery

---

## Summary — Verification Gate Contract

| Step | Key Test File(s) | Must Also Pass |
|------|------------------|----------------|
| 1 | `test_object_discovery.py` | `test_architecture_scaffold.py`, `test_part_set_discovery.py` |
| 2 | `test_object_working_files.py` | Step 1 tests |
| 3 | `test_object_dispatch_integration.py` | Step 2 tests, `test_file_generation.py` |
| 4 | `test_documentation_generation.py` | Step 3 tests |
| 5 | `test_documentation_generation.py` (expanded) | Step 4 tests |
| 6 | `test_scaffold_and_status.py` | Step 5 tests |
| 7 | `test_bulk_object_migration.py` | Step 6 tests, `test_file_generation.py` |
| 8 | `test_bulk_object_migration.py` (expanded) | Step 7 tests |
| 9 | `test_bulk_set_migration.py` | Step 8 tests, `test_make_sets_discovery_integration.py` |
| 10 | `test_complete_migration.py` | ALL previous tests, `run_tests.py` |

**The rule is simple: if any test fails, you fix it before moving on.**
