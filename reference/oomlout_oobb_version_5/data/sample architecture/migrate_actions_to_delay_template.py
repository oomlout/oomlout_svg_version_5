from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parent
ACTIONS_DIR = ROOT_DIR / "actions"
DEFAULT_TEMPLATE_ACTION = "roboclick_action_base_time_delay"
CANONICAL_SCHEMA_FILE = ROOT_DIR / "canonical_action_schema.json"


@dataclass
class SnapshotEntry:
    existed: bool
    is_dir: bool
    content: bytes | None = None


def _load_module_from_file(file_path: Path, module_name: str):
    spec = spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {file_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _discover_action_dirs(actions_root: Path) -> list[Path]:
    action_dirs: list[Path] = []
    if not actions_root.is_dir():
        return action_dirs
    for entry in sorted(actions_root.iterdir(), key=lambda item: item.name):
        if not entry.is_dir():
            continue
        if (entry / "working.py").is_file():
            action_dirs.append(entry)
    return action_dirs


def _extract_template_schema(template_action_dir: Path) -> dict:
    working_file = template_action_dir / "working.py"
    module = _load_module_from_file(working_file, f"canonical_template_{template_action_dir.name}")
    define_fn = getattr(module, "define", None)
    metadata = {}
    if callable(define_fn):
        raw = define_fn()
        if isinstance(raw, dict):
            metadata = raw

    metadata_keys = sorted(metadata.keys())
    variable_keys: list[str] = []
    raw_variables = metadata.get("variables", [])
    if isinstance(raw_variables, list):
        for item in raw_variables:
            if isinstance(item, dict):
                for key in item.keys():
                    if key not in variable_keys:
                        variable_keys.append(key)

    schema = {
        "schema_version": 1,
        "template_action": template_action_dir.name,
        "runtime_entrypoint": "working.py",
        "canonical_interface": {
            "required_functions": ["define", "action"],
            "test_discovery_fallback_order": [
                "working.py:test",
                "test.py:test",
                "oomlout_test.py:test",
            ],
        },
        "expanded_layout": {
            "required_files": [
                "working.py",
                "<folder_name>.py",
                "oomlout_test.py",
                "config.yaml",
                "README.md",
            ],
            "test_output_dir": "test_result",
        },
        "metadata": {
            "required_keys": [
                "name",
                "name_long",
                "name_short_options",
                "description",
                "variables",
                "category",
                "returns",
            ],
            "template_define_keys": metadata_keys,
            "template_variable_keys": variable_keys,
        },
        "return_semantics": {
            "continue": ["", None],
            "stop": ["exit", "exit_no_tab"],
            "manual_merge": "dict values must be merged into *_manual.yaml",
        },
    }
    return schema


def _write_text_if_changed(path: Path, content: str) -> bool:
    existing = ""
    if path.is_file():
        existing = path.read_text(encoding="utf-8")
    if existing == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def _write_yaml_if_changed(path: Path, payload: dict) -> bool:
    text = yaml.safe_dump(payload, sort_keys=False, allow_unicode=False)
    return _write_text_if_changed(path, text)


def _normalize_name_short_options(raw: object) -> list[str]:
    values: list[str] = []

    if isinstance(raw, str):
        values = [raw]
    elif isinstance(raw, list):
        values = [item for item in raw if isinstance(item, str)]

    cleaned: list[str] = []
    seen: set[str] = set()
    for value in values:
        token = value.strip()
        if not token:
            continue
        if token in seen:
            continue
        seen.add(token)
        cleaned.append(token)
    return cleaned


def _normalize_variables(raw_variables: object) -> list:
    if not isinstance(raw_variables, list):
        return []
    normalized: list = []
    for item in raw_variables:
        if isinstance(item, dict):
            normalized.append(item)
        elif isinstance(item, str):
            normalized.append({"name": item, "description": "", "type": "string", "default": ""})
    return normalized


def _title_from_folder_name(folder_name: str) -> str:
    stripped = folder_name.replace("roboclick_action_", "")
    return " ".join(part.capitalize() for part in stripped.split("_"))


def _extract_metadata_from_working(action_dir: Path) -> dict:
    working_file = action_dir / "working.py"
    module = _load_module_from_file(working_file, f"working_meta_{action_dir.name}")
    define_fn = getattr(module, "define", None)
    if not callable(define_fn):
        return {}
    raw = define_fn()
    if not isinstance(raw, dict):
        return {}
    return raw


def _normalize_metadata(action_dir: Path, metadata: dict) -> dict:
    folder_name = action_dir.name
    short_options = _normalize_name_short_options(metadata.get("name_short_options"))
    if not short_options:
        short_options = _normalize_name_short_options(metadata.get("name_short"))
    if not short_options:
        short_options = _normalize_name_short_options(metadata.get("aliases"))

    description = str(metadata.get("description", "")).strip()
    if not description:
        description = f"RoboClick action `{folder_name}`."

    name_long = str(metadata.get("name_long", "")).strip()
    if not name_long:
        name_long = _title_from_folder_name(folder_name)

    category = str(metadata.get("category", "Other")).strip() or "Other"
    returns = str(metadata.get("returns", "")).strip()
    if not returns:
        returns = (
            'Return "" or None to continue, "exit"/"exit_no_tab" to stop, '
            "or dict to merge into *_manual.yaml."
        )

    return {
        "name": folder_name,
        "name_long": name_long,
        "name_short_options": short_options,
        "description": description,
        "variables": _normalize_variables(metadata.get("variables", [])),
        "category": category,
        "returns": returns,
    }


def _build_config_payload(action_dir: Path, normalized_meta: dict, schema: dict) -> dict:
    return {
        "schema_version": 1,
        "action": {
            "name": action_dir.name,
            "runtime_entrypoint": "working.py",
            "module_mirror": f"{action_dir.name}.py",
            "test_runner": "oomlout_test.py",
        },
        "entrypoints": {"define": "define", "action": "action", "test": "test"},
        "metadata": normalized_meta,
        "return_semantics": schema["return_semantics"],
    }


def _build_readme(action_dir: Path, normalized_meta: dict) -> str:
    lines: list[str] = [
        f"# {action_dir.name}",
        "",
        f"- Runtime entrypoint: `working.py`",
        "- Canonical interface: `define()` + `action()`",
        "- Canonical test runner: `oomlout_test.py`",
        "- Config schema: `config.yaml`",
        "",
        "## Metadata",
        "",
        f"- Name: `{normalized_meta['name']}`",
        f"- Name long: `{normalized_meta['name_long']}`",
        f"- Category: `{normalized_meta['category']}`",
        f"- Description: {normalized_meta['description']}",
        f"- Returns: {normalized_meta['returns']}",
        "",
        "## Name Short Options",
        "",
    ]

    short_options = normalized_meta["name_short_options"]
    if short_options:
        for option in short_options:
            lines.append(f"- `{option}`")
    else:
        lines.append("- _none_")

    lines.extend(["", "## Variables", ""])
    variables = normalized_meta["variables"]
    if variables:
        for variable in variables:
            if isinstance(variable, dict):
                var_name = str(variable.get("name", "")).strip() or "<unnamed>"
                var_type = str(variable.get("type", "string")).strip() or "string"
                var_default = variable.get("default", "")
                var_desc = str(variable.get("description", "")).strip()
                lines.append(
                    f"- `{var_name}` ({var_type}, default `{var_default}`): {var_desc or 'No description.'}"
                )
    else:
        lines.append("- _none_")

    lines.extend(
        [
            "",
            "## Return Semantics",
            "",
            '- Continue: `""` or `None`',
            "- Stop run: `exit` or `exit_no_tab`",
            "- Manual merge update: return a `dict`",
            "",
        ]
    )
    return "\n".join(lines)


def _build_module_mirror_content(action_dir: Path) -> str:
    return (
        '"""Auto-generated canonical mirror for tooling and static discovery."""\n'
        "\n"
        "from importlib.util import module_from_spec, spec_from_file_location\n"
        "from pathlib import Path\n"
        "\n"
        "\n"
        "BASE_DIR = Path(__file__).resolve().parent\n"
        "WORKING_FILE = BASE_DIR / \"working.py\"\n"
        "\n"
        "\n"
        "def _load_working_module():\n"
        "    module_name = f\"{BASE_DIR.name}_working_{abs(hash(str(WORKING_FILE)))}\"\n"
        "    spec = spec_from_file_location(module_name, str(WORKING_FILE))\n"
        "    if spec is None or spec.loader is None:\n"
        "        raise RuntimeError(f\"Unable to load module from {WORKING_FILE}\")\n"
        "    module = module_from_spec(spec)\n"
        "    spec.loader.exec_module(module)\n"
        "    return module\n"
        "\n"
        "\n"
        "_working = _load_working_module()\n"
        "define = getattr(_working, \"define\")\n"
        "action = getattr(_working, \"action\")\n"
        "\n"
        "\n"
        "def test(**kwargs):\n"
        "    test_fn = getattr(_working, \"test\", None)\n"
        "    if callable(test_fn):\n"
        "        return test_fn(**kwargs)\n"
        "\n"
        "    fallback_file = BASE_DIR / \"oomlout_test.py\"\n"
        "    spec = spec_from_file_location(f\"{BASE_DIR.name}_oomlout_test\", str(fallback_file))\n"
        "    if spec is None or spec.loader is None:\n"
        "        return False\n"
        "    module = module_from_spec(spec)\n"
        "    spec.loader.exec_module(module)\n"
        "    fallback_test = getattr(module, \"test\", None)\n"
        "    if not callable(fallback_test):\n"
        "        return False\n"
        "    return fallback_test(**kwargs)\n"
    )


def _build_oomlout_test_content(action_dir: Path) -> str:
    return (
        "import contextlib\n"
        "import io\n"
        "import re\n"
        "import sys\n"
        "import time\n"
        "from importlib.util import module_from_spec, spec_from_file_location\n"
        "from pathlib import Path\n"
        "\n"
        "\n"
        "BASE_DIR = Path(__file__).resolve().parent\n"
        "RESULT_DIR = BASE_DIR / \"test_result\"\n"
        "SUMMARY_FILE = BASE_DIR / \"test.md\"\n"
        "SUMMARY_ALL_FILE = BASE_DIR / \"test_all.md\"\n"
        "\n"
        "\n"
        "def test_1(**kwargs):\n"
        "    \"\"\"Test 1: working.py exposes callable define() and action().\"\"\"\n"
        "    working = _load_working_module()\n"
        "    has_define = callable(getattr(working, \"define\", None))\n"
        "    has_action = callable(getattr(working, \"action\", None))\n"
        "    passed = has_define and has_action\n"
        "    return {\n"
        "        \"passed\": passed,\n"
        "        \"details\": f\"define={has_define}, action={has_action}\",\n"
        "    }\n"
        "\n"
        "\n"
        "def test_2(**kwargs):\n"
        "    \"\"\"Test 2: define() returns a dict with basic metadata keys.\"\"\"\n"
        "    working = _load_working_module()\n"
        "    define_fn = getattr(working, \"define\", None)\n"
        "    if not callable(define_fn):\n"
        "        return {\"passed\": False, \"details\": \"define() missing\"}\n"
        "    metadata = define_fn()\n"
        "    if not isinstance(metadata, dict):\n"
        "        return {\"passed\": False, \"details\": \"define() did not return dict\"}\n"
        "    required = [\"name\", \"description\", \"variables\", \"category\"]\n"
        "    missing = [key for key in required if key not in metadata]\n"
        "    return {\n"
        "        \"passed\": len(missing) == 0,\n"
        "        \"details\": f\"missing_keys={missing}\",\n"
        "    }\n"
        "\n"
        "\n"
        "def test_3(**kwargs):\n"
        "    \"\"\"Test 3: optional working.py test() callable executes successfully.\"\"\"\n"
        "    working = _load_working_module()\n"
        "    working_test = getattr(working, \"test\", None)\n"
        "    if not callable(working_test):\n"
        "        return {\"passed\": True, \"details\": \"working.test() not defined; skipped\"}\n"
        "    result = working_test()\n"
        "    passed = bool(result)\n"
        "    return {\n"
        "        \"passed\": passed,\n"
        "        \"details\": f\"working_test_result={result!r}\",\n"
        "    }\n"
        "\n"
        "\n"
        "def test(test_to_run=\"all\", **kwargs):\n"
        "    selected = _resolve_selected_tests(test_to_run)\n"
        "    if not selected:\n"
        "        _write_text(\n"
        "            SUMMARY_FILE,\n"
        f"            \"# {action_dir.name} Tests\\n\\n\"\n"
        "            f\"- Status: failed\\n\"\n"
        "            f\"- Reason: unknown test_to_run `{test_to_run}`\\n\",\n"
        "        )\n"
        "        return False\n"
        "\n"
        "    all_available = _resolve_selected_tests(\"all\")\n"
        "    selected_names = {name for name, _ in selected}\n"
        "    all_names = {name for name, _ in all_available}\n"
        "    running_all = selected_names == all_names\n"
        "\n"
        "    results = []\n"
        "    for case_name, case_fn in selected:\n"
        "        results.append(_run_case(case_name, case_fn, _get_test_description(case_fn), kwargs))\n"
        "\n"
        "    passed = sum(1 for item in results if item[\"status\"] == \"passed\")\n"
        "    failed = len(results) - passed\n"
        "    lines = [\n"
        f"        \"# {action_dir.name} Tests\",\n"
        "        \"\",\n"
        "        f\"- Selected: {test_to_run}\",\n"
        "        f\"- Total: {len(results)}\",\n"
        "        f\"- Passed: {passed}\",\n"
        "        f\"- Failed: {failed}\",\n"
        "        \"\",\n"
        "        \"| Test | Description | Status | Duration (s) | Details |\",\n"
        "        \"|---|---|---|---:|---|\",\n"
        "    ]\n"
        "    for item in results:\n"
        "        lines.append(\n"
        "            f\"| {item['name']} | {item['description'].replace('|', '/')} | \"\n"
        "            f\"{item['status']} | {item['duration']:.3f} | \"\n"
        "            f\"{item['details'].replace('|', '/')} |\"\n"
        "        )\n"
        "    summary_content = \"\\n\".join(lines) + \"\\n\"\n"
        "    _write_text(SUMMARY_FILE, summary_content)\n"
        "    if running_all:\n"
        "        _write_text(SUMMARY_ALL_FILE, summary_content)\n"
        "    return failed == 0\n"
        "\n"
        "\n"
        "def _load_working_module():\n"
        "    working_file = BASE_DIR / \"working.py\"\n"
        "    module_name = f\"{BASE_DIR.name}_working_{abs(hash(str(working_file)))}\"\n"
        "    spec = spec_from_file_location(module_name, str(working_file))\n"
        "    if spec is None or spec.loader is None:\n"
        "        raise RuntimeError(f\"Unable to load working module from {working_file}\")\n"
        "    module = module_from_spec(spec)\n"
        "    spec.loader.exec_module(module)\n"
        "    return module\n"
        "\n"
        "\n"
        "def _write_text(path, content):\n"
        "    path.parent.mkdir(parents=True, exist_ok=True)\n"
        "    path.write_text(content, encoding=\"utf-8\")\n"
        "\n"
        "\n"
        "def _get_test_description(test_fn):\n"
        "    doc = getattr(test_fn, \"__doc__\", \"\") or \"\"\n"
        "    return \" \".join(doc.strip().split())\n"
        "\n"
        "\n"
        "def _resolve_selected_tests(test_to_run):\n"
        "    tests = {}\n"
        "    for name, value in globals().items():\n"
        "        if not callable(value):\n"
        "            continue\n"
        "        if not re.match(r\"^test_\\d+$\", name):\n"
        "            continue\n"
        "        tests[name] = value\n"
        "    tests = dict(sorted(tests.items(), key=lambda item: int(item[0].split(\"_\", 1)[1])))\n"
        "\n"
        "    if test_to_run in (None, \"\", \"all\"):\n"
        "        return list(tests.items())\n"
        "\n"
        "    token = str(test_to_run).strip().lower()\n"
        "    if token.isdigit():\n"
        "        token = f\"test_{token}\"\n"
        "    if token in tests:\n"
        "        return [(token, tests[token])]\n"
        "    return []\n"
        "\n"
        "\n"
        "def _run_case(case_name, case_fn, description, case_kwargs):\n"
        "    started = time.monotonic()\n"
        "    log_buffer = io.StringIO()\n"
        "    status = \"passed\"\n"
        "    details = \"\"\n"
        "    error_text = \"\"\n"
        "    try:\n"
        "        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):\n"
        "            result = case_fn(**case_kwargs)\n"
        "        if isinstance(result, dict):\n"
        "            passed = bool(result.get(\"passed\", False))\n"
        "            details = str(result.get(\"details\", \"\"))\n"
        "        else:\n"
        "            passed = bool(result)\n"
        "            details = f\"raw_result={result!r}\"\n"
        "        status = \"passed\" if passed else \"failed\"\n"
        "    except Exception as exc:\n"
        "        status = \"failed\"\n"
        "        error_text = repr(exc)\n"
        "        details = \"exception raised\"\n"
        "\n"
        "    elapsed = round(time.monotonic() - started, 3)\n"
        "    lines = [\n"
        "        f\"# {case_name}\",\n"
        "        \"\",\n"
        "        f\"- Description: {description}\",\n"
        "        f\"- Status: {status}\",\n"
        "        f\"- Duration (s): {elapsed}\",\n"
        "        f\"- Details: {details}\",\n"
        "    ]\n"
        "    if error_text:\n"
        "        lines.append(f\"- Error: `{error_text}`\")\n"
        "    logs = log_buffer.getvalue().strip()\n"
        "    if logs:\n"
        "        lines.extend([\"\", \"## Captured Output\", \"\", \"```text\", logs, \"```\"])\n"
        "    _write_text(RESULT_DIR / f\"{case_name}.md\", \"\\n\".join(lines) + \"\\n\")\n"
        "    return {\n"
        "        \"name\": case_name,\n"
        "        \"description\": description,\n"
        "        \"status\": status,\n"
        "        \"duration\": elapsed,\n"
        "        \"details\": details,\n"
        "        \"error\": error_text,\n"
        "    }\n"
        "\n"
        "\n"
        "def main():\n"
        "    test_to_run = \"all\"\n"
        "    if len(sys.argv) > 1:\n"
        "        test_to_run = sys.argv[1]\n"
        "    ok = test(test_to_run=test_to_run)\n"
        f"    print(f\"{action_dir.name} tests complete. selected={{test_to_run}} passed={{ok}}\")\n"
        "    return 0 if ok else 1\n"
        "\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    raise SystemExit(main())\n"
    )


def _remove_top_level_function(text: str, function_name: str) -> str:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return text

    lines = text.splitlines()
    remove_start: int | None = None
    remove_end: int | None = None
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name != function_name:
            continue
        remove_start = node.lineno - 1
        remove_end = node.end_lineno
        break

    if remove_start is None or remove_end is None:
        return text

    del lines[remove_start:remove_end]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _remove_import_line(text: str, pattern: str) -> str:
    lines = text.splitlines()
    updated_lines = [line for line in lines if pattern not in line]
    return "\n".join(updated_lines) + ("\n" if text.endswith("\n") else "")


def _remove_unused_import_lines(text: str) -> str:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return text

    used_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_names.add(node.id)

    lines = text.splitlines()
    ranges_to_remove: list[tuple[int, int]] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            imported_names = [alias.asname or alias.name.split(".")[0] for alias in node.names]
            if all(name not in used_names for name in imported_names):
                ranges_to_remove.append((node.lineno - 1, node.end_lineno))
        if isinstance(node, ast.ImportFrom):
            if node.module == "__future__":
                continue
            imported_names = [alias.asname or alias.name for alias in node.names]
            if all(name not in used_names for name in imported_names):
                ranges_to_remove.append((node.lineno - 1, node.end_lineno))

    for start, end in sorted(ranges_to_remove, reverse=True):
        del lines[start:end]

    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _normalize_blank_lines(text: str) -> str:
    normalized = re.sub(r"\n{3,}", "\n\n", text)
    return normalized.strip() + "\n"


def _cleanup_working_py(action_dir: Path) -> bool:
    working_file = action_dir / "working.py"
    original = working_file.read_text(encoding="utf-8")
    updated = original
    updated = _remove_top_level_function(updated, "_dispatch_action")
    updated = _remove_import_line(updated, "from action_loader import build_action_lookup")
    updated = _remove_unused_import_lines(updated)
    updated = _normalize_blank_lines(updated)
    if updated == original:
        return False
    working_file.write_text(updated, encoding="utf-8")
    return True


def _ensure_action_layout(action_dir: Path, schema: dict, migration_pass: int) -> list[Path]:
    changed: list[Path] = []
    metadata = _extract_metadata_from_working(action_dir)
    normalized_meta = _normalize_metadata(action_dir, metadata)

    config_file = action_dir / "config.yaml"
    if _write_yaml_if_changed(config_file, _build_config_payload(action_dir, normalized_meta, schema)):
        changed.append(config_file)

    readme_file = action_dir / "README.md"
    if _write_text_if_changed(readme_file, _build_readme(action_dir, normalized_meta)):
        changed.append(readme_file)

    mirror_file = action_dir / f"{action_dir.name}.py"
    if _write_text_if_changed(mirror_file, _build_module_mirror_content(action_dir)):
        changed.append(mirror_file)

    oomlout_test_file = action_dir / "oomlout_test.py"
    if not oomlout_test_file.exists():
        if _write_text_if_changed(oomlout_test_file, _build_oomlout_test_content(action_dir)):
            changed.append(oomlout_test_file)

    test_result_dir = action_dir / "test_result"
    if not test_result_dir.exists():
        test_result_dir.mkdir(parents=True, exist_ok=True)
        changed.append(test_result_dir)

    if migration_pass >= 2 and _cleanup_working_py(action_dir):
        changed.append(action_dir / "working.py")

    return changed


def _snapshot_paths(paths: list[Path]) -> dict[Path, SnapshotEntry]:
    snapshot: dict[Path, SnapshotEntry] = {}
    for path in paths:
        if path in snapshot:
            continue
        if path.exists():
            if path.is_dir():
                snapshot[path] = SnapshotEntry(existed=True, is_dir=True, content=None)
            else:
                snapshot[path] = SnapshotEntry(
                    existed=True,
                    is_dir=False,
                    content=path.read_bytes(),
                )
        else:
            snapshot[path] = SnapshotEntry(existed=False, is_dir=path.suffix == "", content=None)
    return snapshot


def _restore_snapshot(snapshot: dict[Path, SnapshotEntry]) -> None:
    for path, entry in snapshot.items():
        if entry.existed:
            if entry.is_dir:
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                if entry.content is not None:
                    path.write_bytes(entry.content)
            continue

        if path.exists():
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)


