# SCAD Object Generation Migration Plan (working.py discovery model)

## Goal

Migrate part-set definitions from monolithic files (primarily `oobb_make_sets.py`) to a folder-based structure where each set lives in its own directory with a `working.py`, discovered automatically at runtime.

## Compatibility contract

1. Existing entrypoints continue to work:
   - `oobb_make_sets.make_all()`
   - legacy `get_*` functions used by tests/scripts
2. Existing part dict schema remains unchanged (for `oobb_base.get_thing_from_dict()`).
3. Existing output generation/snapshot tests remain valid.
4. Migration is additive and incremental; legacy fallback remains available during transition.

## Target structure

```text
part_calls/
  sets/
    bearing_plates/
      working.py
    bearing_circles/
      working.py
    circles/
      working.py
    ...
```

Each `working.py` exposes:

- `define() -> dict`: metadata (name, description, category, variables)
- `items(size="oobb", **kwargs) -> list[dict]`: returns part dictionaries
- optional `test(**kwargs) -> bool`: module-local smoke check

## Discovery/runtime model

1. Discover all `part_calls/sets/*/working.py` modules.
2. Validate required callables (`define`, `items`).
3. Build lookup by folder name and aliases (`name_short` in metadata).
4. `make_all()` obtains requested set names and calls discovered providers.
5. If a set is not discovered, fallback to legacy `get_<set>()` implementation.

## Auto-generation model

- Provide a script to scaffold new set folders:
  - create folder + `working.py` template
  - inject metadata and placeholder `items()`
- Provide a script to emit migration status report:
  - discovered sets
  - missing expected sets
  - legacy-only sets remaining

## Test strategy

1. Unit tests for discovery contract and lookup behavior.
2. Unit tests for legacy fallback behavior.
3. Unit tests for scaffold generator output.
4. Existing `tests/test_file_generation.py` smoke/capability tests stay green.

## Rollout sequence

- Phase A: introduce discovery framework + tests (no behavior changes)
- Phase B: wire `make_all()` through discovery + fallback
- Phase C: migrate selected sets to `part_calls/sets/*/working.py`
- Phase D: add auto-generation and reporting tooling
- Phase E: continue set-by-set migration until complete
