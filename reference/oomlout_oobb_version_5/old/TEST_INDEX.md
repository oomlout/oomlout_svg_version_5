# 🧪 Test Index

Quick navigation for the test suite, snapshots, generated artifacts, and per-test reports.

## Start here

- Main test guide: [`tests/README.md`](tests/README.md)
- Test module: [`tests/test_file_generation.py`](tests/test_file_generation.py)
- Snapshot baseline: [`tests/snapshots/file_generation_snapshot.json`](tests/snapshots/file_generation_snapshot.json)
- Per-test report index: [`tests/test_runs/README.md`](tests/test_runs/README.md)
- Current failure summary: [`TEST_FAILURES.md`](TEST_FAILURES.md)

## Capability coverage (expanded object generation)

These are the heavy coverage tests that generate many objects and compare SCAD/JSON/YAML/TXT + OpenSCAD AST hashes.

- Core geometry report: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_core_geometry/test_report.md`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_core_geometry/test_report.md)
  - Generated files: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_core_geometry/capability_core_geometry/generated/`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_core_geometry/capability_core_geometry/generated/)
- Motion + drive report: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_motion_drive/test_report.md`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_motion_drive/test_report.md)
  - Generated files: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_motion_drive/capability_motion_drive/generated/`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_motion_drive/capability_motion_drive/generated/)
- Fasteners + connectors report: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_fasteners_connectors/test_report.md`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_fasteners_connectors/test_report.md)
  - Generated files: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_fasteners_connectors/capability_fasteners_connectors/generated/`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_fasteners_connectors/capability_fasteners_connectors/generated/)
- Holders + storage report: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_holders_storage/test_report.md`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_holders_storage/test_report.md)
  - Generated files: [`tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_holders_storage/capability_holders_storage/generated/`](tests/test_runs/test_file_generation_ScadGenerationMatrixTests_test_capability_holders_storage/capability_holders_storage/generated/)

## Other key test reports

- Snapshot markdown generation: [`tests/test_runs/test_file_generation_SnapshotTests_test_markdown_generation_snapshot/test_report.md`](tests/test_runs/test_file_generation_SnapshotTests_test_markdown_generation_snapshot/test_report.md)
- OOBB base dump/load/build tests: [`tests/test_runs/test_file_generation_OobbBaseFileGenerationTests_test_dump_json_and_load_json_round_trip/test_report.md`](tests/test_runs/test_file_generation_OobbBaseFileGenerationTests_test_dump_json_and_load_json_round_trip/test_report.md)
- Release copy workflow (3d print): [`tests/test_runs/test_file_generation_FileGenerationTests_test_release_3d_printable_copies_expected_files/test_report.md`](tests/test_runs/test_file_generation_FileGenerationTests_test_release_3d_printable_copies_expected_files/test_report.md)
- Release copy workflow (laser cut): [`tests/test_runs/test_file_generation_FileGenerationTests_test_release_laser_cut_copies_expected_files/test_report.md`](tests/test_runs/test_file_generation_FileGenerationTests_test_release_laser_cut_copies_expected_files/test_report.md)

## Full report table

For a complete list of all tests, status, artifact counts, and report links:

- [`tests/test_runs/README.md`](tests/test_runs/README.md)
