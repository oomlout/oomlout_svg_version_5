from __future__ import annotations

import json
from pathlib import Path

from oobb_arch.catalog.part_set_discovery import discover_part_sets


DEFAULT_EXPECTED_SETS = [
    "bearing_plates",
    "bearing_circles",
    "buntings",
    "circles",
    "gears",
    "holders",
    "jacks",
    "jigs",
    "mounting_plates",
    "plates",
    "pulleys",
    "shaft_couplers",
    "shafts",
    "soldering_jigs",
    "smd_magazines",
    "tool_holders",
    "trays",
    "ziptie_holders",
    "nuts",
    "wires",
    "wheels",
    "screws",
    "bearings",
    "tests",
    "others",
]


def build_status(expected_sets: list[str] | None = None, sets_root: str | Path | None = None) -> dict:
    expected = expected_sets or list(DEFAULT_EXPECTED_SETS)
    discovered = discover_part_sets(sets_root=sets_root)
    discovered_names = sorted(discovered.keys())

    expected_set = set(expected)
    discovered_set = set(discovered_names)

    missing = sorted(expected_set - discovered_set)
    extra = sorted(discovered_set - expected_set)

    return {
        "sets_root": str(Path(sets_root).resolve()) if sets_root is not None else "part_calls/sets",
        "expected_count": len(expected),
        "discovered_count": len(discovered_names),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "missing": missing,
        "extra": extra,
        "discovered": discovered_names,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Report part-set migration status")
    parser.add_argument("--sets-root", default=None, help="Optional custom sets root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    status = build_status(sets_root=args.sets_root)
    if args.json:
        print(json.dumps(status, indent=2))
    else:
        print(f"expected:   {status['expected_count']}")
        print(f"discovered: {status['discovered_count']}")
        print(f"missing:    {status['missing_count']}")
        print(f"extra:      {status['extra_count']}")
