import hashlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import action_generate_release_3d_printable
import action_generate_release_laser_cut
import oobb
import oobb_dxf_laser_copy
import oobb_make_sets
import oobb_markdown


TESTS_DIR = Path(__file__).parent
GENERATED_SCAD_DIR = TESTS_DIR / "generated_scad"
TEST_RUNS_DIR = TESTS_DIR / "test_runs"


class ReportedTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        safe_name = self.id().replace(".", "_")
        self.test_artifact_dir = TEST_RUNS_DIR / safe_name
        if self.test_artifact_dir.exists():
            shutil.rmtree(self.test_artifact_dir)
        self.test_artifact_dir.mkdir(parents=True, exist_ok=True)
        self.report_path = self.test_artifact_dir / "test_report.md"
        self._report_lines = []
        self._changed_bits = []
        self._report_images = []

    def add_report_line(self, line: str):
        self._report_lines.append(line)

    def add_report_image(self, image_path: Path, label: str):
        self._report_images.append((image_path, label))

    def record_hash_diff(self, group_name: str, expected_map, actual_map, max_lines: int = 40):
        expected_map = expected_map or {}
        actual_map = actual_map or {}
        changed = []

        expected_keys = set(expected_map.keys())
        actual_keys = set(actual_map.keys())

        for key in sorted(expected_keys - actual_keys):
            changed.append(f"- missing in actual: `{key}`")
        for key in sorted(actual_keys - expected_keys):
            changed.append(f"- extra in actual: `{key}`")
        for key in sorted(expected_keys & actual_keys):
            if expected_map[key] != actual_map[key]:
                changed.append(
                    f"- changed `{key}`\\n"
                    f"  - expected: `{expected_map[key]}`\\n"
                    f"  - actual:   `{actual_map[key]}`"
                )

        if changed:
            self._changed_bits.append(f"### {group_name}\n" + "\n".join(changed[:max_lines]))

    def _write_test_report(self):
        result = getattr(self._outcome, "result", None)
        failed = False
        if result is not None:
            for test, _ in (getattr(result, "failures", []) + getattr(result, "errors", [])):
                if test is self:
                    failed = True
                    break

        status = "FAIL" if failed else "PASS"
        report = [
            f"# Test Report: `{self.id()}`",
            "",
            f"- Status: **{status}**",
            f"- Timestamp: `{datetime.now().isoformat(timespec='seconds')}`",
            f"- Artifact folder: `{self.test_artifact_dir.as_posix()}`",
            "",
        ]
        if self._report_lines:
            report.append("## Notes")
            report.append("")
            report.extend(self._report_lines)
            report.append("")

        if self._report_images:
            report.append("## Rendered previews")
            report.append("")
            for image_path, label in self._report_images:
                try:
                    rel = image_path.relative_to(self.test_artifact_dir).as_posix()
                except ValueError:
                    rel = image_path.as_posix()
                report.append(f"### {label}")
                report.append("")
                report.append(f"![{label}]({rel})")
                report.append("")

        if failed and self._changed_bits:
            report.append("## Changed bits")
            report.append("")
            report.extend(self._changed_bits)
            report.append("")

        self.report_path.write_text("\n".join(report), encoding="utf-8")

    @staticmethod
    def _extract_status_from_report(report_path: Path) -> str:
        try:
            for line in report_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("- Status:"):
                    if "PASS" in line:
                        return "PASS"
                    if "FAIL" in line:
                        return "FAIL"
        except Exception:
            pass
        return "UNKNOWN"

    @classmethod
    def _rebuild_test_runs_index(cls):
        TEST_RUNS_DIR.mkdir(parents=True, exist_ok=True)
        index_path = TEST_RUNS_DIR / "README.md"

        rows = []
        for test_dir in sorted([p for p in TEST_RUNS_DIR.iterdir() if p.is_dir()]):
            report = test_dir / "test_report.md"
            if not report.exists():
                continue

            status = cls._extract_status_from_report(report)
            artifacts = [f for f in test_dir.rglob("*") if f.is_file() and f.name != "test_report.md"]
            report_rel = report.relative_to(TEST_RUNS_DIR).as_posix()
            rows.append((test_dir.name, status, len(artifacts), report_rel))

        lines = [
            "# Test Run Reports",
            "",
            f"- Total tests with reports: **{len(rows)}**",
            "",
            "| Test Folder | Status | Artifact Files | Report |",
            "| --- | --- | ---: | --- |",
        ]

        for folder_name, status, artifact_count, report_rel in rows:
            lines.append(
                f"| `{folder_name}` | **{status}** | {artifact_count} | [`test_report.md`]({report_rel}) |"
            )

        lines.append("")
        index_path.write_text("\n".join(lines), encoding="utf-8")

    def tearDown(self):
        try:
            self._write_test_report()
            self._rebuild_test_runs_index()
        finally:
            super().tearDown()


