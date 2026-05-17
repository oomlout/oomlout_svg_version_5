from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
ACTIONS_DIR = ROOT / "actions"


@dataclass
class Replacement:
    file_path: Path
    action_name: str
    variable_name: str
    old_description: str
    new_description: str
    strategy: str
    start: int
    end: int


def _iter_working_files() -> list[Path]:
    files: list[Path] = []
    if not ACTIONS_DIR.is_dir():
        return files
    for action_dir in sorted(ACTIONS_DIR.iterdir(), key=lambda p: p.name):
        working = action_dir / "working.py"
        if action_dir.is_dir() and working.is_file():
            files.append(working)
    return files


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(text):
        if char == "\n":
            starts.append(index + 1)
    return starts


def _to_offset(starts: list[int], lineno: int, col: int) -> int:
    return starts[lineno - 1] + col


def _humanize_token(token: str) -> str:
    cleaned = re.sub(r"[_\s]+", " ", token).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _ordinal_text(index: int) -> str:
    words = {
        1: "first",
        2: "second",
        3: "third",
        4: "fourth",
        5: "fifth",
        6: "sixth",
        7: "seventh",
        8: "eighth",
        9: "ninth",
        10: "tenth",
    }
    return words.get(index, f"{index}th")


CANONICAL_GLOSSARY: dict[str, str] = {
    "file_source": "Path to the source input file.",
    "file_destination": "Path to the output file to create or update.",
    "file_name": "File name to read or write for this action.",
    "file_name_full": "Full file path to save captured content.",
    "file_name_clip": "File path used to store clipboard text.",
    "file_source_trace": "Path to the raster file used for tracing.",
    "file_template": "Template file to render with Jinja variables.",
    "file_output": "Output file path for rendered text or converted assets.",
    "text": "Text content used by this action.",
    "content": "Text content to write into the created file.",
    "delay": "Delay duration in seconds.",
    "delay_trace": "Delay in seconds before trace-specific steps.",
    "delay_png": "Delay in seconds before PNG export steps.",
    "x": "X coordinate for placement.",
    "y": "Y coordinate for placement.",
    "width": "Target width for sizing or placement.",
    "height": "Target height for sizing or placement.",
    "max_dimension": "Maximum dimension allowed when scaling content.",
    "angle": "Rotation angle in degrees.",
    "font": "Font family name to apply.",
    "font_size": "Font size value to apply.",
    "bold": "Whether text should be bold.",
    "italic": "Whether text should be italic.",
    "order": "Object stacking order command (for example, to_front or to_back).",
    "url": "URL to open or use for the operation.",
    "url_chat": "Chat URL to continue an existing conversation.",
    "url_directory": "Subdirectory used when saving URL snapshots.",
    "log_url": "Whether to capture and store the current chat URL.",
    "method": "Execution method used by the action.",
    "mode": "Mode selector controlling action behavior.",
    "mode_ai_wait": "AI wait strategy (slow, fast_button_state, or fast_clipboard_state).",
    "position_click": "Screen position to click before executing the step.",
    "position": "Insertion position option for the target document.",
    "image_detail": "Prompt detail level for generated image instructions.",
    "index": "1-based index of the search result image to target.",
    "overwrite": "Whether existing output files should be overwritten.",
    "render_type": "Rendering mode passed to the OpenSCAD render step.",
    "scale": "Scale multiplier applied during image upscaling.",
    "crop": "Crop box or crop mode applied to the image.",
    "remove_background_color_from_entire_image": "Whether to remove the background color before tracing.",
    "number_of_colors": "Color count target used by trace settings.",
    "detail_minus": "Trace detail reduction amount.",
    "smoothing": "Trace smoothing level.",
    "corner_smoothness": "Corner smoothing level for trace output.",
    "ungroup": "Whether to ungroup objects after converting to curves.",
    "file_type": "Export file type or extension.",
    "page_number": "Target page number to switch to.",
    "search_and_replace": "Search/replace rules applied during templating.",
    "convert_to_pdf": "Whether to convert rendered output to PDF.",
    "convert_to_png": "Whether to convert rendered output to PNG.",
    "dict_data": "Dictionary data passed into template rendering.",
    "select_all": "Whether to select all objects before resizing.",
    "description": "Optional context note used by the action.",
    "clip": "Clipboard text payload to save.",
    "template": "Template identifier used when creating the document.",
    "title": "Title used when creating the document.",
    "folder": "Destination folder for the created document.",
}


