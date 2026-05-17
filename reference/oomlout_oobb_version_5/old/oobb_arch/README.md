# OOBB Architecture Scaffold (Phase 1)

This package is an additive, compatibility-safe scaffold for a staged refactor.

## Why this exists

- Introduce cleaner boundaries without breaking existing scripts.
- Keep legacy entrypoints (`action_*`, `oobb_working_*`, `oobb_base`) stable.
- Prepare for phased migration to explicit domain/catalog/engine/adapters layers.

## Current status

- No production wiring changed yet.
- `compat/legacy_api.py` delegates to `oobb_base` unchanged.
- Domain models and core interfaces are available for incremental adoption.

## Migration intent

Future phases will route internals through this package while preserving public
input methods and output compatibility validated by snapshots/tests.