class FileGenerationTests(ReportedTestCase):
    def test_copy_and_rename_file_copies_matching_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "input"
            output_dir = root / "output"
            (input_dir / "part_a").mkdir(parents=True)
            (input_dir / "part_b").mkdir(parents=True)
            (input_dir / "part_a" / "laser_flat.dxf").write_text("DXF_A", encoding="utf-8")

            oobb_dxf_laser_copy.copy_and_rename_file(
                str(input_dir), str(output_dir), "laser_flat.dxf"
            )

            self.assertTrue((output_dir / "part_a.dxf").is_file())
            self.assertEqual((output_dir / "part_a.dxf").read_text(encoding="utf-8"), "DXF_A")
            self.assertFalse((output_dir / "part_b.dxf").exists())

    def test_folders_to_folder_all_calls_all_steps(self):
        with (
            mock.patch.object(oobb_dxf_laser_copy, "folders_to_folder_dxf") as dxf,
            mock.patch.object(oobb_dxf_laser_copy, "folders_to_folder_stl") as stl,
            mock.patch.object(oobb_dxf_laser_copy, "folders_to_folder_svg") as svg,
            mock.patch.object(oobb_dxf_laser_copy, "folders_to_folder_png") as png,
        ):
            oobb_dxf_laser_copy.folders_to_folder_all()
            dxf.assert_called_once()
            stl.assert_called_once()
            svg.assert_called_once()
            png.assert_called_once()

    def test_markdown_format_handles_nested_data(self):
        data = {
            "name": "example",
            "numbers": [1, 2, 3],
            "nested": {"k": "v"},
        }
        result = oobb_markdown.markdown_format(data)
        self.assertIn("# details", result)
        self.assertIn("list with 3 items", result)
        self.assertIn("nested", result)

    def test_make_markdown_creates_index_and_part_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parts = root / "parts"
            part_folder = parts / "oobb_plate_03_03"
            part_folder.mkdir(parents=True)

            (part_folder / "details.json").write_text(
                json.dumps({"description": "Plate 3x3", "type": "plate", "width": 3, "height": 3}),
                encoding="utf-8",
            )
            (part_folder / "true.png").write_bytes(b"png")
            (part_folder / "laser_flat.dxf").write_text("dxf", encoding="utf-8")

            cwd = os.getcwd()
            try:
                os.chdir(root)
                oobb_markdown.make_markdown()
            finally:
                os.chdir(cwd)

            self.assertTrue((parts / "README.md").is_file())
            self.assertTrue((part_folder / "README.md").is_file())
            part_readme = (part_folder / "README.md").read_text(encoding="utf-8")
            self.assertIn("Plate 3x3", part_readme)
            self.assertIn("# details", part_readme)

    def test_release_3d_printable_copies_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder_things = root / "parts"
            thing = folder_things / "oobb_plate_03_03_03"
            thing.mkdir(parents=True)

            (thing / "details.json").write_text(
                json.dumps({"type": "plate", "width": 3, "height": 3}),
                encoding="utf-8",
            )
            (thing / "3dpr.stl").write_text("stl", encoding="utf-8")
            (thing / "3dpr.png").write_bytes(b"png")
            (thing / "working.yaml").write_text("id: test", encoding="utf-8")

            folder_release = root / "release_3d"
            action_generate_release_3d_printable.main(
                folder_things=str(folder_things),
                folder_release=str(folder_release),
                clone_if_missing=False,
            )

            self.assertTrue((folder_release / "3dpr" / "oobb_plate_03_03_03" / "3dpr.stl").is_file())
            self.assertTrue(
                (
                    folder_release
                    / "navigation"
                    / "plate"
                    / "width_3"
                    / "height_3"
                    / "oobb_plate_03_03_03"
                    / "3dpr.stl"
                ).is_file()
            )

    def test_release_laser_cut_copies_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder_things = root / "parts"
            thing = folder_things / "oobb_plate_03_03_03"
            thing.mkdir(parents=True)

            (thing / "details.json").write_text(
                json.dumps({"type": "plate", "width": 3, "height": 3}),
                encoding="utf-8",
            )
            (thing / "laser_flat.svg").write_text("svg", encoding="utf-8")
            (thing / "laser_flat.dxf").write_text("dxf", encoding="utf-8")
            (thing / "laser_flat.png").write_bytes(b"png")
            (thing / "working.yaml").write_text("id: test", encoding="utf-8")

            folder_release = root / "release_laser"
            action_generate_release_laser_cut.main(
                folder_things=str(folder_things),
                folder_release=str(folder_release),
                clone_if_missing=False,
            )

            self.assertTrue(
                (
                    folder_release
                    / "laser_cut"
                    / "svg"
                    / "oobb_plate_03_03_03"
                    / "laser.svg"
                ).is_file()
            )
            self.assertTrue(
                (
                    folder_release
                    / "navigation"
                    / "plate"
                    / "width_3"
                    / "height_3"
                    / "oobb_plate_03_03_03"
                    / "laser.dxf"
                ).is_file()
            )


