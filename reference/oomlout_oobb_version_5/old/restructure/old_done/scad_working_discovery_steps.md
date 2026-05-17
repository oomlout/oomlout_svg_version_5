# 10 Small Steps: working.py Discovery Migration

Each step is atomic and must pass tests before proceeding.

## Step 1 — Create plan + contracts
- Add migration plan docs and explicit module contract for `working.py`.
- Test gate: documentation-only (no code regression expected).

## Step 2 — Add discovery tests (red/green harness)
- Add tests for discovering `working.py` modules and validating required callables.
- Test gate: new test file passes.

## Step 3 — Add discovery runtime module
- Implement `discover_part_sets()` + lookup builder.
- Keep it unused by production path initially.
- Test gate: discovery tests pass.

## Step 4 — Add initial part_calls directory + sample migrated set modules
- Create `part_calls/sets/.../working.py` for first migrated sets.
- Test gate: discovery sees migrated sets; module contracts pass.

## Step 5 — Wire `oobb_make_sets.make_all()` to discovery (with legacy fallback)
- Preserve output behavior and function signature.
- Test gate: existing smoke test + discovery tests pass.

## Step 6 — Add compatibility bridge for legacy `get_*` calls
- Legacy getters call discovered providers if available.
- Test gate: legacy getter parity tests pass.

## Step 7 — Migrate first real set block from monolith to per-folder working.py
- Move one concrete set implementation from `oobb_make_sets.py` into `part_calls`.
- Keep wrapper in `oobb_make_sets.py`.
- Test gate: targeted parity test passes.

## Step 8 — Add auto-scaffold generator for new sets
- Script creates `part_calls/sets/<name>/working.py` with contract template.
- Test gate: generator unit test passes.

## Step 9 — Add migration status reporter
- Script outputs discovered/migrated/legacy-only set counts.
- Test gate: reporter unit test passes.

## Step 10 — Document usage + run final smoke regression
- Add concise usage docs for discovery and scaffold scripts.
- Run smoke regression tests.
- Test gate: all targeted tests pass.
