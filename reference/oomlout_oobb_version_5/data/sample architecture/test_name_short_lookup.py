from __future__ import annotations

import argparse
from pathlib import Path

from oomlout_roboclick import build_action_lookup


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a name_short alias resolves to an action"
    )
    parser.add_argument(
        "alias",
        nargs="?",
        default="corel_file_close",
        help="Alias/name to test (default: corel_file_close)",
    )
    parser.add_argument(
        "--actions-root",
        default=None,
        help="Optional path to actions folder (defaults to ./actions)",
    )
    args = parser.parse_args()

    actions_root = Path(args.actions_root).resolve() if args.actions_root else None
    lookup = build_action_lookup(actions_root=actions_root)

    command = args.alias.strip()
    found = lookup.get(command)

    print(f"input: {command}")
    if found is None:
        print("found: NO")
        return 1

    print("found: YES")
    print(f"resolved_action_name: {found.name}")
    print(f"module_path: {found.path}")
    print(f"available_name_short_aliases: {list(found.aliases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
