from __future__ import annotations

import argparse
import ast
import importlib.util
import os
import sys
from pathlib import Path

PREVIEW_IMAGE_NAMES = (
    "image.png",
    "image_400.png",
    "image_120.png",
    "image_top.png",
    "image_top_400.png",
    "image_top_120.png",
    "image_side.png",
    "image_side_400.png",
    "image_side_120.png",
)


def _load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _file_exists_with_content(path: Path) -> bool:
    try:
        return path.exists() and path.stat().st_size > 0
    except OSError:
        return False


def _sample_names_from_working_file(working_file: Path) -> list[str]:
    try:
        tree = ast.parse(working_file.read_text(encoding="utf-8-sig"))
    except (OSError, SyntaxError):
        return []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != "test":
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Assign):
                continue
            if not any(isinstance(target, ast.Name) and target.id == "samples" for target in child.targets):
                continue
            try:
                samples = ast.literal_eval(child.value)
            except (ValueError, SyntaxError):
                return []
            names = []
            for sample in samples:
                if isinstance(sample, dict) and sample.get("filename"):
                    names.append(str(sample["filename"]))
            return names
    return []


def _component_preview_images_exist(component_dir: Path, sample_names: list[str]) -> bool:
    if not sample_names:
        return False
    for sample_name in sample_names:
        sample_dir = component_dir / "test" / sample_name
        if not all(_file_exists_with_content(sample_dir / image_name) for image_name in PREVIEW_IMAGE_NAMES):
            return False
    return True


def generate_all_component_tests(
    objects_root: str | Path = "components",
    skip_existing_images: bool = False,
) -> int:
    root = Path(objects_root).resolve()
    working_files = sorted(
        path for path in root.glob("*/working.py") if path.parent.name != "__pycache__"
    )

    previous_skip_value = os.environ.get("OOBB_SKIP_EXISTING_IMAGES")
    if skip_existing_images:
        os.environ["OOBB_SKIP_EXISTING_IMAGES"] = "1"

    attempted = 0
    completed = 0
    skipped = 0
    failures: list[tuple[str, str]] = []

    try:
        for working_file in working_files:
            component_name = working_file.parent.name
            try:
                if skip_existing_images:
                    sample_names = _sample_names_from_working_file(working_file)
                    if _component_preview_images_exist(working_file.parent, sample_names):
                        skipped += 1
                        print(f"[skip] {component_name}: existing preview images")
                        continue

                module = _load_module(working_file, f"component_test_{component_name}")
                test_fn = getattr(module, "test", None)
                if not callable(test_fn):
                    continue
                attempted += 1
                test_fn()
                completed += 1
                print(f"[ok] {component_name}")
            except Exception as exc:  # noqa: BLE001
                failures.append((component_name, f"{type(exc).__name__}: {exc}"))
                print(f"[fail] {component_name}: {type(exc).__name__}: {exc}")
    finally:
        if previous_skip_value is None:
            os.environ.pop("OOBB_SKIP_EXISTING_IMAGES", None)
        else:
            os.environ["OOBB_SKIP_EXISTING_IMAGES"] = previous_skip_value

    print("")
    print(f"Attempted: {attempted}")
    print(f"Completed: {completed}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {len(failures)}")
    if failures:
        print("Failures:")
        for component_name, message in failures:
            print(f" - {component_name}: {message}")

    return 0


def cli() -> int:
    parser = argparse.ArgumentParser(description="Generate all component test assets")
    parser.add_argument("--objects-root", default="components")
    parser.add_argument("--skip-existing-images", action="store_true")
    args = parser.parse_args()
    return generate_all_component_tests(
        objects_root=args.objects_root,
        skip_existing_images=args.skip_existing_images,
    )


if __name__ == "__main__":
    raise SystemExit(cli())
