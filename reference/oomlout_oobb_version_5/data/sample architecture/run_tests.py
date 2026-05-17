from __future__ import annotations

import contextlib
import io
import json
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

import yaml

from oomlout_roboclick import discover_actions, get_all_actions_documentation, run_folder


ROOT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = ROOT_DIR / "test_result"
TESTS_DIR = ROOT_DIR / "tests"
PYTHON_TEST_DEFINITION_FILE = TESTS_DIR / "working.py"


@dataclass
class TestCase:
    name: str
    kind: str
    runner: Callable[[], Any]
    definition_file: str = ""


def _slugify(value: str) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append("_")
    text = "".join(cleaned).strip("_")
    while "__" in text:
        text = text.replace("__", "_")
    return text or "test"


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _normalize_test_result(raw_result: Any) -> tuple[bool, dict[str, Any]]:
    if isinstance(raw_result, dict):
        if "all_passed" in raw_result:
            return bool(raw_result.get("all_passed")), raw_result
        if "passed" in raw_result and "failed" in raw_result:
            return bool(raw_result.get("failed", 1) == 0), raw_result
        if "passed" in raw_result:
            return bool(raw_result.get("passed")), raw_result
        return True, raw_result
    if isinstance(raw_result, bool):
        return raw_result, {"returned": raw_result}
    return bool(raw_result), {"returned": repr(raw_result)}


