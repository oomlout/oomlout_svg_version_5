import contextlib
import io
import re
import sys
import time
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "test_result"
SUMMARY_FILE = BASE_DIR / "test.md"
SUMMARY_ALL_FILE = BASE_DIR / "test_all.md"


########################
##### tests
########################

def test_1(**kwargs):
    """Test 1: Delay should wait roughly requested time and return empty string."""
    working = _load_working_module()
    started = time.monotonic()
    result = working.action(
        action={
            "delay": 0.2,
            "rand": 0,
            "mode_skip_key": False,
            "mode_scroll_lock_skip": False,
        }
    )
    elapsed = time.monotonic() - started
    passed = (result == "") and (elapsed >= 0.15)
    return {"passed": passed, "details": f"result={result!r}, elapsed={elapsed:.3f}"}


def test_2(**kwargs):
    """Test 2: Invalid delay input should fall back to default delay behavior."""
    working = _load_working_module()
    started = time.monotonic()
    result = working.action(
        action={
            "delay": "not_a_number",
            "rand": 0,
            "mode_skip_key": False,
            "mode_scroll_lock_skip": False,
        }
    )
    elapsed = time.monotonic() - started
    passed = (result == "") and (elapsed >= 0.9)
    return {"passed": passed, "details": f"result={result!r}, elapsed={elapsed:.3f}"}


def test_3(**kwargs):
    """Test 3: Message should be accepted and action should still complete normally."""
    working = _load_working_module()
    result = working.action(
        action={
            "delay": 0.05,
            "rand": 0,
            "message": "delay-test-message",
            "mode_skip_key": False,
            "mode_scroll_lock_skip": False,
        }
    )
    passed = result == ""
    return {"passed": passed, "details": f"result={result!r}"}


########################
##### utils
#######################


def test(test_to_run="all", **kwargs):
    selected = _resolve_selected_tests(test_to_run)
    if not selected:
        _write_text(
            SUMMARY_FILE,
            "# Delay Action Tests\n\n"
            f"- Status: failed\n"
            f"- Reason: unknown test_to_run `{test_to_run}`\n",
        )
        return False

    all_available = _resolve_selected_tests("all")
    selected_names = {name for name, _ in selected}
    all_names = {name for name, _ in all_available}
    running_all = selected_names == all_names

    results = []
    for case_name, case_fn in selected:
        results.append(_run_case(case_name, case_fn, _get_test_description(case_fn), kwargs))

    passed = sum(1 for item in results if item["status"] == "passed")
    failed = len(results) - passed
    lines = [
        "# Delay Action Tests",
        "",
        f"- Selected: {test_to_run}",
        f"- Total: {len(results)}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        "",
        "| Test | Description | Status | Duration (s) | Details |",
        "|---|---|---|---:|---|",
    ]
    for item in results:
        lines.append(
            f"| {item['name']} | {item['description'].replace('|', '/')} | "
            f"{item['status']} | {item['duration']:.3f} | "
            f"{item['details'].replace('|', '/')} |"
        )
    summary_content = "\n".join(lines) + "\n"
    _write_text(SUMMARY_FILE, summary_content)
    if running_all:
        _write_text(SUMMARY_ALL_FILE, summary_content)
    return failed == 0

def _load_working_module():
    working_file = BASE_DIR / "working.py"
    module_name = f"roboclick_action_base_time_delay_working_{abs(hash(str(working_file)))}"
    spec = spec_from_file_location(module_name, str(working_file))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load working module from {working_file}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_text(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _get_test_description(test_fn):
    doc = getattr(test_fn, "__doc__", "") or ""
    return " ".join(doc.strip().split())


def _resolve_selected_tests(test_to_run):
    tests = {}
    for name, value in globals().items():
        if not callable(value):
            continue
        if not re.match(r"^test_\d+$", name):
            continue
        tests[name] = value
    tests = dict(sorted(tests.items(), key=lambda item: int(item[0].split("_", 1)[1])))

    if test_to_run in (None, "", "all"):
        return list(tests.items())

    token = str(test_to_run).strip().lower()
    if token.isdigit():
        token = f"test_{token}"
    if token in tests:
        return [(token, tests[token])]

    return []


def _run_case(case_name, case_fn, description, case_kwargs):
    started = time.monotonic()
    log_buffer = io.StringIO()
    status = "passed"
    details = ""
    error_text = ""
    try:
        with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
            result = case_fn(**case_kwargs)
        if isinstance(result, dict):
            passed = bool(result.get("passed", False))
            details = str(result.get("details", ""))
        else:
            passed = bool(result)
            details = f"raw_result={result!r}"
        status = "passed" if passed else "failed"
    except Exception as exc:
        status = "failed"
        error_text = repr(exc)
        details = "exception raised"

    elapsed = round(time.monotonic() - started, 3)
    lines = [
        f"# {case_name}",
        "",
        f"- Description: {description}",
        f"- Status: {status}",
        f"- Duration (s): {elapsed}",
        f"- Details: {details}",
    ]
    if error_text:
        lines.append(f"- Error: `{error_text}`")
    logs = log_buffer.getvalue().strip()
    if logs:
        lines.extend(["", "## Captured Output", "", "```text", logs, "```"])

    _write_text(RESULT_DIR / f"{case_name}.md", "\n".join(lines) + "\n")
    return {
        "name": case_name,
        "description": description,
        "status": status,
        "duration": elapsed,
        "details": details,
        "error": error_text,
    }


def main():
    test_to_run = "all"
    if len(sys.argv) > 1:
        test_to_run = sys.argv[1]

    ok = test(test_to_run=test_to_run)
    print(f"Delay action tests complete. selected={test_to_run} passed={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
