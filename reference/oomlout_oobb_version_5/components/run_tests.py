from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from typing import Literal

from oobb_arch.catalog.object_discovery import discover_objects
from oobb_arch.catalog.part_set_discovery import discover_part_sets


@dataclass
class TestResult:
    entity_type: Literal["object", "set"]
    name: str
    status: Literal["PASS", "FAIL", "ERROR", "SKIP"]
    message: str
    duration: float


def run_all_object_tests(objects_root=None) -> list[TestResult]:
    results: list[TestResult] = []
    discovered = discover_objects(objects_root=objects_root)
    for name in sorted(discovered.keys()):
        item = discovered[name]
        if item.test_fn is None:
            results.append(TestResult("object", name, "SKIP", "no test() function", 0.0))
            continue

        start = time.perf_counter()
        try:
            passed = bool(item.test_fn())
            status: Literal["PASS", "FAIL"] = "PASS" if passed else "FAIL"
            message = "" if passed else "test() returned False"
        except Exception as exc:
            status = "ERROR"
            message = str(exc)
        duration = time.perf_counter() - start
        results.append(TestResult("object", name, status, message, duration))
    return results


def run_all_set_tests(sets_root=None) -> list[TestResult]:
    results: list[TestResult] = []
    discovered = discover_part_sets(sets_root=sets_root)
    for name in sorted(discovered.keys()):
        item = discovered[name]
        if item.test_fn is None:
            results.append(TestResult("set", name, "SKIP", "no test() function", 0.0))
            continue

        start = time.perf_counter()
        try:
            passed = bool(item.test_fn())
            status: Literal["PASS", "FAIL"] = "PASS" if passed else "FAIL"
            message = "" if passed else "test() returned False"
        except Exception as exc:
            status = "ERROR"
            message = str(exc)
        duration = time.perf_counter() - start
        results.append(TestResult("set", name, status, message, duration))
    return results


def run_all_tests(objects_root=None, sets_root=None) -> list[TestResult]:
    return run_all_object_tests(objects_root=objects_root) + run_all_set_tests(sets_root=sets_root)


def print_test_report(results: list[TestResult]):
    objects = [result for result in results if result.entity_type == "object"]
    sets = [result for result in results if result.entity_type == "set"]

    print("=" * 44)
    print(" OOBB Per-Folder Test Report")
    print("=" * 44)

    print(f"\nOBJECTS ({len(objects)} total)")
    for result in objects:
        symbol = {"PASS": "✓", "FAIL": "✗", "ERROR": "✗", "SKIP": "⚠"}[result.status]
        suffix = f" {result.message}" if result.message else ""
        print(f"{symbol} {result.name:35} {result.status:5} ({result.duration:.3f}s){suffix}")

    print(f"\nSETS ({len(sets)} total)")
    for result in sets:
        symbol = {"PASS": "✓", "FAIL": "✗", "ERROR": "✗", "SKIP": "⚠"}[result.status]
        suffix = f" {result.message}" if result.message else ""
        print(f"{symbol} {result.name:35} {result.status:5} ({result.duration:.3f}s){suffix}")

    totals = {"PASS": 0, "FAIL": 0, "ERROR": 0, "SKIP": 0}
    for result in results:
        totals[result.status] += 1

    print("\n" + "-" * 44)
    print(
        f"TOTAL: {len(results)} | PASS: {totals['PASS']} | FAIL: {totals['FAIL']} | ERROR: {totals['ERROR']} | SKIP: {totals['SKIP']}"
    )
    print("-" * 44)


def cli() -> int:
    parser = argparse.ArgumentParser(description="OOBB Per-Folder Test Runner")
    parser.add_argument("--objects-only", action="store_true")
    parser.add_argument("--sets-only", action="store_true")
    parser.add_argument("--json", default="", help="Optional path to write JSON test results")
    parser.add_argument("--objects-root", default=None)
    parser.add_argument("--sets-root", default=None)
    args = parser.parse_args()

    if args.objects_only:
        results = run_all_object_tests(objects_root=args.objects_root)
    elif args.sets_only:
        results = run_all_set_tests(sets_root=args.sets_root)
    else:
        results = run_all_tests(objects_root=args.objects_root, sets_root=args.sets_root)

    print_test_report(results)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump([asdict(result) for result in results], handle, indent=2)

    failures = [result for result in results if result.status in ("FAIL", "ERROR")]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(cli())