ACTION_OVERRIDES: dict[tuple[str, str], str] = {
    ("roboclick_action_ai_new_chat", "description"): "Optional kickoff note sent in the first chat message.",
    ("roboclick_action_alias_new_chat", "description"): "Optional kickoff note sent in the first chat message.",
    ("roboclick_action_ai_query", "method"): "Query input method (typing or paste).",
    ("roboclick_action_alias_query", "method"): "Query input method (typing or paste).",
    ("roboclick_action_google_doc_new", "template"): "Template name used when creating a new Google Doc.",
    ("roboclick_action_google_doc_new", "title"): "Title for the new Google Doc.",
    ("roboclick_action_google_doc_new", "folder"): "Drive folder destination for the new Google Doc.",
    ("roboclick_action_google_doc_add_text", "position"): "Insertion position in the Google Doc (for example end).",
    ("roboclick_action_save_image_generated", "position_click"): "Screen position used to open the generated image context menu.",
    ("roboclick_action_save_image_search_result", "position_click"): "Base screen position for search results before index offset.",
    ("roboclick_action_save_image_search_result", "index"): "1-based search result index used to offset the click position.",
    ("roboclick_action_wait_for_file", "file_name"): "Primary file name to wait for in the action directory.",
    ("roboclick_action_corel_import", "special, 'no double click' - to deal with non square objects"): (
        "Special import flag to skip double-click sizing behavior for non-square objects."
    ),
}


def _fallback_description(variable_name: str) -> str:
    indexed_file_name = re.fullmatch(r"file_name_(\d+)", variable_name)
    if indexed_file_name:
        index = int(indexed_file_name.group(1))
        return f"{_ordinal_text(index)} candidate file name to wait for."

    if variable_name.endswith("_directory"):
        return f"Directory path for {_humanize_token(variable_name.removesuffix('_directory'))} files."

    if variable_name.startswith("mode_"):
        suffix = _humanize_token(variable_name.removeprefix("mode_"))
        return f"Mode selector for {suffix} behavior."

    if variable_name.startswith("file_"):
        suffix = _humanize_token(variable_name.removeprefix("file_"))
        return f"File path for {suffix}."

    if variable_name.startswith("delay_"):
        suffix = _humanize_token(variable_name.removeprefix("delay_"))
        return f"Delay in seconds for {suffix}."

    return f"Value for {_humanize_token(variable_name)}."


def _resolve_description(
    *,
    action_name: str,
    variable_name: str,
    old_source: str,
) -> tuple[str, str]:
    override = ACTION_OVERRIDES.get((action_name, variable_name))
    if override:
        return override, "action_override"

    if variable_name == "method":
        lowered = old_source.lower()
        if "typing" in lowered and "paste" in lowered:
            return "Input method to send content (typing or paste).", "context"

    glossary = CANONICAL_GLOSSARY.get(variable_name)
    if glossary:
        return glossary, "glossary"

    return _fallback_description(variable_name), "fallback"


def _get_function(tree: ast.Module, name: str) -> ast.FunctionDef | None:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def _describe_variable_replacements(path: Path) -> list[Replacement]:
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except Exception:
        return []

    describe_fn = _get_function(tree, "describe")
    if describe_fn is None:
        return []
    old_fn = _get_function(tree, "old")
    old_source = ast.get_source_segment(source, old_fn) if old_fn is not None else ""

    starts = _line_starts(source)
    replacements: list[Replacement] = []
    action_name = path.parent.name

    for node in ast.walk(describe_fn):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "append":
            continue
        if not node.args:
            continue
        arg = node.args[0]
        if not isinstance(arg, ast.Dict):
            continue

        variable_name: str | None = None
        description_node: ast.Constant | None = None
        description_value: str | None = None

        for key_node, value_node in zip(arg.keys, arg.values):
            if not isinstance(key_node, ast.Constant) or not isinstance(key_node.value, str):
                continue
            if key_node.value == "name":
                if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str):
                    variable_name = value_node.value
            if key_node.value == "description":
                if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str):
                    description_node = value_node
                    description_value = value_node.value

        if not variable_name or description_node is None or description_value is None:
            continue
        if not description_value.startswith("Legacy parameter:"):
            continue
        if (
            description_node.end_lineno is None
            or description_node.end_col_offset is None
            or description_node.lineno is None
            or description_node.col_offset is None
        ):
            continue

        new_description, strategy = _resolve_description(
            action_name=action_name,
            variable_name=variable_name,
            old_source=old_source,
        )
        if new_description == description_value:
            continue

        start = _to_offset(starts, description_node.lineno, description_node.col_offset)
        end = _to_offset(starts, description_node.end_lineno, description_node.end_col_offset)
        replacements.append(
            Replacement(
                file_path=path,
                action_name=action_name,
                variable_name=variable_name,
                old_description=description_value,
                new_description=new_description,
                strategy=strategy,
                start=start,
                end=end,
            )
        )

    return replacements


