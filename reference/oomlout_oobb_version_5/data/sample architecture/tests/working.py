from __future__ import annotations


def define() -> list[dict]:
    return [
        {
            "name": "Integration (python): run folder test_data/example_duirectory",
            "type": "run_folder",
            "kind": "integration",
            "folder": "test_data/example_duirectory",
            "mode": "all",
        }
    ]