class SnapshotTests(ReportedTestCase):
    SNAPSHOT_FILE = TESTS_DIR / "snapshots" / "file_generation_snapshot.json"

    def _hash_file(self, file_path: Path) -> str:
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

    def _collect_hashes(self, root: Path):
        hashes = {}
        for file_path in sorted(root.rglob("*")):
            if file_path.is_file():
                rel = file_path.relative_to(root).as_posix()
                hashes[rel] = self._hash_file(file_path)
        return hashes

    def _write_or_assert_snapshot(self, key: str, value):
        update = os.environ.get("UPDATE_SNAPSHOTS", "0") == "1"
        if self.SNAPSHOT_FILE.exists():
            snapshots = json.loads(self.SNAPSHOT_FILE.read_text(encoding="utf-8"))
        else:
            snapshots = {}

        if update or key not in snapshots:
            snapshots[key] = value
            self.SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
            self.SNAPSHOT_FILE.write_text(json.dumps(snapshots, indent=2), encoding="utf-8")
            self.add_report_line(f"Snapshot `{key}` written/updated.")
            return

        if value != snapshots[key] and isinstance(value, dict) and isinstance(snapshots[key], dict):
            self.record_hash_diff(key, snapshots[key], value)
        self.assertEqual(value, snapshots[key])

    def test_markdown_generation_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parts = root / "parts"
            part_folder = parts / "oobb_plate_03_03"
            part_folder.mkdir(parents=True)

            (part_folder / "details.json").write_text(
                json.dumps({"description": "Plate 3x3", "type": "plate", "width": 3, "height": 3}),
                encoding="utf-8",
            )
            (part_folder / "true.png").write_bytes(b"png")

            cwd = os.getcwd()
            try:
                os.chdir(root)
                oobb_markdown.make_markdown()
            finally:
                os.chdir(cwd)

            hashes = self._collect_hashes(parts)
            self._write_or_assert_snapshot("markdown_generation", hashes)