def _apply_replacements(source: str, replacements: Iterable[Replacement]) -> str:
    updated = source
    for item in sorted(replacements, key=lambda r: r.start, reverse=True):
        updated = updated[: item.start] + repr(item.new_description) + updated[item.end :]
    return updated


def _write_report(path: Path, replacements: list[Replacement], files_scanned: int) -> None:
    by_strategy: dict[str, int] = {}
    by_action: dict[str, int] = {}
    fallback_rows: list[Replacement] = []
    for item in replacements:
        by_strategy[item.strategy] = by_strategy.get(item.strategy, 0) + 1
        by_action[item.action_name] = by_action.get(item.action_name, 0) + 1
        if item.strategy == "fallback":
            fallback_rows.append(item)

    lines: list[str] = []
    lines.append("# Variable Description Migration Report")
    lines.append("")
    lines.append(f"- Files scanned: {files_scanned}")
    lines.append(f"- Files changed: {len({r.file_path for r in replacements})}")
    lines.append(f"- Variable descriptions rewritten: {len(replacements)}")
    lines.append("")
    lines.append("## Rewrite Strategy Counts")
    lines.append("")
    for key in sorted(by_strategy):
        lines.append(f"- `{key}`: {by_strategy[key]}")
    if not by_strategy:
        lines.append("- none")
    lines.append("")
    lines.append("## Changes By Action")
    lines.append("")
    for action_name, count in sorted(by_action.items()):
        lines.append(f"- `{action_name}`: {count}")
    if not by_action:
        lines.append("- none")
    lines.append("")
    lines.append("## Rewritten Variables")
    lines.append("")
    lines.append("| Action | Variable | Strategy | Old | New |")
    lines.append("| --- | --- | --- | --- | --- |")
    for item in sorted(replacements, key=lambda x: (x.action_name, x.variable_name)):
        old = item.old_description.replace("|", "\\|")
        new = item.new_description.replace("|", "\\|")
        lines.append(
            f"| `{item.action_name}` | `{item.variable_name}` | `{item.strategy}` | {old} | {new} |"
        )
    if not replacements:
        lines.append("| - | - | - | - | - |")
    lines.append("")
    lines.append("## Fallback-Generated Entries")
    lines.append("")
    if fallback_rows:
        for item in sorted(fallback_rows, key=lambda x: (x.action_name, x.variable_name)):
            lines.append(
                f"- `{item.action_name}` / `{item.variable_name}` -> {item.new_description}"
            )
    else:
        lines.append("- none")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(*, check_only: bool, report_path: Path | None) -> int:
    files = _iter_working_files()
    all_replacements: list[Replacement] = []
    changed_files: list[Path] = []

    for path in files:
        source = path.read_text(encoding="utf-8")
        replacements = _describe_variable_replacements(path)
        if not replacements:
            continue
        all_replacements.extend(replacements)
        updated = _apply_replacements(source, replacements)
        if updated != source:
            changed_files.append(path)
            if not check_only:
                path.write_text(updated, encoding="utf-8")

    if report_path is not None:
        _write_report(report_path, all_replacements, len(files))

    print(f"Files scanned: {len(files)}")
    print(f"Files with rewrites: {len({r.file_path for r in all_replacements})}")
    print(f"Variable descriptions to rewrite: {len(all_replacements)}")
    for path in sorted({r.file_path for r in all_replacements}):
        count = sum(1 for item in all_replacements if item.file_path == path)
        print(f"  - {path.relative_to(ROOT)} ({count})")
    if report_path is not None:
        print(f"Report: {report_path}")

    if check_only:
        print("Mode: check (no files modified)")
    else:
        print(f"Mode: apply (files changed: {len(changed_files)})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Show pending rewrites only.")
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional markdown report output path.",
    )
    args = parser.parse_args()
    return run(check_only=args.check, report_path=args.report)


if __name__ == "__main__":
    raise SystemExit(main())