def _run_quality_gates() -> tuple[bool, list[str]]:
    commands = [
        [sys.executable, "-m", "compileall", "actions", "oomlout_ai_roboclick.py", "run_tests.py"],
        [sys.executable, "run_tests.py"],
    ]
    logs: list[str] = []

    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )
        joined_command = " ".join(command)
        logs.append(f"$ {joined_command}\n{result.stdout}\n{result.stderr}")
        if result.returncode != 0:
            return False, logs
    return True, logs


def _get_target_batches(action_dirs: list[Path], batch_size: int) -> list[list[Path]]:
    if batch_size <= 0:
        return [action_dirs]
    batches: list[list[Path]] = []
    for index in range(0, len(action_dirs), batch_size):
        batches.append(action_dirs[index : index + batch_size])
    return batches


def _candidate_paths_for_action(action_dir: Path) -> list[Path]:
    return [
        action_dir / "working.py",
        action_dir / "config.yaml",
        action_dir / "README.md",
        action_dir / f"{action_dir.name}.py",
        action_dir / "oomlout_test.py",
        action_dir / "test_result",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Align RoboClick actions to the delay template contract.")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE_ACTION, help="Template action folder name.")
    parser.add_argument("--migration-pass", type=int, choices=[1, 2], default=1)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--actions", nargs="*", default=[])
    parser.add_argument("--with-gates", action="store_true")
    parser.add_argument("--write-schema", action="store_true")
    args = parser.parse_args()

    template_action_dir = ACTIONS_DIR / args.template
    if not template_action_dir.is_dir():
        print(f"Template action not found: {template_action_dir}")
        return 1

    schema = _extract_template_schema(template_action_dir)
    if args.write_schema:
        CANONICAL_SCHEMA_FILE.write_text(json.dumps(schema, indent=2), encoding="utf-8")
        print(f"Wrote canonical schema: {CANONICAL_SCHEMA_FILE}")

    all_action_dirs = _discover_action_dirs(ACTIONS_DIR)
    if args.actions:
        selected_names = set(args.actions)
        action_dirs = [item for item in all_action_dirs if item.name in selected_names]
    else:
        action_dirs = all_action_dirs

    if not action_dirs:
        print("No action folders selected.")
        return 0

    batches = _get_target_batches(action_dirs, args.batch_size)
    changed_paths: list[Path] = []

    for batch_index, batch in enumerate(batches, start=1):
        print(f"[batch {batch_index}/{len(batches)}] processing {len(batch)} action folders")
        snapshot_targets: list[Path] = []
        for action_dir in batch:
            snapshot_targets.extend(_candidate_paths_for_action(action_dir))
        snapshot = _snapshot_paths(snapshot_targets)

        for action_dir in batch:
            changed_paths.extend(_ensure_action_layout(action_dir, schema, args.migration_pass))

        if args.with_gates:
            ok, logs = _run_quality_gates()
            for block in logs:
                print(block)
            if not ok:
                print(f"[batch {batch_index}] quality gates failed, restoring this batch.")
                _restore_snapshot(snapshot)
                return 1

    changed_unique = sorted({str(path.relative_to(ROOT_DIR)) for path in changed_paths})
    print("Migration complete.")
    print(f"- Actions processed: {len(action_dirs)}")
    print(f"- Files or dirs changed: {len(changed_unique)}")
    for path_text in changed_unique:
        print(f"  - {path_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