class OobbBaseFileGenerationTests(ReportedTestCase):
    def setUp(self):
        super().setUp()
        self._orig_things = dict(oobb.things)
        self._orig_variables = dict(oobb.variables)
        self._orig_things_folder = oobb_base.things_folder_absolute

    def tearDown(self):
        oobb.things.clear()
        oobb.things.update(self._orig_things)
        oobb.variables.clear()
        oobb.variables.update(self._orig_variables)
        oobb_base.things_folder_absolute = self._orig_things_folder
        super().tearDown()

    def test_dump_json_and_load_json_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                oobb.things.clear()
                oobb.variables.clear()
                oobb.things.update({"part_1": {"id": "part_1", "value": 3}})
                oobb.variables.update({"osp": 15})

                oobb_base.dump("json")
                self.assertTrue(Path("things.json").is_file())
                self.assertTrue(Path("variables.json").is_file())

                oobb.things.clear()
                oobb.variables.clear()
                oobb_base.load("json")

                self.assertIn("part_1", oobb.things)
                self.assertEqual(oobb.things["part_1"]["value"], 3)
            finally:
                os.chdir(cwd)

    def test_dump_pickle_creates_pickle_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            try:
                os.chdir(tmp)
                oobb.things.clear()
                oobb.variables.clear()
                oobb.things.update({"part_1": {"id": "part_1"}})
                oobb.variables.update({"osp": 15})

                oobb_base.dump("pickle")

                self.assertTrue(Path("temporary/things.pickle").is_file())
                self.assertTrue(Path("temporary/variables.pickle").is_file())
            finally:
                os.chdir(cwd)

    def test_dump_folder_creates_details_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            parts_dir = Path(tmp) / "parts"
            oobb_base.things_folder_absolute = str(parts_dir)
            oobb.things.clear()
            oobb.things.update(
                {
                    "part_1": {
                        "id": "part_1",
                        "type": "plate",
                        "description": "test part",
                    }
                }
            )

            oobb_base.dump("folder")

            self.assertTrue((parts_dir / "part_1" / "details.json").is_file())
            self.assertTrue((parts_dir / "part_1" / "details.yaml").is_file())

    def test_build_thing_writes_mode_files_and_calls_renderer(self):
        with tempfile.TemporaryDirectory() as tmp:
            parts_dir = Path(tmp) / "parts"
            thing_id = "part_build"
            (parts_dir / thing_id).mkdir(parents=True)
            oobb_base.things_folder_absolute = str(parts_dir)

            oobb.things.clear()
            oobb.things.update(
                {
                    thing_id: {
                        "thickness_mm": 6,
                        "height_mm": 30,
                        "components": [{"shape": "cube"}],
                        "components_string": ["cube_component"],
                        "components_objects": [{"shape": "cube", "size": [1, 1, 1]}],
                    }
                }
            )

            with mock.patch.object(oobb_base.opsc, "opsc_make_object") as mocked_make:
                oobb_base.build_thing(thing_id, save_type="none", overwrite=True, modes=["3dpr", "laser"])

            self.assertEqual(mocked_make.call_count, 2)
            self.assertTrue((parts_dir / thing_id / "3dpr.txt").is_file())
            self.assertTrue((parts_dir / thing_id / "3dpr.json").is_file())
            self.assertTrue((parts_dir / thing_id / "3dpr.yaml").is_file())
            self.assertTrue((parts_dir / thing_id / "laser.txt").is_file())
            self.assertTrue((parts_dir / thing_id / "laser.json").is_file())
            self.assertTrue((parts_dir / thing_id / "laser.yaml").is_file())

    def test_build_thing_filename_calls_renderer_for_all_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "output_"
            with mock.patch.object(oobb_base.opsc, "opsc_make_object") as mocked_make:
                oobb_base.build_thing_filename(
                    thing=[{"shape": "cube"}],
                    save_type="none",
                    overwrite=True,
                    filename=str(base),
                    depth=6,
                    height=40,
                    render=False,
                )

            self.assertEqual(mocked_make.call_count, 3)
            called_files = [call.args[0] for call in mocked_make.call_args_list]
            self.assertIn(f"{base}3dpr.scad", called_files)
            self.assertIn(f"{base}laser.scad", called_files)
            self.assertIn(f"{base}true.scad", called_files)