def _load_yaml_file(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _load_module_from_file(file_path: Path, module_name: str) -> ModuleType:
    spec = spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {file_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_case(test_case: TestCase) -> dict[str, Any]:
    import time

    log_buffer = io.StringIO()
    started = time.monotonic()
    status = "passed"
    result_data: dict[str, Any] = {}
    error_text = ""

    try:
        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
            raw_result = test_case.runner()
        passed, result_data = _normalize_test_result(raw_result)
        status = "passed" if passed else "failed"
    except Exception:
        status = "failed"
        error_text = traceback.format_exc()

    duration = round(time.monotonic() - started, 3)
    if error_text:
        log_buffer.write("\n[EXCEPTION]\n")
        log_buffer.write(error_text)

    log_name = f"{_slugify(test_case.name)}.log"
    log_path = RESULTS_DIR / log_name
    _write_text(log_path, log_buffer.getvalue())

    return {
        "name": test_case.name,
        "kind": test_case.kind,
        "status": status,
        "duration_seconds": duration,
        "result": result_data,
        "error": error_text,
        "log_file": str(log_path.relative_to(ROOT_DIR)),
        "definition_file": test_case.definition_file,
    }


def _make_run_folder_runner(config: dict[str, Any]) -> Callable[[], dict[str, Any]]:
    folder_value = str(config.get("folder", "")).strip()
    mode_value = config.get("mode", "all")
    file_action_value = str(config.get("file_action", "")).strip()

    def _runner() -> dict[str, Any]:
        folder_path = ROOT_DIR / folder_value
        if not folder_path.is_dir():
            return {
                "all_passed": False,
                "passed": 0,
                "failed": 1,
                "reason": f"Folder not found: {folder_path}",
            }

        kwargs: dict[str, Any] = {"folder": str(folder_path)}
        if mode_value not in ("", None):
            kwargs["mode"] = mode_value
        if file_action_value:
            kwargs["file_action"] = file_action_value

        run_folder(**kwargs)
        working_oomp = folder_path / "working.oomp"
        working_yaml = folder_path / "working.yaml"
        used_file = str(working_oomp if working_oomp.exists() else working_yaml)
        return {
            "all_passed": True,
            "passed": 1,
            "failed": 0,
            "folder": str(folder_path),
            "working_file_used": used_file,
        }

    return _runner


def _load_test_definitions() -> list[tuple[Path, dict[str, Any]]]:
    definitions: list[tuple[Path, dict[str, Any]]] = []
    if not TESTS_DIR.exists():
        return definitions

    for test_dir in sorted(TESTS_DIR.iterdir(), key=lambda p: p.name):
        if not test_dir.is_dir():
            continue
        definition_file = test_dir / "working.yaml"
        if not definition_file.is_file():
            continue
        definition = _load_yaml_file(definition_file)
        if not definition:
            continue
        if definition.get("enabled", True) is False:
            continue
        definitions.append((definition_file, definition))

    if PYTHON_TEST_DEFINITION_FILE.is_file():
        try:
            module = _load_module_from_file(
                PYTHON_TEST_DEFINITION_FILE,
                f"roboclick_tests_{abs(hash(str(PYTHON_TEST_DEFINITION_FILE)))}",
            )
            define_fn = getattr(module, "define", None)
            if callable(define_fn):
                raw_definitions = define_fn()
                if isinstance(raw_definitions, dict):
                    raw_definitions = [raw_definitions]
                if isinstance(raw_definitions, list):
                    for item in raw_definitions:
                        if not isinstance(item, dict):
                            continue
                        if item.get("enabled", True) is False:
                            continue
                        definitions.append((PYTHON_TEST_DEFINITION_FILE, item))
                else:
                    print(
                        f"Warning: {PYTHON_TEST_DEFINITION_FILE} define() must return a dict or list of dicts."
                    )
            else:
                print(f"Warning: {PYTHON_TEST_DEFINITION_FILE} is missing define().")
        except Exception as exc:
            print(f"Warning: failed to load python test definitions from {PYTHON_TEST_DEFINITION_FILE}: {exc}")
    return definitions


def _build_test_cases() -> list[TestCase]:
    test_cases: list[TestCase] = []
    discovered_actions = discover_actions()
    action_root = ROOT_DIR / "actions"

    def _action_audit_runner() -> dict[str, Any]:
        action_dirs = sorted(path for path in action_root.iterdir() if path.is_dir())
        import_failures: list[str] = []
        contract_failures: list[str] = []
        duplicate_named_files: list[str] = []
        metadata_name_mismatches: list[str] = []
        smoke_failures: list[str] = []

        for action_dir in action_dirs:
            working_file = action_dir / "working.py"
            named_file = action_dir / f"{action_dir.name}.py"
            if named_file.exists():
                duplicate_named_files.append(action_dir.name)
            if not working_file.is_file():
                contract_failures.append(f"{action_dir.name}: missing working.py")
                continue

            try:
                module = _load_module_from_file(
                    working_file,
                    f"audit_{action_dir.name}_{abs(hash(str(working_file)))}",
                )
            except Exception as exc:
                import_failures.append(f"{action_dir.name}: {exc}")
                continue

            define_fn = getattr(module, "define", None)
            action_fn = getattr(module, "action", None)
            if not callable(define_fn) or not callable(action_fn):
                contract_failures.append(
                    f"{action_dir.name}: define={callable(define_fn)}, action={callable(action_fn)}"
                )
                continue

            metadata = define_fn()
            if not isinstance(metadata, dict):
                contract_failures.append(f"{action_dir.name}: define() did not return dict")
                continue

            for key in ("name", "description", "variables", "category"):
                if key not in metadata:
                    contract_failures.append(f"{action_dir.name}: missing metadata key {key}")
            if metadata.get("name") != action_dir.name:
                metadata_name_mismatches.append(
                    f"{action_dir.name}: define().name={metadata.get('name')!r}"
                )

            test_fn = getattr(module, "test", None)
            if not callable(test_fn):
                fallback_test = action_dir / "oomlout_test.py"
                if fallback_test.is_file():
                    test_module = _load_module_from_file(
                        fallback_test,
                        f"audit_test_{action_dir.name}_{abs(hash(str(fallback_test)))}",
                    )
                    test_fn = getattr(test_module, "test", None)
            if callable(test_fn):
                try:
                    result = test_fn()
                except Exception as exc:
                    smoke_failures.append(f"{action_dir.name}: {exc}")
                else:
                    passed, details = _normalize_test_result(result)
                    if not passed:
                        smoke_failures.append(f"{action_dir.name}: {details}")
            else:
                contract_failures.append(f"{action_dir.name}: missing callable test()")

        docs = get_all_actions_documentation()
        doc_commands = {item.get("command", "") for item in docs}
        expected_commands = {path.name for path in action_dirs}
        missing_docs = sorted(name for name in expected_commands if name not in doc_commands)
        missing_discovered = sorted(name for name in expected_commands if name not in discovered_actions)

        failures = []
        failures.extend(import_failures)
        failures.extend(contract_failures)
        failures.extend(metadata_name_mismatches)
        failures.extend(smoke_failures)
        failures.extend(f"duplicate_named_file:{name}" for name in duplicate_named_files)
        failures.extend(f"missing_discovered:{name}" for name in missing_discovered)
        failures.extend(f"missing_docs:{name}" for name in missing_docs)

        return {
            "all_passed": len(failures) == 0,
            "passed": len(action_dirs) - len(failures),
            "failed": len(failures),
            "total_action_dirs": len(action_dirs),
            "discovered_actions": len(discovered_actions),
            "documented_actions": len(docs),
            "details": failures,
        }

    test_cases.append(
        TestCase(
            name="Action audit: all action folders",
            kind="audit",
            runner=_action_audit_runner,
            definition_file="run_tests.py",
        )
    )

    for definition_file, definition in _load_test_definitions():
        test_type = str(definition.get("type", "")).strip().lower()
        base_name = str(definition.get("name", definition_file.parent.name)).strip()
        kind = str(definition.get("kind", "custom")).strip() or "custom"
        definition_rel = str(definition_file.relative_to(ROOT_DIR))

        if test_type == "run_folder":
            test_cases.append(
                TestCase(
                    name=base_name,
                    kind=kind,
                    runner=_make_run_folder_runner(definition),
                    definition_file=definition_rel,
                )
            )
            continue

        if test_type == "action_tests_all":
            for action_name, action_info in sorted(discovered_actions.items(), key=lambda item: item[0]):
                test_cases.append(
                    TestCase(
                        name=f"{base_name}: {action_name}",
                        kind=kind or "action",
                        runner=action_info.test_fn,
                        definition_file=definition_rel,
                    )
                )
            continue

        if test_type == "action_test":
            action_name = str(definition.get("action", "")).strip()
            action_info = discovered_actions.get(action_name)
            if action_info is None:
                def _missing_action_runner(action_name_local: str = action_name) -> dict[str, Any]:
                    return {
                        "all_passed": False,
                        "passed": 0,
                        "failed": 1,
                        "reason": f"Action not found: {action_name_local}",
                    }

                test_cases.append(
                    TestCase(
                        name=base_name,
                        kind=kind,
                        runner=_missing_action_runner,
                        definition_file=definition_rel,
                    )
                )
            else:
                test_cases.append(
                    TestCase(
                        name=base_name,
                        kind=kind,
                        runner=action_info.test_fn,
                        definition_file=definition_rel,
                    )
                )
            continue

        def _unknown_type_runner(test_type_local: str = test_type) -> dict[str, Any]:
            return {
                "all_passed": False,
                "passed": 0,
                "failed": 1,
                "reason": f"Unknown test type: {test_type_local}",
            }

        test_cases.append(
            TestCase(
                name=base_name,
                kind=kind,
                runner=_unknown_type_runner,
                definition_file=definition_rel,
            )
        )

    return test_cases


def _write_summary(results: list[dict[str, Any]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    passed = sum(1 for item in results if item["status"] == "passed")
    failed = len(results) - passed

    payload = {
        "timestamp_utc": timestamp,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results,
    }
    _write_text(RESULTS_DIR / "results.json", json.dumps(payload, indent=2))

    lines = [
        "# RoboClick Test Results",
        "",
        f"- Timestamp (UTC): {timestamp}",
        f"- Total: {len(results)}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        "",
        "| Test | Kind | Status | Duration (s) | Definition | Log |",
        "|---|---|---|---:|---|---|",
    ]

    for item in results:
        lines.append(
            f"| {item['name']} | {item['kind']} | {item['status']} | "
            f"{item['duration_seconds']:.3f} | {item['definition_file']} | {item['log_file']} |"
        )
    lines.append("")
    _write_text(RESULTS_DIR / "results.md", "\n".join(lines))


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    all_results: list[dict[str, Any]] = []

    for test_case in _build_test_cases():
        all_results.append(_run_case(test_case))

    _write_summary(all_results)
    failed = sum(1 for item in all_results if item["status"] != "passed")
    print(f"Tests complete: {len(all_results) - failed} passed, {failed} failed.")
    print(f"Summary: {RESULTS_DIR / 'results.md'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
