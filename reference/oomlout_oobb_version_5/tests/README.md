# Test Suite for File-Generation Baseline

This test suite is designed to create a safety net before refactoring the OOBB generation code.

## Scope

The suite currently validates file-output behavior for:

- `oobb_dxf_laser_copy.copy_and_rename_file`
- `oobb_dxf_laser_copy.folders_to_folder_all`
- `oobb_markdown.make_markdown`
- `action_generate_release_3d_printable.main`
- `action_generate_release_laser_cut.main`
- `oobb_base.get_thing_from_dict` + `oobb_base.build_thing` across many discovered item types
- Capability-specific generation regression suites (core geometry, motion, fasteners/connectors, holders/storage)

## Why these tests first

These paths are deterministic and operate primarily on files/directories, so they give immediate regression protection while larger generator internals are still tightly coupled.

## Per-item SCAD matrix (broad coverage)

- The suite discovers buildable item types from `oobb_make_sets.get_*` and validates them by capability bucket.
- Capability tests:
	- `capability_core_geometry`
	- `capability_motion_drive`
	- `capability_fasteners_connectors`
	- `capability_holders_storage`
- Each capability test writes all generated files into its own test folder, for example:
	- `tests/test_runs/<test_name>/capability_core_geometry/generated/<item-id>/3dpr.scad`
	- `tests/test_runs/<test_name>/capability_core_geometry/generated/<item-id>/3dpr.json`
	- `tests/test_runs/<test_name>/capability_core_geometry/generated/<item-id>/3dpr.yaml`
	- `tests/test_runs/<test_name>/capability_core_geometry/generated/<item-id>/3dpr.txt`
- Snapshot parity is strict for generated artifacts:
	- `scad_hashes`
	- `json_hashes`
	- `yaml_hashes`
	- `txt_hashes`
	- `openscad_ast_hashes`
	- OpenSCAD validation is performed per SCAD file by exporting AST output and hashing it.

	## OpenSCAD requirement

	- OpenSCAD must be installed for SCAD matrix validation.
	- The test auto-detects OpenSCAD from:
		- `openscad` / `openscad.com` on `PATH`
		- `C:\Program Files\OpenSCAD\openscad.com`
		- `C:\Program Files\OpenSCAD\openscad.exe`
	- If OpenSCAD is missing, the SCAD matrix test fails with a clear setup message.

## Running tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Per-test folders and reports

- Every test writes artifacts to its own folder under `tests/test_runs/`.
- Folder name pattern: `<module>_<class>_<test_name>`.
- Each folder contains `test_report.md`.
	- On pass: report includes status and key coverage notes.
	- On fail: report includes a **Changed bits** section with file/hash deltas for changed snapshot groups.
- A central index is auto-generated at `tests/test_runs/README.md` with status, artifact counts, and links to each report.

## Snapshot workflow

A snapshot hash map is stored in `tests/snapshots/file_generation_snapshot.json`.

- Normal run: compare generated output hashes against baseline.
- Includes:
	- `markdown_generation`
	- `capability_core_geometry`
	- `capability_motion_drive`
	- `capability_fasteners_connectors`
	- `capability_holders_storage`
- Update snapshot intentionally:

```powershell
$env:UPDATE_SNAPSHOTS="1"
python -m unittest discover -s tests -p "test_*.py"
```

Then clear the variable:

```powershell
Remove-Item Env:\UPDATE_SNAPSHOTS
```