class ScadGenerationMatrixTests(ReportedTestCase):
    SNAPSHOT_FILE = TESTS_DIR / "snapshots" / "file_generation_snapshot.json"

    def setUp(self):
        super().setUp()
        self._orig_things = dict(oobb.things)
        self._orig_variables = dict(oobb.variables)
        self._orig_things_folder = oobb_base.things_folder_absolute

    def tearDown(self):
        oobb.things.clear()
        oobb.things.update(self._orig_things)
        oobb.variables.clear()
        oobb.variables.update(self._orig_variables)
        oobb_base.things_folder_absolute = self._orig_things_folder
        super().tearDown()

    def _hash_file(self, file_path: Path) -> str:
        return hashlib.sha256(file_path.read_bytes()).hexdigest()

    def _write_or_assert_snapshot(self, key: str, value):
        update = os.environ.get("UPDATE_SNAPSHOTS", "0") == "1"
        if self.SNAPSHOT_FILE.exists():
            snapshots = json.loads(self.SNAPSHOT_FILE.read_text(encoding="utf-8"))
        else:
            snapshots = {}

        if update or key not in snapshots:
            snapshots[key] = value
            self.SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
            self.SNAPSHOT_FILE.write_text(json.dumps(snapshots, indent=2), encoding="utf-8")
            self.add_report_line(f"Snapshot `{key}` written/updated.")
            return

        if value != snapshots[key] and isinstance(value, dict) and isinstance(snapshots[key], dict):
            self.record_hash_diff(key, snapshots[key], value)
        self.assertEqual(value, snapshots[key])

    def _call_getter(self, getter):
        sig = inspect.signature(getter)
        if "size" in sig.parameters:
            return getter(size="oobb")
        return getter()

    def _discover_buildable_items(self, limit=40):
        discovered = []
        getter_names = sorted(
            [
                name
                for name in dir(oobb_make_sets)
                if name.startswith("get_") and callable(getattr(oobb_make_sets, name))
            ]
        )
        for getter_name in getter_names:
            getter = getattr(oobb_make_sets, getter_name)
            try:
                items = self._call_getter(getter)
            except Exception:
                continue
            if not isinstance(items, list):
                continue

            for idx, item in enumerate(items):
                if not isinstance(item, dict) or "type" not in item:
                    continue
                # avoid duplicates by type and getter source; keep broad spread
                discovered.append((getter_name, idx, item))
                break

            if len(discovered) >= limit:
                break

        buildable = []
        seen_types = set()
        for getter_name, idx, item in discovered:
            typ = item.get("type", "")
            if typ in seen_types:
                continue
            try:
                # Validate that this item can be constructed through the real dispatch path.
                thing = oobb_base.get_thing_from_dict(item)
                if isinstance(thing, dict) and thing.get("components") is not None:
                    buildable.append((getter_name, idx, item))
                    seen_types.add(typ)
            except Exception:
                continue

        return buildable

    def _find_openscad_executable(self):
        candidates = [
            shutil.which("openscad"),
            shutil.which("openscad.com"),
            r"C:\Program Files\OpenSCAD\openscad.com",
            r"C:\Program Files\OpenSCAD\openscad.exe",
            r"C:\Program Files (x86)\OpenSCAD\openscad.com",
            r"C:\Program Files (x86)\OpenSCAD\openscad.exe",
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                return str(candidate)
        return None

    def _validate_scad_file(self, openscad_executable: str, scad_file: Path):
        with tempfile.TemporaryDirectory() as tmp:
            ast_file = Path(tmp) / f"{scad_file.stem}.ast"
            result = subprocess.run(
                [openscad_executable, "-q", "-o", str(ast_file), str(scad_file)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=(
                    f"OpenSCAD validation failed for {scad_file}\n"
                    f"stdout:\n{result.stdout}\n"
                    f"stderr:\n{result.stderr}"
                ),
            )
            self.assertTrue(ast_file.exists(), f"Expected AST output for {scad_file}")
            return self._hash_file(ast_file)

    def _render_scad_png(self, openscad_executable: str, scad_file: Path) -> Path:
        png_file = scad_file.with_suffix(".png")
        result = subprocess.run(
            [
                openscad_executable,
                "-q",
                "--autocenter",
                "--viewall",
                "--imgsize",
                "512,384",
                "-o",
                str(png_file),
                str(scad_file),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"OpenSCAD PNG render failed for {scad_file}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            ),
        )
        self.assertTrue(png_file.exists(), f"Expected PNG output for {scad_file}")
        return png_file

    def _run_capability_snapshot(self, capability_name: str, include_types, required_types: int):
        openscad_executable = self._find_openscad_executable()
        self.assertIsNotNone(
            openscad_executable,
            "OpenSCAD executable not found. Install OpenSCAD or add it to PATH.",
        )

        discovered = self._discover_buildable_items(limit=200)
        by_type = {item[2].get("type", ""): item for item in discovered}
        selected = [by_type[t] for t in include_types if t in by_type]

        self.assertGreaterEqual(
            len(selected),
            required_types,
            f"Expected at least {required_types} buildable item types for capability `{capability_name}`.",
        )

        capability_dir = self.test_artifact_dir / capability_name / "generated"
        capability_dir.mkdir(parents=True, exist_ok=True)

        oobb_base.things_folder_absolute = str(capability_dir)
        oobb.things.clear()

        generated_scad_files = []
        generated_json_files = []
        generated_yaml_files = []
        generated_txt_files = []
        generated_png_files = []
        ast_hashes = {}

        for getter_name, idx, item in selected:
            with self.subTest(getter=getter_name, index=idx, item_type=item.get("type", "")):
                thing_obj = oobb_base.get_thing_from_dict(item)
                thing_id = thing_obj["id"]
                oobb.things[thing_id] = thing_obj
                oobb_base.build_thing(thing_id, save_type="none", overwrite=True, modes=["3dpr", "laser", "true"])

                # Ensure each item has its own folder and all mode SCAD files.
                item_folder = capability_dir / thing_id
                self.assertTrue(item_folder.is_dir())
                scad_files = [
                    item_folder / "3dpr.scad",
                    item_folder / "laser.scad",
                    item_folder / "true.scad",
                ]
                for scad_file in scad_files:
                    self.assertTrue(scad_file.is_file())
                    generated_scad_files.append(scad_file)
                    rel = scad_file.relative_to(capability_dir).as_posix()
                    ast_hashes[rel] = self._validate_scad_file(openscad_executable, scad_file)
                    png_file = self._render_scad_png(openscad_executable, scad_file)
                    generated_png_files.append(png_file)

                json_files = [
                    item_folder / "3dpr.json",
                    item_folder / "laser.json",
                    item_folder / "true.json",
                ]
                yaml_files = [
                    item_folder / "3dpr.yaml",
                    item_folder / "laser.yaml",
                    item_folder / "true.yaml",
                ]

                for json_file in json_files:
                    self.assertTrue(json_file.is_file())
                    generated_json_files.append(json_file)
                for yaml_file in yaml_files:
                    self.assertTrue(yaml_file.is_file())
                    generated_yaml_files.append(yaml_file)

                txt_files = [
                    item_folder / "3dpr.txt",
                    item_folder / "laser.txt",
                    item_folder / "true.txt",
                ]
                for txt_file in txt_files:
                    self.assertTrue(txt_file.is_file())
                    generated_txt_files.append(txt_file)

        scad_hashes = {}
        for scad_file in sorted(generated_scad_files):
            rel = scad_file.relative_to(capability_dir).as_posix()
            scad_hashes[rel] = self._hash_file(scad_file)

        json_hashes = {}
        for json_file in sorted(generated_json_files):
            rel = json_file.relative_to(capability_dir).as_posix()
            json_hashes[rel] = self._hash_file(json_file)

        yaml_hashes = {}
        for yaml_file in sorted(generated_yaml_files):
            rel = yaml_file.relative_to(capability_dir).as_posix()
            yaml_hashes[rel] = self._hash_file(yaml_file)

        txt_hashes = {}
        for txt_file in sorted(generated_txt_files):
            rel = txt_file.relative_to(capability_dir).as_posix()
            txt_hashes[rel] = self._hash_file(txt_file)

        png_hashes = {}
        for png_file in sorted(generated_png_files):
            rel = png_file.relative_to(capability_dir).as_posix()
            png_hashes[rel] = self._hash_file(png_file)

        self.assertEqual(
            set(scad_hashes.keys()),
            set(ast_hashes.keys()),
            "SCAD hash set and OpenSCAD AST hash set differ.",
        )
        self.assertEqual(len(scad_hashes), len(selected) * 3)
        self.assertEqual(len(json_hashes), len(selected) * 3)
        self.assertEqual(len(yaml_hashes), len(selected) * 3)
        self.assertEqual(len(txt_hashes), len(selected) * 3)
        self.assertEqual(len(png_hashes), len(selected) * 3)

        self.add_report_line(f"Capability: `{capability_name}`")
        self.add_report_line(f"Artifact output: `{capability_dir.as_posix()}`")
        self.add_report_line(f"Buildable item types covered: `{len(selected)}`")
        self.add_report_line(f"Compared SCAD files: `{len(scad_hashes)}`")
        self.add_report_line(f"Compared JSON files: `{len(json_hashes)}`")
        self.add_report_line(f"Compared YAML files: `{len(yaml_hashes)}`")
        self.add_report_line(f"Compared TXT files: `{len(txt_hashes)}`")
        self.add_report_line(f"Compared PNG files: `{len(png_hashes)}`")

        # Add a compact visual preview set (first six PNGs) to each report.
        for png_file in sorted(generated_png_files)[:6]:
            label = png_file.relative_to(capability_dir).as_posix()
            self.add_report_image(png_file, label)

        snapshot_payload = {
            "capability": capability_name,
            "item_count": len(selected),
            "item_types": sorted({item["type"] for _, _, item in selected}),
            "scad_hashes": scad_hashes,
            "json_hashes": json_hashes,
            "yaml_hashes": yaml_hashes,
            "txt_hashes": txt_hashes,
            "png_hashes": png_hashes,
            "openscad_ast_hashes": ast_hashes,
        }

        if self.SNAPSHOT_FILE.exists():
            existing = json.loads(self.SNAPSHOT_FILE.read_text(encoding="utf-8")).get(capability_name, {})
            if isinstance(existing, dict):
                self.record_hash_diff("scad_hashes", existing.get("scad_hashes", {}), scad_hashes)
                self.record_hash_diff("json_hashes", existing.get("json_hashes", {}), json_hashes)
                self.record_hash_diff("yaml_hashes", existing.get("yaml_hashes", {}), yaml_hashes)
                self.record_hash_diff("txt_hashes", existing.get("txt_hashes", {}), txt_hashes)
                self.record_hash_diff("png_hashes", existing.get("png_hashes", {}), png_hashes)
                self.record_hash_diff("openscad_ast_hashes", existing.get("openscad_ast_hashes", {}), ast_hashes)

        self._write_or_assert_snapshot(capability_name, snapshot_payload)

    def test_capability_core_geometry(self):
        self._run_capability_snapshot(
            "capability_core_geometry",
            include_types=["plate", "circle", "mounting_plate", "bearing_plate", "bearing_circle", "other", "test"],
            required_types=6,
        )

    def test_capability_motion_drive(self):
        self._run_capability_snapshot(
            "capability_motion_drive",
            include_types=["gear", "pulley_gt2", "shaft", "shaft_coupler", "wheel", "bearing"],
            required_types=5,
        )

    def test_capability_fasteners_connectors(self):
        self._run_capability_snapshot(
            "capability_fasteners_connectors",
            include_types=["nut", "screw_countersunk", "ziptie_holder_jack", "wire"],
            required_types=3,
        )

    def test_capability_holders_storage(self):
        self._run_capability_snapshot(
            "capability_holders_storage",
            include_types=["tool_holder", "tray", "smd_magazine_lid", "jig", "bunting_alphabet"],
            required_types=4,
        )


if __name__ == "__main__":
    unittest.main()
